from django.urls import path
from . import views
from django.conf.urls import url

urlpatterns = [
    path('', views.index, name='index'),
	path('dashboard/', views.TripListView.as_view(), name='dashboard'),
	path('register/', views.register, name='register'),
	path('profile/', views.profile, name='profile'),
	# trip path must include an integer trip_id field
	# path('trip/<int:trip_id>', views.TripInfoView.as_view(), name='trip_info'),
	url(r'^trip/(?P<pk>\d+)/$', views.TripInfoView.as_view(), name='trip_info'),
	url(r'^profile_info/(?P<pk>\d+)/$', views.UserInfoView.as_view(), name='profile_info'),
    path('waiver/', views.waiver, name = 'waiver'),
    path('admin_trip_planner/', views.admin_trip_planner, name='admin_trip_planner'),
    path('admin_management/', views.admin_management, name='admin_management'),
]