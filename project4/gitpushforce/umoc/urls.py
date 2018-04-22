from django.urls import path, include
from . import views
from django.conf.urls import url

urlpatterns = [
    path('', views.index, name='index'),
	path('notifications', views.notifications, name='notifications'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    url(r'^profile/(?P<pk>\d+)/$', views.public_profile, name='public_profile'),
    url(r'^trip/(?P<pk>\d+)/$', views.trip_info, name='trip_info'),
    url(r'^trip/(?P<pk>\d+)/comments$', views.trip_comments, name='trip_comments'),
    path('waiver/', views.waiver, name = 'waiver'),
    path('administration/', views.admin_management, name='admin_management'),
    path('trip/create/', views.TripCreate.as_view(), name='trip_create'),
    path('trip/<int:pk>/edit/', views.TripUpdate.as_view(), name='trip_update'),
    path('trip/<int:pk>/cancel/', views.cancel_trip, name='trip_cancel'),
	path('trip/<int:pk>/join/', views.join_trip, name='trip_join'),
	path('trip/<int:pk>/leave/', views.leave_trip, name='trip_leave'),
	path('trip/<int:pk>/report/', views.trip_report, name='trip_report'),
]

urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]
