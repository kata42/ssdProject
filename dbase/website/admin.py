from django.contrib import admin
from .models import Profile, Doctor


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'gender','profileFilled','bdate', 'photo']

class DoctorAdmin(admin.ModelAdmin):
    list_display = ['user','organization','specialization','rating','phoneNumber','address']

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Doctor, DoctorAdmin)
