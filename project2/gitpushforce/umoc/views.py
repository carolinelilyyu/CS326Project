from django.shortcuts import render

# Create your views here.
from .models import User, Trip
from datetime import datetime
from django.views import generic

# Sample models!!!
user_sample = User(first_name='Stefan', last_name='Kussmaul', email='stefankussmaul@umass.edu', phone_num='1234567890', admin_level='l', dob=datetime.strptime('Jun 1 1998 1:33PM', '%b %d %Y %I:%M%p'))

trip_sample = Trip(name='Trip 1', description='This is our first trip', num_seats=10, start_time=datetime.strptime('Mar 29 2018 1:30PM', '%b %d %Y %I:%M%p'), end_time=datetime.strptime('Mar 29 2018 5:00PM', '%b %d %Y %I:%M%p'), cancelled=False, tag='r', leader=user_sample)

def index(request):
	"""
	View function for home page of site.
	"""
	# Generate counts of some of the main objects
	num_users=User.objects.all().count()
	num_trips=Trip.objects.all().count()
	num_admins=User.objects.filter(admin_level__exact='a').count()

	user = User.objects.filter(first_name__exact='Stefan')[0]
	notifications = user.notification_set.all()
	
	print ('Found user {}'.format(user))
	print ('User has {} notifications:'.format(len(notifications)))
	for n in notifications:
		print (n)
		
	return render(
		request,
		'index.html',
		context={'num_users':num_users,'num_trips':num_trips, 'num_admins':num_admins, 'user': user, notifications: notifications },
	)

def dashboard(request):
	"""
	View function for home page of site.
	"""
	user = User.objects.filter(first_name__exact='Stefan')[0]
	notifications = user.notification_set.all()
	
	return render(
		request,
		'dashboard.html',
		context={'user': user, 'trips': [trip_sample], notifications: notifications},
	)


def profile(request):
	"""
	View function for home page of site.
	"""

	user = User.objects.filter(first_name__exact='Stefan')[0]
	notifications = user.notification_set.all()
	
	return render(
		request,
		'profile_info.html',
		context={'user': user, notifications: notifications},
	)

class TripListView(generic.ListView):
	model = Trip
	template_name = 'dashboard.html'  # Specify your own template name/location
	num_trips=Trip.objects.all().count()
	
	user = User.objects.filter(first_name__exact='Stefan')[0]
	notifications = user.notification_set.all()
	
	def get_context_data(self, **kwargs):
		# Call the base implementation first to get the context
		context = super(TripListView, self).get_context_data(**kwargs)
		# Create any data and add it to the context
		context['some_data'] = 'This is just some data'
		context['count'] = self.get_queryset().count()
		context['user'] = user
		context['notifications'] = notifications
		return context


class TripInfoView(generic.DetailView):
	model = Trip
	template_name = 'trip_info.html'
	
	def trip_detail_view(request,pk):
		try:
			trip_id=Trip.objects.get(pk=pk)
		except Trip.DoesNotExist:
			raise Http404("Trip does not exist")

		user = User.objects.filter(first_name__exact='Stefan')[0]
		notifications = user.notification_set.all()
	
		return render(
			request,
			'trip_info.html',
			context={'trip': trip_id, 'user': user, notifications: notifications}
		)

def trip_info(request, trip_id):
	"""
	Serves information page for trip with given trip_id.
	"""
	user = User.objects.filter(first_name__exact='Stefan')[0]
	notifications = user.notification_set.all()

	return render(
		request,
		'trip_info.html',
		context={'user': user, notifications: notifications, 'trip':trip_sample},
	)


def admin_trip_planner(request):
	"""
	View function for home page of site.
	"""
	user = User.objects.filter(first_name__exact='Stefan')[0]
	notifications = user.notification_set.all()
	
	return render(
		request,
		'admin_trip_planner.html',
		context={'user': user, 'notifications': notifications, 'users': [user_sample]},
	)

def admin_management(request):
	"""
	View function for home page of site.
	"""
	# Generate counts of some of the main objects
	num_users=User.objects.all().count()
	num_leaders=User.objects.filter(admin_level__exact='l').count()
	num_admins=User.objects.filter(admin_level__exact='a').count()
	user = User.objects.filter(first_name__exact='Stefan')[0]
	notifications = user.notification_set.all()

	return render(
		request,
		'admin_management.html',
		context={'num_users':num_users, 'num_leaders': num_leaders, 'num_admins': num_admins, 'user': user, 'notifications': notifications}
	)