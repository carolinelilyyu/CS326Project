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

from datetime import datetime, timezone
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
			
			# create and save corresponding user profile
			userpro = UserProfile(user=user, first_name = form.cleaned_data.get('first_name'), last_name = form.cleaned_data.get('last_name'))
			userpro.save()
			
			# create a welcome notification
			Notification(recipient=userpro, message='Welcome to UMOC! Click here to fill out your profile', link=reverse('profile')).save()
			
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
		form = UpdateProfileForm(request.POST, request.FILES)
		
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


def dashboard(request):
	""" 
	Renders page with menu of upcoming trips, in order of start time.
	"""
	# filter trips by those starting after current time, and order by start time
	return render(request, 'dashboard.html', {'trips': Trip.objects.filter(start_time__gte=datetime.datetime.now(timezone.utc)).order_by('start_time')})

		
def trip_info(request, pk):
	"""
	Info page for a trip. Allows users to sign up, withdraw, and comment. Trip's leader and admins can edit or cancel the trip.
	"""
	try:
		return render(
			request,
			'trip_info.html',
			context={'trip': Trip.objects.get(pk=pk)}
		)
	except Trip.DoesNotExist:
		raise Http404('Sorry! That trip does not exist')

	
def public_profile(request, pk):
	try:
		return render(
			request,
			'public_profile.html',
			context={'profile': UserProfile.objects.get(pk=pk)}
		)
	except UserProfile.DoesNotExist:
		raise Http404("UserProfile does not exist")


class ProcessedComment:
	# initialize with a Comment var
	def __init__(self, comment, parent=None, depth=0):
		self.id = comment.id
		self.author = comment.author
		self.text = comment.text
		self.time_stamp = comment.time_stamp
		self.href = comment.author.get_absolute_url()
		self.replies = []
		self.parent = parent
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
			print (processed.href)
			processed_comments[comment.id] = processed
			
			if comment.parent:
				# set comment's parent and add comment as reply to parent
				processed.parent = processed_comments[comment.parent.id]
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
		
		# retrieve relevant database records
		author = UserProfile.objects.get(pk=request.user.profile.id)
		parent_comment = Comment.objects.get(pk=request.POST['parent'])
		trip = Trip.objects.get(pk=pk)
		
		# create Comment object and save to database
		comment = Comment(author=author, parent=parent_comment, text=request.POST['text'], trip=trip)
		comment.save()
		
		# create Notification for comment's parent if one exists and author is not equal to current signed-in user
		if parent_comment.author.id != request.user.profile.id:
			Notification(recipient=parent_comment.author, message='{} {} replied to your comment'.format(parent_comment.author.first_name, parent_comment.author.last_name), link=comment.get_absolute_url()).save()
		
		return JsonResponse({'success': True})
		#return HttpResponse({'success': True}, content_type="application/json")
	else:
		raise Http404('Access Denied')


def notifications(request):
	"""
	AJAX handler managing currently signed in user's notifications. Only accessible via AJAX requests. Returns rendered HTML of user's notifications, for insertion into the navbar on GET. POST accepts 'dismissed_id': <int:id> as the id of the notification the user has dismissed. 
	"""
	if request.method == 'GET':
		print ('Retrieving notifications for user {}'.format(request.user.id))
		return render(
			request,
			'notifications.html',
			context={'notifications': Notification.objects.filter(recipient_id=request.user.profile.id, dismissed=False).order_by('-time_stamp')}
		)
	elif request.method == 'POST':
		print ('Received request to dismiss notification {}'.format(request.POST))
		requested = Notification.objects.get(pk=request.POST['dismissed_id'])
		print (requested)
		requested.dismissed = True
		requested.save()
		print (requested)
		return JsonResponse({'success': True})
	else:
		raise Http404('Access Denied')
		

def admin_management(request):
	"""
	Allows an administrator to set user permission levels. IMPORTANT: This must only be accessible by admins. admin_edit is used to make AJAX calls to receive and update specific user data.
	"""
	if request.user.profile.admin_level != 'a':
		raise Http404('You do not have access to this page')
	else:
		return render(
			request,
			'admin_management.html',
			context={'users': UserProfile.objects.all().order_by('last_name')}
		)


