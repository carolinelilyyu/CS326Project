from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from datetime import datetime, timezone

from umoc.models import Trip
from umoc.models import UserProfile

from django.forms import ModelForm


class RegisterForm(UserCreationForm):
	first_name = forms.CharField(max_length=30, help_text='Required. Please enter your first name.')
	last_name = forms.CharField(max_length=30, help_text='Required. Please enter your last name.')
	email = forms.EmailField(max_length=150, help_text='Required. Please enter your email address.', error_messages={'invalid': 'Please enter a valid email address.'})

	class Meta:
		model = User
		fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')


class AdminTripForm(ModelForm):
	OPTIONS = (
		('r', 'Rock Climbing'),
		('h', 'Hiking'),
		('s', 'Ski and Board'),
		('sk', 'Skiing'),
		('sn', 'Snowboarding'),
		('c', 'Cabin Trip'),
		)
	
	valid_dates= ['%Y-%m-%d %H:%M:%S',    # '2006-10-25 14:30:59'
				 '%Y-%m-%d %H:%M',       # '2006-10-25 14:30'
				 '%Y-%m-%d',             # '2006-10-25'
				 '%m/%d/%Y %H:%M:%S',    # '10/25/2006 14:30:59'
				 '%m/%d/%Y %H:%M',       # '10/25/2006 14:30'
				 '%m/%d/%Y',             # '10/25/2006'
				 '%m/%d/%y %H:%M:%S',    # '10/25/06 14:30:59'
				 '%m/%d/%y %H:%M',       # '10/25/06 14:30'
				 '%m/%d/%y']             # '10/25/06'
	
	choices = Trip.participants
	name = forms.CharField(max_length=20, help_text='Enter Trip Name', error_messages={'required': 'Please enter your name'})
	description = forms.CharField(widget=forms.Textarea, help_text='Enter description and informatin for trip', error_messages={'required': 'Please enter your description'})
	#num_seats = forms.IntegerField(help_text='Enter number of seats available for the trip', error_messages={'required': 'Please enter the number of seats'})
	capacity = forms.IntegerField(help_text='Enter number of seats available for the trip', error_messages={'required': 'Please enter the capacity'})
	#thumbnail = forms.ImageField(required=False,help_text='Upload an image to show alongside this trip', error_messages={'required': 'Please enter a thumbnail picture'})
	start_time = forms.DateTimeField(widget=forms.TextInput(attrs={'class':'datepicker'}), input_formats=['%Y-%m-%d %I:%M %p'], help_text='Select Start Date/Time of the Trip. Format: year-month-day hour:minute am/pm. Example: 2016-02-16 2:30 pm', error_messages={'required': 'Please enter a date'})
	end_time = forms.DateTimeField(input_formats=['%Y-%m-%d %I:%M %p'], help_text='Select End Date/Time of the Trip. Format: year-month-day hour:minute (use 24 hour clock). Example: 2016-02-16 3:30 pm', error_messages={'required': 'Please enter a date'})
	cancelled = forms.BooleanField(required=False, help_text='Click to Cancel', error_messages={'required': 'Please enter whether is cancelled or not'})
	tag = forms.ChoiceField(choices=OPTIONS, help_text='Select a tag to help classify this trip', error_messages={'required': 'Please enter the tags'})
	leader = forms.ModelChoiceField(queryset=UserProfile.objects.filter(admin_level='l'), help_text='Select a user to be in charge of organizing and leading this trip', error_messages={'required': 'Please enter the leader\'s name'})
	participants = forms.ModelMultipleChoiceField(queryset=UserProfile.objects.filter(admin_level='u'), help_text='Select users who are signed up to go on the trip', error_messages={'required': 'Please enter the participants\' names'})
	drivers = forms.ModelMultipleChoiceField(queryset=UserProfile.objects.filter(admin_level='u'), help_text='Users who have committed to driving. Drivers must also be participants', error_messages={'required': 'Please enter the drivers'})
	
	class Meta:
		model = Trip
		fields = ('name', 'description', 'num_seats', 'capacity', 'thumbnail', 'start_time', 'end_time', 'cancelled', 'tag', 'leader', 'participants', 'drivers')

