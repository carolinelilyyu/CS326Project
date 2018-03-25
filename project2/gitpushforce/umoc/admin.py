from django.contrib import admin
from .models import User, Trip, Comment, Notification

# Register your models here.
admin.site.register(User)
admin.site.register(Trip) 
admin.site.register(Comment)
admin.site.register(Notification)

