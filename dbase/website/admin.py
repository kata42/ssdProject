from django.contrib import admin
from .models import Profile, specialities, insurances, Doctor


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'gender','profileFilled','bdate', 'photo']


class SpecialityAdmin(admin.ModelAdmin):
    list_display = ['speciality_name']

class InsuranceAdmin(admin.ModelAdmin):
    list_display = ['insurance_name']


class DoctorAdmin(admin.ModelAdmin):
    list_display = ['user','organization','speciality','rating','phoneNumber','address']

admin.site.register(Profile, ProfileAdmin)
admin.site.register(specialities, SpecialityAdmin)
admin.site.register(insurances, InsuranceAdmin)
admin.site.register(Doctor, DoctorAdmin)
