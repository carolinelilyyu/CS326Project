from django.contrib import admin
from .models import UserProfile, Trip, Comment, Notification

class TripAdmin(admin.ModelAdmin):
	list_display = ('name', 'description', 'num_seats', 'tag')
	search_fields = ('name', 'num_seats', 'tag')

class UserAdmin(admin.ModelAdmin):
	list_display = ('first_name', 'last_name')
	search_fields = ('first_name', 'last_name')


# Register your models here.
admin.site.register(UserProfile, UserAdmin)
admin.site.register(Trip, TripAdmin) 
admin.site.register(Comment)
admin.site.register(Notification)

admin.site.site_header = 'UMOC Administration'