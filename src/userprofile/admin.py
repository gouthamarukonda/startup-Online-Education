from django.contrib import admin

from .models import UserProfile

class UserProfileAdmin(admin.ModelAdmin):
	list_display = ('user', 'role', 'PROGRAMS', 'gender', 'mobile', 'institute', 'dob', 'address', 'status')
	fields = ('user' , 'role', 'gender', 'mobile', 'institute', 'dob', 'address', 'status')

admin.site.register(UserProfile, UserProfileAdmin)
