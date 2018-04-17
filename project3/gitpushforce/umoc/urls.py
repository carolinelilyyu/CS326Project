from django.urls import path, include
from . import views
from django.conf.urls import url

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.TripListView.as_view(), name='dashboard'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('profile2/<pk>', views.profile2, name='profile2'),
    url(r'^user/(?P<pk>\d+)/$', views.UserInfoView.as_view(), name='public_profile'),
    url(r'^trip/(?P<pk>\d+)/$', views.TripInfoView.as_view(), name='trip_info'),
    url(r'^trip/(?P<pk>\d+)/comments$', views.trip_comments, name='trip_comments'),
    path('waiver/', views.waiver, name = 'waiver'),
    path('trip_planner/', views.trip_planner, name='trip_planner'),
    path('administration/', views.admin_management, name='admin_management'),
    path('trip/create/', views.TripCreate.as_view(), name='trip_create'),
    path('trip/<int:pk>/update/', views.TripUpdate.as_view(), name='trip_update'),
    path('trip/<int:pk>/delete/', views.TripDelete.as_view(), name='trip_delete'),
]
#Add Django site authentication urls (for login, logout, password management)
urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]
