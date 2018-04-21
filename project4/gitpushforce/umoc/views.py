from django.urls import reverse
from django.views import generic
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from datetime import *
import json
from django import forms
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect, HttpResponse, Http404

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
		return render(
				request,
				'profile.html',
				context={},
		)

def get_matching_userprofile(user_inst):
	for p in UserProfile.objects.all():
			if str(p.user) == str(user_inst.username):
				return p


def profile2(request, pk):
	"""
	View function for profile page of site.
	"""
	model = UserProfile
	user_inst = get_object_or_404(User, pk = pk)
	#user_prof_inst = get_object_or_404(UserProfile, pk = pk)
	user_profile_inst = get_matching_userprofile(user_inst)
	
	# If this is a POST request then process the Form data
	if request.method == 'POST':

		# Create a form instance and populate it with data from the request (binding):
		form = UpdateProfileForm(request.POST)

		# Check if the form is valid:
		if form.is_valid():
			# process the data in form.cleaned_data as required (here we just write it to the model due_back field)
			user_inst.first_name = form.cleaned_data['first_name']
			user_inst.last_name = form.cleaned_data['last_name']
			user_inst.email = form.cleaned_data['email']
			user_inst.save()

			user_profile_inst.dob = form.cleaned_data['dob']
			user_profile_inst.phone_num = form.cleaned_data['phone_num']
			user_profile_inst.save()

			# redirect to a new URL:
			return HttpResponseRedirect(reverse('dashboard') )

	# If this is a GET (or any other method) create the default form.
	else:
		form = UpdateProfileForm(initial={'first_name': user_inst.first_name,
										  'last_name': user_inst.last_name,
										  'email': user_inst.email,
										  'dob': user_profile_inst.dob,
										  'phone_num': user_profile_inst.phone_num})

	return render(request, 'profile2.html', {'form': form, 'userinst':user_inst})

		# return render(
		#		 request,
		#		 'profile2.html',
		#		 context={},
		# )

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
		
		# retrieve comments on given trip in order of posting
		trip_comments = Comment.objects.filter(trip_id=pk).order_by('time_stamp')
		data = [{ 'id': comment.id, 'parent': comment.parent.id if comment.parent else 0, 'author_id': comment.author.id, 'author_name': '{} {}'.format(comment.author.first_name, comment.author.last_name), 'text': comment.text, 'timestamp': comment.time_stamp} for comment in trip_comments]
		
		# map id->ProcessedComment
		processed_comments = {}
		# top-level comments
		top_level_comments = []
		
		for comment in trip_comments:
			# create ProcessedComment wrapper and add to dictionary
			processed = ProcessedComment(comment)
			processed_comments[comment.id] = processed
			
			if comment.parent:
				# add comment as reply to parent
				print('Adding reply to parent')
				processed_comments[comment.parent.id].replies.append(processed)
			else:
				# comment must be top-level
				top_level_comments.append(processed)
				
		# unravel top-level comments, creating list of ordered ProcessedComments
		ordered_comments = []
		for processed_comment in top_level_comments:
			ordered_comments += processed_comment.unravel()
			
		print (ordered_comments)
		return render(
			request,
			'trip_comments.html',
			context={'comments': ordered_comments}
		)
		#return JsonResponse(data, safe=False)
	elif request.method == 'POST': # and request.is_ajax()
		print (request.POST)
		print ('Saving new comment')
		print (request.user)
		print (request.user.profile)
		if request.user.is_authenticated:
			print('Saving new comment by {}'.format(request.user.profile))
			print(request.POST['text'])
			print (UserProfile.objects.get(pk=request.user.profile.id))
			print(Comment.objects.get(pk=request.POST['parent']).parent)
			print(request.POST['text'])
			print(Trip.objects.get(pk=pk))
			# TODO: COULD BE A VULNERABILITY (NOT ENOUGH DATA VALIDATION)
			comment = Comment(author=UserProfile.objects.get(pk=request.user.profile.id), parent=Comment.objects.get(pk=request.POST['parent']), text=request.POST['text'], trip=Trip.objects.get(pk=pk))
			comment.save()
			
			#return JsonResponse({'success': True})
			return HttpResponse({'success': True}, content_type="application/json")
		else:
			return JsonResponse({'success': False}) # TODO: RETURN PERMISSION ERROR
	
	else:
		raise Http404('Access Denied')

			
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

		from django.contrib.auth.decorators import permission_required
