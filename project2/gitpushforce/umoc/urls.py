from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
]

#Users: able to view trips, summaries, tags, and led by
#Admin: above and can add trips (going to have to make add trip exclusive to admins)
urlpatterns += [
    path('dashboard/', views.dashboard, name='dashboard'),
]

#gets the specific information of the trip. able to put user in trip. able to view member info(?)
urlpatterns += [
    path('trip_info/', views.trip_info, name='trip_info'),
]

#gets the information of a user
urlpatterns += [
    path('profile_info/', views.profile_info, name='profile_info'),
]

#admins: download information about trip. gives table of users on trip/ checks if they signed waivers. batch downloads waiver pdf
urlpatterns += [
    path('admin_trip_planner/', views.admin_trip_planner, name='admin_trip_planner'),
]

#admins: to change who gets to be leader or not
urlpatterns += [
    path('admin_management/', views.admin_management, name='admin_management'),
]