class AdminUpdateTripForm(ModelForm):
	OPTIONS = (
		('r', 'Rock Climbing'),
		('h', 'Hiking'),
		('s', 'Ski and Board'),
		('sk', 'Skiing'),
		('sn', 'Snowboarding'),
		('c', 'Cabin Trip'),
		)
	
	valid_dates= ['%Y-%m-%d %H:%M:%S',    # '2006-10-25 14:30:59'
				 '%Y-%m-%d %H:%M',       # '2006-10-25 14:30'
				 '%Y-%m-%d',             # '2006-10-25'
				 '%m/%d/%Y %H:%M:%S',    # '10/25/2006 14:30:59'
				 '%m/%d/%Y %H:%M',       # '10/25/2006 14:30'
				 '%m/%d/%Y',             # '10/25/2006'
				 '%m/%d/%y %H:%M:%S',    # '10/25/06 14:30:59'
				 '%m/%d/%y %H:%M',       # '10/25/06 14:30'
				 '%m/%d/%y']             # '10/25/06'
	
	choices = Trip.participants
	name = forms.CharField(max_length=20, help_text='Enter Trip Name', error_messages={'required': 'Please enter your name'})
	description = forms.CharField(widget=forms.Textarea, help_text='Enter description and informatin for trip', error_messages={'required': 'Please enter your description'})
	num_seats = forms.IntegerField(help_text='Enter number of seats available for the trip', error_messages={'required': 'Please enter the number of seats'})
	capacity = forms.IntegerField(help_text='Enter number of seats available for the trip', error_messages={'required': 'Please enter the capacity'})
	thumbnail = forms.ImageField(required=False,help_text='Upload an image to show alongside this trip', error_messages={'required': 'Please enter a thumbnail picture'})
	start_time = forms.DateTimeField(input_formats=['%Y-%m-%d %I:%M %p'], help_text='Select Start Date/Time of the Trip. Format: year-month-day hour:minute am/pm. Example: 2016-02-16 2:30 pm', error_messages={'required': 'Please enter a date'})
	end_time = forms.DateTimeField(input_formats=['%Y-%m-%d %I:%M %p'], help_text='Select End Date/Time of the Trip. Format: year-month-day hour:minute (use 24 hour clock). Example: 2016-02-16 3:30 pm', error_messages={'required': 'Please enter a date'})
	cancelled = forms.BooleanField(required=False, help_text='Click to Cancel', error_messages={'required': 'Please enter whether is cancelled or not'})
	tag = forms.ChoiceField(choices=OPTIONS, help_text='Select a tag to help classify this trip', error_messages={'required': 'Please enter the tags'})
	leader = forms.ModelChoiceField(queryset=UserProfile.objects.filter(admin_level='l'), help_text='Select a user to be in charge of organizing and leading this trip', error_messages={'required': 'Please enter the leader\'s name'})
	participants = forms.ModelMultipleChoiceField(queryset=UserProfile.objects.filter(admin_level='u'), help_text='Select users who are signed up to go on the trip', error_messages={'required': 'Please enter the participants\' names'})
	drivers = forms.ModelMultipleChoiceField(queryset=UserProfile.objects.filter(admin_level='u'), help_text='Users who have committed to driving. Drivers must also be participants', error_messages={'required': 'Please enter the drivers'})
	
	class Meta:
		model = Trip
		fields = ('name', 'description', 'num_seats', 'capacity', 'thumbnail', 'start_time', 'end_time', 'cancelled', 'tag', 'leader', 'participants', 'drivers')


class UpdateProfileForm(forms.Form):
	first_name = forms.CharField(max_length=30, help_text='Required. Please enter your first name.')
	last_name = forms.CharField(max_length=30, help_text='Required. Please enter your last name.')
	email = forms.EmailField(max_length=150, help_text='Required. Please enter your email address.', error_messages={'invalid': 'Please enter a valid email address.'})
	date_of_birth = forms.DateField(help_text='Required. Please enter your date of birth (yyyy-mm-dd).')
	phone_number = forms.RegexField(regex=r'^\d{10}$', help_text='Required. Please enter your phone number (ten digits only).', error_messages={'invalid': 'Please enter a valid phone number.'})
	profile_image = forms.ImageField(required=False, help_text='Optional. Please select a new profile picture.')
	contact_name = forms.RegexField(regex=r'^[A-Z][a-z]+ [A-Z][a-z]+$', help_text='Required. Please enter your contact\'s first and last name.', error_messages={'invalid': 'Please enter a valid first and last name.'})
	contact_number = forms.RegexField(regex=r'^\d{10}$', help_text='Required. Please enter your contact\'s phone number (ten digits only).', error_messages={'invalid': 'Please enter a valid phone number.'})


class WaiverForm(forms.Form):
	first_name = forms.CharField(max_length=30, help_text='Required. Please enter your first name.')
	last_name = forms.CharField(max_length=30, help_text='Required. Please enter your last name.')
	current_date = forms.DateField(help_text='Required. Please enter the current date (yyyy-mm-dd).')

	def __init__(self, *args, **kwargs):
		self.profile = kwargs.pop('profile', None)
		super(WaiverForm, self).__init__(*args, **kwargs)
	
	def is_valid(self):
		valid = super(WaiverForm, self).is_valid()

		if not valid:
			return valid
		
		if not self.profile:
			self._errors['no_profile'] = 'The profile does not exist.'
			return False

		fname = self.cleaned_data.get('first_name')
		lname = self.cleaned_data.get('last_name')
		cdate = self.cleaned_data.get('current_date')
		
		if self.profile.first_name != fname or self.profile.last_name != lname or datetime.now().date() != cdate:
			if self.profile.first_name != fname:
				self.add_error('first_name', 'Please re-enter your first name.')
			if self.profile.last_name != lname:
				self.add_error('last_name', 'Please re-enter your last name.')
			if datetime.now().date() != cdate:
				self.add_error('current_date', 'Please re-enter the current date.')
			return False
		
		return True
