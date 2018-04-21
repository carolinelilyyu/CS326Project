from django import forms
from django.urls import reverse, reverse_lazy
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse, Http404
from django.views import generic
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required
from django.core.exceptions import ValidationError
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from datetime import *
import json

from .models import UserProfile, Trip, Comment, Notification
from .forms import *


def index(request):
	"""
	View function for home page of site.
	"""
	
	num_users = UserProfile.objects.all().count()
	num_trips = Trip.objects.all().count()
	num_admins = UserProfile.objects.filter(admin_level__exact='a').count()
	
	return render(
		request,
		'index.html',
		context={'num_users': num_users, 'num_trips': num_trips, 'num_admins': num_admins}
	)


def register(request):
	"""
	View function where new users register.
	"""
	
	if request.method == 'POST':
		form = RegisterForm(request.POST)
		
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			raw_password = form.cleaned_data.get('password1')
			user = authenticate(username=username, password=raw_password)
			
			userpro = UserProfile(user=user, first_name = form.cleaned_data.get('first_name'), last_name = form.cleaned_data.get('last_name'))
			userpro.save()
			
			login(request, user)
			return redirect('dashboard')
	
	else:
		form = RegisterForm()
	
	return render(request, 'register.html', {'form': form})


def profile(request):
	"""
	View function for profile page of site.
	"""
	
	user = request.user
	profile = user.profile
	
	if request.method == 'POST':
		form = UpdateProfileForm(request.POST)
		
		if form.is_valid():
			user.first_name = form.cleaned_data['first_name']
			user.last_name = form.cleaned_data['last_name']
			user.email = form.cleaned_data['email']
			user.save()
			
			profile.first_name = form.cleaned_data['first_name']
			profile.last_name = form.cleaned_data['last_name']
			profile.dob = form.cleaned_data['date_of_birth']
			profile.phone_num = form.cleaned_data['phone_number']
			profile.profile_img = form.cleaned_data['profile_image']
			profile.save()
			
			return HttpResponseRedirect(reverse('dashboard'))

	else:
		form = UpdateProfileForm(initial={'first_name': profile.first_name,
										  'last_name': profile.last_name,
										  'email': user.email,
										  'date_of_birth': profile.dob,
										  'phone_number': profile.phone_num})

	return render(request, 'profile.html', {'form': form})


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
		context['today'] = datetime.datetime.now()
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


class ProcessedComment:
	# initialize with a Comment var
	def __init__(self, comment, depth=0):
		self.id = comment.id
		self.author = comment.author
		self.text = comment.text
		self.time_stamp = comment.time_stamp
		self.replies = []
		self.depth = depth
		
	# Unravels child comments and threads, running recursively and returning a list of ordered comments. Sets depth for each. 
	def unravel(self):
		ordered = [self]
		for comment in self.replies:
			comment.depth = self.depth + 1
			ordered += comment.unravel()
		return ordered
		
	def get_padding(self):
		return self.depth * 30
		
	def __repr__(self):
		return 'ProcessedComment(id="{}", author="{}", text="{}", time_stamp="{}". {} replies'.format(self.id, self.author, self.text, self.time_stamp, len(self.replies))


