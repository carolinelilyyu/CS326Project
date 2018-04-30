from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from datetime import datetime, timezone

from umoc.models import Trip
from umoc.models import UserProfile


class RegisterForm(UserCreationForm):
	first_name = forms.CharField(max_length=30, help_text='Required. Please enter your first name.')
	last_name = forms.CharField(max_length=30, help_text='Required. Please enter your last name.')
	email = forms.EmailField(max_length=150, help_text='Required. Please enter your email address.', error_messages={'invalid': 'Please enter a valid email address.'})

	class Meta:
		model = User
		fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')


class AdminTripForm(ModelForm):	
	name = forms.CharField(max_length=20, help_text='Enter Trip Name', error_messages={'required': 'Please enter your name'})
	description = forms.CharField(widget=forms.Textarea, help_text='Enter description and informatin for trip', error_messages={'required': 'Please enter your description'})
	capacity = forms.IntegerField(help_text='Enter number of seats available for the trip', error_messages={'required': 'Please enter the capacity'})
	# thumbnail = forms.ImageField(required=False,help_text='Upload an image to show alongside this trip', error_messages={'required': 'Please enter a thumbnail picture'})
	start_time = forms.DateTimeField(input_formats=['%Y-%m-%d %I:%M %p'], help_text='Select Start Date/Time of the Trip. Format: year-month-day hour:minute am/pm. Example: 2019-02-16 2:30 pm', error_messages={'required': 'Please enter a date'})
	end_time = forms.DateTimeField(input_formats=['%Y-%m-%d %I:%M %p'], help_text='Select End Date/Time of the Trip. Format: year-month-day hour:minute am/pm. Example: 2019-02-16 3:30 pm', error_messages={'required': 'Please enter a date'})
	leader = forms.ModelChoiceField(queryset=UserProfile.objects.filter(admin_level='l'), help_text='Select a user to be in charge of organizing and leading this trip', error_messages={'required': 'Please enter the leader\'s name'})
	
	class Meta:
		model = Trip
		fields = ('name', 'description', 'capacity', 'start_time', 'end_time', 'tag', 'leader')

class AdminUpdateTripForm(ModelForm):
	name = forms.CharField(max_length=20, help_text='Enter Trip Name', error_messages={'required': 'Please enter your name'})
	description = forms.CharField(widget=forms.Textarea, help_text='Enter description and informatin for trip', error_messages={'required': 'Please enter your description'})
	capacity = forms.IntegerField(help_text='Enter number of seats available for the trip', error_messages={'required': 'Please enter the capacity'})
	# thumbnail = forms.ImageField(required=False,help_text='Upload an image to show alongside this trip', error_messages={'required': 'Please enter a thumbnail picture'})
	start_time = forms.DateTimeField(input_formats=['%Y-%m-%d %I:%M %p'], help_text='Select Start Date/Time of the Trip. Format: year-month-day hour:minute am/pm. Example: 2019-02-16 2:30 pm', error_messages={'required': 'Please enter a date'})
	end_time = forms.DateTimeField(input_formats=['%Y-%m-%d %I:%M %p'], help_text='Select End Date/Time of the Trip. Format: year-month-day hour:minute am/pm. Example: 2019-02-16 3:30 pm', error_messages={'required': 'Please enter a date'})
	leader = forms.ModelChoiceField(queryset=UserProfile.objects.filter(admin_level='l'), help_text='Select a user to be in charge of organizing and leading this trip', error_messages={'required': 'Please enter the leader\'s name'})
	
	class Meta:
		model = Trip
		fields = ('name', 'description', 'capacity', 'start_time', 'end_time', 'tag', 'leader')
	
	def __init__(self, *args, **kwargs):
		self.trip = kwargs.pop('trip', None)
		super(AdminUpdateTripForm, self).__init__(*args, **kwargs)
	
	def is_valid(self):
		valid = super(AdminUpdateTripForm, self).is_valid()

		if not valid:
			return valid
		
		if not self.trip:
			self._errors['no_trip'] = 'The trip does not exist.'
			return False
		
		if self.trip.num_seats - self.trip.capacity + self.cleaned_data.get('capacity') < 0:
			self.add_error('capacity', 'Error. Please enter a new capacity that is larger than or equal to the number of participants.')
			return False
		
		return True


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
