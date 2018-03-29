from django.contrib import admin
from .models import User, Trip, Comment, Notification

class TripAdmin(admin.ModelAdmin):
	list_display = ('name', 'description', 'num_seats', 'tag')
	search_fields = ('name', 'num_seats', 'tag')

class UserAdmin(admin.ModelAdmin):
	list_display = ('first_name', 'last_name', 'email')
	search_fields = ('first_name', 'last_name', 'email')


# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Trip, TripAdmin) 
admin.site.register(Comment)
admin.site.register(Notification)

admin.site.site_header = 'UMOC Administration'