def trip_comments(request, pk):
	""" 
	Manages comments for a trip of given id (/trip/<id>/comments). Only available via AJAX on properly authenticated users.
	GET: Renders HTML comment section for given trip
	POST: Creates the added comment. Requires a 'text' field storing the text body of the comment and a 'parent' field storing the id of the comment the new comment is replying to (0 if none). Returns 'success': boolean and 'message': string (will be empty if success=True) 
	"""
	if request.method == 'GET':
		print ('Retrieving comments for trip id {}'.format(pk))
		# TODO: CHECK IF TRIP IS IN DATABASE
		
		# map id->ProcessedComment
		processed_comments = {}
		# top-level comments
		top_level_comments = []
		
		# retrieve comments on given trip in order of posting
		trip_comments = Comment.objects.filter(trip_id=pk).order_by('time_stamp')

		for comment in trip_comments:
			# create ProcessedComment wrapper and add to dictionary
			processed = ProcessedComment(comment)
			processed_comments[comment.id] = processed
			
			if comment.parent:
				# add comment as reply to parent
				processed_comments[comment.parent.id].replies.append(processed)
			else:
				# comment must be top-level
				top_level_comments.append(processed)
				
		# unravel top-level comments, creating list of ordered ProcessedComments
		ordered_comments = []
		for processed_comment in top_level_comments:
			ordered_comments += processed_comment.unravel()
			
		return render(
			request,
			'trip_comments.html',
			context={'comments': ordered_comments}
		)
		#return JsonResponse(data, safe=False)
	elif request.method == 'POST' and request.user.is_authenticated: # and request.is_ajax()
		print('Saving new comment by {}'.format(request.user.profile))
		# TODO: COULD BE A VULNERABILITY (NOT ENOUGH DATA VALIDATION)
		
		# create Comment object and save to database
		Comment(author=UserProfile.objects.get(pk=request.user.profile.id), parent=Comment.objects.get(pk=request.POST['parent']), text=request.POST['text'], trip=Trip.objects.get(pk=pk)).save()
		
		return JsonResponse({'success': True})
		#return HttpResponse({'success': True}, content_type="application/json")
	else:
		raise Http404('Access Denied')


def notifications(request):
	"""
	AJAX handler managing currently signed in user's notifications. Only accessible via AJAX requests. Returns rendered HTML of user's notifications, for insertion into the navbar on GET. POST accepts 'dismissed': <int:id> as the id of the notification the user has dismissed. 
	"""
	if request.method == 'GET':
		print ('retrieving notifications for user {}'.format(request.user.id))
		print ('Found {}'.format(Notification.objects.filter(recipient_id=request.user.profile.id).order_by('time_stamp').all()))
		return render(
			request,
			'notifications.html',
			context={'notifications': Notification.objects.filter(recipient_id=request.user.profile.id).order_by('time_stamp')}
		)
	elif request.method == 'POST':
		print ('Received {}'.format(request.POST))
		return JsonResponse({'success': True})
	else:
		raise Http404('Access Denied')
		
		
def trip_planner(request):
	"""
	View function for home page of site.
	"""
	return render(
		request,
		'trip_planner.html',
		context={'profiles': [UserProfile.objects.all()]}
	)


def admin_management(request):
	"""
	View function for home page of site.
	"""
	# Generate counts of some of the main objects
	num_users=UserProfile.objects.all().count()
	num_admins=UserProfile.objects.filter(admin_level__exact='a').count()
	names_list=UserProfile.objects.all()

	return render(
		request,
		'admin_management.html',
		context={'names_list':names_list,'num_users':num_users, 'num_admins': num_admins}
	)


def waiver(request):
	return render(
		request,
		'waiver.html',
		context={}
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
	template_name = 'umoc/trip_form.html'

	def get(self, request):
		form = AdminTripForm()
		args = {'form': form}
		return render(request, self.template_name, args)

	def post(self, request):
		if request.method == 'POST':
			print("this is a post")
			print(request.POST)
			form = AdminTripForm(request.POST)
			print(form.errors)
			if form.is_valid():
				print("this is valid")
				text = form.cleaned_data['post']
				name = request.POST.get('name')
				description = request.POST.get('description')
				form.save()
				print(text)
				print(name)
				print(description)
				return HttpResponseRedirect(reverse('dashboard'))
		else:
			print("failed. this is not a post")
			form = AdminTripForm()

		args = {'form': form}
		return render(request, self.template_name, args)


class TripUpdate(UpdateView):
	model = Trip
	fields = ['name','description','num_seats','capacity', 'thumbnail','start_time', 'end_time']#, 'cancelled', 'tag', 'leader', 'participants', 'drivers']


class TripDelete(DeleteView):
	model = Trip
	success_url = reverse_lazy('dashboard')
