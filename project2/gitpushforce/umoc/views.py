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

	
	# Render the HTML template index.html with the data in the context variable
	
	# "Caroline's note to clarify what render does":

	# Render creates an html page as a response
	# GIVEN: request object (HttpRequest), HTML template with placeholder for data, and context variable (data to be inserted into placeholders)
	return render(
		request,
		'index.html',
		context={'num_users':num_users,'num_trips':num_trips, 'num_admins':num_admins},
	)

def dashboard(request):
	"""
	View function for home page of site.
	"""
	# Generate counts of some of the main objects
	num_trips=Trip.objects.all().count()

	
	# Render the HTML template index.html with the data in the context variable
	
	# "Caroline's note to clarify what render does":

	# Render creates an html page as a response
	# GIVEN: request object (HttpRequest), HTML template with placeholder for data, and context variable (data to be inserted into placeholders)
	return render(
		request,
		'dashboard.html',
		context={'num_trips':num_trips, 'user': user_sample, 'trips': [trip_sample]},
	)


def profile(request):
	"""
	View function for home page of site.
	"""
	# Generate counts of some of the main objects
	num_trips=Trip.objects.all().count()

	
	# Render the HTML template index.html with the data in the context variable
	
	# "Caroline's note to clarify what render does":

	# Render creates an html page as a response
	# GIVEN: request object (HttpRequest), HTML template with placeholder for data, and context variable (data to be inserted into placeholders)
	return render(
		request,
		'profile_info.html',
		context={'num_trips':num_trips, 'user': user_sample},
	)

class TripListView(generic.ListView):
    model = Trip
    template_name = 'dashboard.html'  # Specify your own template name/location

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(TripListView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['some_data'] = 'This is just some data'
        return context

class TripInfoView(generic.DetailView):
    model = Trip
    template_name = 'trip_info.html'

    def trip_detail_view(request,pk):
        try:
            trip_id=Trip.objects.get(pk=pk)
        except Trip.DoesNotExist:
            raise Http404("Trip does not exist")

        #book_id=get_object_or_404(Book, pk=pk)
        
        return render(
            request,
            'trip_info.html',
            context={'trip':trip_id,}
        )

def trip_info(request, trip_id):
	"""
	Serves information page for trip with given trip_id.
	"""
	print('Received trip_id {}'.format(trip_id))
	# Generate counts of some of the main objects
	num_trips=Trip.objects.all().count()

	
	# Render the HTML template index.html with the data in the context variable
	
	# "Caroline's note to clarify what render does":

	# Render creates an html page as a response
	# GIVEN: request object (HttpRequest), HTML template with placeholder for data, and context variable (data to be inserted into placeholders)
	return render(
		request,
		'trip_info.html',
		context={'num_trips':num_trips, 'user': user_sample, 'trip':trip_sample},
	)


def admin_trip_planner(request):
	"""
	View function for home page of site.
	"""
	# Generate counts of some of the main objects
	num_trips=Trip.objects.all().count()

	
	# Render the HTML template index.html with the data in the context variable
	
	# "Caroline's note to clarify what render does":

	# Render creates an html page as a response
	# GIVEN: request object (HttpRequest), HTML template with placeholder for data, and context variable (data to be inserted into placeholders)
	return render(
		request,
		'admin_trip_planner.html',
		context={'num_trips':num_trips, 'users': [user_sample]},
	)

def admin_management(request):
	"""
	View function for home page of site.
	"""
	# Generate counts of some of the main objects
	num_trips=Trip.objects.all().count()

	
	# Render the HTML template index.html with the data in the context variable
	
	# "Caroline's note to clarify what render does":

	# Render creates an html page as a response
	# GIVEN: request object (HttpRequest), HTML template with placeholder for data, and context variable (data to be inserted into placeholders)
	return render(
		request,
		'admin_management.html',
		context={'num_trips':num_trips, 'users': [user_sample]},
	)