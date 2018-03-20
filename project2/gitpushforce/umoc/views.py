from django.shortcuts import render

# Create your views here.
from .models import User, Trip

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
		context={'num_trips':num_trips},
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
		context={'num_trips':num_trips},
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
		context={'num_trips':num_trips},
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
		context={'num_trips':num_trips},
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
		context={'num_trips':num_trips},
	)