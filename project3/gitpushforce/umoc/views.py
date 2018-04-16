from django.views import generic
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from datetime import datetime
import json

from .models import UserProfile, Trip, Comment
from .forms import *

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
	print('Equals itself? {}'.format(profile == profile))
	
	notifications = profile.notification_set.all()
	
	print ('Found profile {}'.format(profile))
	print ('User has {} notifications:'.format(len(notifications)))
	for n in notifications:
		print (n)
		
	return render(
		request,
		'index.html',
		context={'num_users':num_users,'num_trips':num_trips, 'num_admins':num_admins },
	)

def dashboard(request):
	"""
	View function for home page of site.
	"""
	return render(
		request,
		'dashboard.html',
		context={'trips': Trip.objects.all() },
	)


def register(request):
	"""
	View function where new users register.
	"""
	# return render(
		# request,
		# 'register.html',
		# context={},
	# )
	
	if request.method == 'POST':
		form = RegisterForm(request.POST)
		
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			raw_password = form.cleaned_data.get('password1')
			user = authenticate(username=username, password=raw_password)
			login(request, user)
			return redirect('dashboard')
	
	else:
		form = RegisterForm()
	
	return render(request, 'register.html', {'form': form})
		
		
def profile(request):
	"""
	View function for home page of site.
	"""
	return render(
		request,
		'profile.html',
		context={},
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
		return context


class TripInfoView(generic.DetailView):
	model = Trip
	template_name = 'trip_info.html'
	
	def trip_detail_view(request,pk):
		print ('received id {}'.format(pk))  # TODO: WHY IS IT NOT PRINTING???
		try:
			queried_trip = Trip.objects.get(pk=pk)
		except Trip.DoesNotExist:
			raise Http404("Trip does not exist")
	
		return render(
			request,
			'trip_info.html',
			context={'trip': queried_trip} # queried_trip.num_seats - queried_trip.participants.count()}
		)
		
	
class UserInfoView(generic.DetailView):
	model = UserProfile
	template_name = 'public_profile.html'
	
	def user_detail_view(request,pk):
		try:
			user_id = UserProfile.objects.get(pk=pk)
		except UserProfile.DoesNotExist:
			raise Http404("UserProfile does not exist")

		profile = UserProfile.objects.get(pk=pk)
	
		return render(
			request,
			'public_profile.html',
			context={'profile': profile}
		)

def trip_info(request, trip_id):  # TODO: IS THIS EVEN USED???
	"""
	Serves information page for trip with given trip_id.
	"""
	return render(
		request,
		'trip_info.html',
		context={'trip': Trip.objects.get(pk=pk)},
	)

	
def trip_comments(request, pk):
	""" 
	Return JSON of all comments for a given trip id.
	"""
	print ('Retrieving comments for trip id {}'.format(pk))
	# TODO: CHECK IF TRIP IS IN DATABASE
	comments = Comment.objects.all()
	data = []
	for comment in comments:
		data.append({ 'id': comment.id, 'parent': comment.parent.id if comment.parent else 0, 'author_id': comment.author.id, 'author_name': '{} {}'.format(comment.author.first_name, comment.author.last_name), 'text': comment.text, 'timestamp': comment.time_stamp})
	print (data)
	return JsonResponse(data, safe=False)

def trip_planner(request):
	"""
	View function for home page of site.
	"""
	return render(
		request,
		'trip_planner.html',
		context={'profiles': [UserProfile.objects.all()]},
	)

def admin_management(request):
	"""
	View function for home page of site.
	"""
	# Generate counts of some of the main objects
	num_users=UserProfile.objects.all().count()
	num_leaders=UserProfile.objects.filter(admin_level__exact='l').count()
	num_admins=UserProfile.objects.filter(admin_level__exact='a').count()

	return render(
		request,
		'admin_management.html',
		context={'num_users':num_users, 'num_leaders': num_leaders, 'num_admins': num_admins}
	)


def waiver(request):
   return render(
      request,
      'waiver.html',
      context={},
   )


class AdminTripPlanner(PermissionRequiredMixin, generic.ListView):
	model = Trip
	template_name = 'trip_planner.html'
	permission_required = 'catalog.can_be_edited'

	#permission_required = 'catalog.can_mark_returned'

	def get_context_data(self, **kwargs):
		user = User.objects.filter(first_name__exact='Stefan')[0]
		notifications = user.notification_set.all()
		context = super(AdminTripPlanner, self).get_context_data(**kwargs)
		context['profiles'] = [UserProfile.objects.all()]
		return context



class TripCreate(CreateView):
    model = Trip
    fields = '__all__'
    # initial={'description':'05/01/2018',}

class TripUpdate(UpdateView):
    model = Trip
    fields = ['name','description','num_seats','start_time', 'end_time', 'cancelled']

class TripDelete(DeleteView):
    model = Trip
    success_url = reverse_lazy('authors')



