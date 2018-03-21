from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
	path('dashboard/', views.TripListView.as_view(), name='dashboard'),
	path('profile/', views.profile, name='profile'),
	# trip path must include an integer trip_id field
	path('trip/<int:trip_id>', views.TripInfoView.as_view(), name='trip_info'),
	path('admin_trip_planner/', views.admin_trip_planner, name='admin_trip_planner'),
	path('admin_management/', views.admin_management, name='admin_management'),
]