from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm, SearchForm
from django.contrib.auth.decorators import login_required
from .models import Profile, dummyDoctor
from django.contrib import messages
from django.core.files import File
import googlemaps
import json
from geopy import geocoders
import names
import random
from random import randint

insurances = ["Aetna", "American Republic", "Amerigroup", "Bakery & Confectionary Union Plan", "CareSource", "Cigna",
              "Commercial Insurance Company", "Community Health Choice", "Coventry Health Care", "Golden Rule",
              "Government Employees Health Association", "Health Net", "HealthPlus", "HealthPlus Amerigroup", "Medico",
              "Midwest Health Plan", "National Elevator", "Principal Life", "UnitedHealthCare", "Universal American",
              "Blue Cross and Blue Shield"]

specialities = ["Opthalmologist", "Dermatologist", "Cardiologist", "Psychiatrist", "Gastroenterologist", "ENT", "Obstetrician", "Neurologist",
                "Dentist", "Prosthodontist", "Endodontist", "Implantologist", "Ayurveda","Acupuncturist", "Physiotherapist",
                "Psychologist", "Audiologist", "Speech Therapist", "Dietitian", "General"]


@login_required
def dashboard(request):
    return render(request,'account/dashboard.html',{'section': 'dashboard'})

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(
                    user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            profile = Profile.objects.create(user=new_user)
            return render(request,
                    'account/register_done.html',
                    {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request,'account/register.html',{'user_form': user_form})

@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,
                       data=request.POST,
                       files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully')
    else:
        messages.success(request, 'Error updating your profile')
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(
        instance=request.user.profile)
    return render(request,
                  'account/edit.html',
                  {'user_form': user_form,
                  'profile_form': profile_form})
def phn():
    n = '0000000000'
    while '9' in n[3:6] or n[3:6]=='000' or n[6]==n[7]==n[8]==n[9]:
        n = str(random.randint(10**9, 10**10-1))
    return n[:3] + '-' + n[3:6] + '-' + n[6:]


def index(request):
    search_form = SearchForm(auto_id=False)
    if request.method == 'POST':
        search_form =  SearchForm(request.POST)
        if search_form.is_valid():
            inputAddress = search_form.cleaned_data['search']#Search Term
            hPlace = 'hospital'
            # Geocoding an address
            gmaps = googlemaps.Client(key='AIzaSyAYCiTaPolA8Y-JbDjXTmfpjuJ-FaJAR8Q')
            # Derive lat and long of a given Place
            g = geocoders.GoogleV3(api_key='AIzaSyAYCiTaPolA8Y-JbDjXTmfpjuJ-FaJAR8Q')
            derived = g.geocode(inputAddress, timeout=10)
            derLocation = []
            derLocation.append(derived.latitude)
            derLocation.append(derived.longitude)
            result = gmaps.places_nearby(derLocation, radius=1500, type=hPlace)
            j = json.loads(json.dumps(result))
            jsonData = j["results"]
            doctors = []
            for item in jsonData:
                fullname = names.get_full_name()
                name = item.get("name")#organization
                speciality = random.choice(specialities)
                ins = random.choice(insurances)
                vicinity = item.get("vicinity")#address
                rtng = random.randint(0, 5)
                phone_number = phn()
                doctors.append(dummyDoctor(fullname = fullname, organization = name,specialization = speciality,insurance = ins,rating = rtng, phoneNumber = phone_number,address = vicinity))
            return render(request, 'account/index.html',{'search_form': search_form,'doctors': doctors,})
    return render(request,'account/index.html',{'search_form': search_form})

def about(request):
    return render(request,'account/about.html')
