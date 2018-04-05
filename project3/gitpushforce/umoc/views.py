from django.shortcuts import render

# Create your views here.
from .models import UserProfile, Trip
from datetime import datetime
from django.views import generic


def index(request):
	"""
	View function for home page of site.
	"""
	# Generate counts of some of the main objects
	num_users=UserProfile.objects.all().count()
	num_trips=Trip.objects.all().count()
	num_admins=UserProfile.objects.filter(admin_level__exact='a').count()

	print (UserProfile.objects.all())
	profile = UserProfile.objects.filter(first_name__exact='Stefan')[0]
	print(profile.profile_img.__dir__())
	print(profile.profile_img.name)
	print(profile.profile_img.url)
	
	notifications = profile.notification_set.all()
	
	print ('Found profile {}'.format(profile))
	print ('User has {} notifications:'.format(len(notifications)))
	for n in notifications:
		print (n)
		
	return render(
		request,
		'index.html',
		context={'num_users':num_users,'num_trips':num_trips, 'num_admins':num_admins, 'profile': profile, notifications: notifications },
	)

def dashboard(request):
	"""
	View function for home page of site.
	"""
	profile = UserProfile.objects.filter(first_name__exact='Stefan')[0]
	notifications = profile.notification_set.all()
	
	return render(
		request,
		'dashboard.html',
		context={'profile': profile, 'trips': [trip_sample], notifications: notifications},
	)


def profile(request):
	"""
	View function for home page of site.
	"""

	profile = UserProfile.objects.filter(first_name__exact='Stefan')[0]
	notifications = profile.notification_set.all()
	
	return render(
		request,
		'profile_info.html',
		context={'profile': profile, notifications: notifications},
	)

class TripListView(generic.ListView):
	model = Trip
	template_name = 'dashboard.html'  # Specify your own template name/location
	num_trips=Trip.objects.all().count()
	
	def get_context_data(self, **kwargs):
		# Call the base implementation first to get the context
		context = super(TripListView, self).get_context_data(**kwargs)
		# Create any data and add it to the context
		context['some_data'] = 'This is just some data'
		context['count'] = self.get_queryset().count()
		profile = UserProfile.objects.filter(first_name__exact='Stefan')[0]
		notifications = profile.notification_set.all()
		context['profile'] = profile
		context['notifications'] = notifications
		return context


class TripInfoView(generic.DetailView):
	model = Trip
	template_name = 'trip_info.html'
	
	def trip_detail_view(request,pk):
		print ('received id {}'.format(pk))  # TODO: WHY IS IT NOT PRINTING???
		try:
			queried_trip = Trip.objects.get(pk=pk)
			print ('{} seats available'.format(queried_trip.num_seats - len(queried_trip.participants)) )
		except Trip.DoesNotExist:
			raise Http404("Trip does not exist")

		profile = UserProfile.objects.filter(first_name__exact='Stefan')[0]
		notifications = profile.notification_set.all()
	
		return render(
			request,
			'trip_info.html',
			context={'trip': queried_trip, 'profile': profile, notifications: notifications, 'num_seats_remaining': 2} # queried_trip.num_seats - queried_trip.participants.count()}
		)


class UserInfoView(generic.DetailView):
	model = UserProfile
	template_name = 'profile_info.html'
	
	def user_detail_view(request,pk):
		try:
			user_id=UserProfile.objects.get(pk=pk)
		except UserProfile.DoesNotExist:
			raise Http404("UserProfile does not exist")

		profile = UserProfile.objects.filter(first_name__exact='Stefan')[0]
		notifications = profile.notification_set.all()
	
		return render(
			request,
			'profile_info.html',
			context={'user_id': user_id, notifications: notifications}
		)

def trip_info(request, trip_id):
	"""
	Serves information page for trip with given trip_id.
	"""
	profile = UserProfile.objects.filter(first_name__exact='Stefan')[0]
	notifications = profile.notification_set.all()

	return render(
		request,
		'trip_info.html',
		context={'profile': profile, notifications: notifications, 'trip':trip_sample},
	)


def admin_trip_planner(request):
	"""
	View function for home page of site.
	"""
	profile = UserProfile.objects.filter(first_name__exact='Stefan')[0]
	notifications = profile.notification_set.all()
	
	return render(
		request,
		'admin_trip_planner.html',
		context={'profile': profile, 'notifications': notifications, 'profiles': [UserProfile.objects.all()]},
	)

def admin_management(request):
	"""
	View function for home page of site.
	"""
	# Generate counts of some of the main objects
	num_users=UserProfile.objects.all().count()
	num_leaders=UserProfile.objects.filter(admin_level__exact='l').count()
	num_admins=UserProfile.objects.filter(admin_level__exact='a').count()
	profile = UserProfile.objects.filter(first_name__exact='Stefan')[0]
	notifications = profile.notification_set.all()

	return render(
		request,
		'admin_management.html',
		context={'num_users':num_users, 'num_leaders': num_leaders, 'num_admins': num_admins, 'profile': profile, 'notifications': notifications}
	)


def waiver(request):
   profile = UserProfile.objects.filter(first_name__exact='Stefan')[0]
   notifications = profile.notification_set.all()

   return render(
      request,
      'waiver.html',
      context={'profile': profile, 'trips': [trip_sample], notifications: notifications},
   )