def admin_edit(request):
	"""
	Manages AJAX calls for the admin page. IMPORTANT: This must only be accessible by admins. Run AJAX GET 'user_id': <id> to retrieve JSON data for a specific user. Run AJAX POST 'user_id': <id>, 'admin_level': <a/l/u> to set admin level for the specified user.
	"""
	if request.user.profile.admin_level != 'a':
		raise Http404('You do not have access to this page')
	elif request.method == 'GET':
		print ('Received GET {}'.format(request.GET))
		try:
			user = UserProfile.objects.get(pk=request.GET['user_id'])
			return JsonResponse({'first_name': user.first_name, 'last_name': user.last_name, 'href': user.get_absolute_url(), 'email': '', 'admin_level': user.admin_level })
		except UserProfile.DoesNotExist:
			return JsonResponse({'success': False})  # todo: return error
	elif request.method == 'POST':
		print ('Received POST {}'.format(request.POST))
		return JsonResponse({'success': True})
	else:
		raise Http404("This url is not being used correctly")
		
		
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
		context = super(AdminTripPlanner, self).get_context_data(**kwargs)
		context['profiles'] = [UserProfile.objects.all()]
		return context


class TripCreate(CreateView):
	model = Trip
	fields = ['name', 'description', 'capacity', 'start_time', 'end_time', 'tag']
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


def cancel_trip(request, pk):
	""" 
	Cancels trip of the given id. Requires requesting user to be trip leader or an admin. Returns 404 if the trip is over or has already been canceled. Creates notification for each user who had been signed up to participate.
	"""
	try:
		trip = Trip.objects.get(pk=pk)
		if trip.is_over():
			raise Http404("You can't cancel a trip that is over")
		elif request.user.profile.admin_level != 'a' and request.user.profile != trip.leader:
			raise Http404("You do not have permission")
		else:  # success
			trip.cancelled = True
			trip.save()
			
			# create notifications
			for participant in trip.participants.all():
				Notification(recipient=participant, message='{} was cancelled'.format(trip.name), link=trip.get_absolute_url()).save()
				
			return redirect('trip_info', pk=pk)
	except Trip.DoesNotExist:
		raise Http404('Sorry, that trip does not exist')

def join_trip(request, pk):
	"""
	Adds user to specified trip. Trip must exist and have capacity for another user, and user must not already be signed up. Returns 404 if this is not the case (it shouldn't be). Sends user a notification and reloads trip page on success. 
	"""
	try:
		trip = Trip.objects.get(pk=pk)
		if trip.is_over():
			raise Http404("You can't join a trip that is over")
		elif request.user.profile in trip.participants.all():
			raise Http404('You are already signed up!')
		elif not trip.num_seats:
			raise Http404('This trip is full')
		else:  # success
			trip.participants.add(request.user.profile)
			trip.num_seats -= 1
			trip.save()
			
			# create notification
			Notification(recipient=request.user.profile, message='You joined {} successfully!'.format(trip.name), link=trip.get_absolute_url()).save()
			
			return redirect('trip_info', pk=pk)
	except Trip.DoesNotExist:
		raise Http404('Sorry, that trip does not exist')
	
	
def leave_trip(request, pk):
	"""
	Removes user from specified trip. Trip must exist and have capacity for another user, and user must not already be signed up. Returns 404 if this is not the case (it shouldn't be). Reloads trip page on success.
	"""
	try:
		trip = Trip.objects.get(pk=pk)
		if trip.is_over():
			raise Http404("You can't leave a trip that is over")
		elif request.user.profile not in trip.participants.all():
			raise Http404("You aren't signed up for this trip")
		elif request.user.profile == trip.leader:
			raise Http404("You're the leader, you can't leave! You must cancel the trip or have an admin switch you out.")
		else:  # success
			trip.participants.remove(request.user.profile)
			trip.num_seats += 1
			trip.save()
			return redirect('trip_info', pk=pk)
	except Trip.DoesNotExist:
		raise Http404('Sorry, that trip does not exist')
		

def trip_report(request, pk):
	"""
	Generates a report on the given trip: Includes signed up users, with emergency information, along with other things. Only accessible for the trip leader, and any admins. Returns 404 if this is not the case.
	"""
	try:
		trip = Trip.objects.get(pk=pk)
		if request.user.profile.admin_level != 'a' and request.user.profile != trip.leader:
			raise Http404("You do not have permission to view this page.")
		else:  # success
			return render(request, 'trip_report.html', context={'trip': trip})
	except Trip.DoesNotExist:
		raise Http404('Sorry, that trip does not exist')