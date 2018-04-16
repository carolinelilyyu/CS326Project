from django.urls import path
from . import views
from django.conf.urls import url

urlpatterns = [
    path('', views.index, name='index'),
	path('dashboard/', views.TripListView.as_view(), name='dashboard'),
	path('register/', views.register, name='register'),
	path('profile/', views.profile, name='profile'),
	url(r'^user/(?P<pk>\d+)/$', views.UserInfoView.as_view(), name='public_profile'),
	url(r'^trip/(?P<pk>\d+)/$', views.TripInfoView.as_view(), name='trip_info'),
	url(r'^trip/(?P<pk>\d+)/comments$', views.trip_comments, name='trip_comments'),
    path('waiver/', views.waiver, name = 'waiver'),
    path('trip_planner/', views.trip_planner, name='trip_planner'),
    path('administration/', views.admin_management, name='admin_management'),
]