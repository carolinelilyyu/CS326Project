from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class RegisterForm(UserCreationForm):
	first_name = forms.CharField(max_length=30, help_text='Required - Please enter your first name.')
	last_name = forms.CharField(max_length=30, help_text='Required - Please enter your last name.')
	email = forms.EmailField(max_length=150, help_text='Required. Please enter your email address.')

	class Meta:
		model = User
		fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')


class AdminTripForm(forms.Form):

	name = forms.CharField(max_length=20, help_text='Enter Trip Name', error_messages={'required': 'Please enter your name'})
	description = forms.CharField(widget=forms.Textarea, help_text='Enter description and informatin for trip', error_messages={'required': 'Please enter your description'})
	num_seats = forms.IntegerField(help_text='Enter number of seats available for the trip', error_messages={'required': 'Please enter the number of seats'})
	capacity = forms.IntegerField(help_text='Enter number of seats available for the trip', error_messages={'required': 'Please enter the capacity'})
	thumbnail = forms.ImageField(help_text='Upload an image to show alongside this trip', error_messages={'required': 'Please enter a thumbnail picture'})
	start_time = forms.DateTimeField(help_text='Select Start Time of the Trip', error_messages={'required': 'Please enter a date'})
	end_time = forms.DateTimeField(help_text='Select End Time of the Trip', error_messages={'required': 'Please enter a date'})
	cancelled = forms.BooleanField(required=False, help_text='Click to Cancel', error_messages={'required': 'Please enter whether is cancelled or not'})
	tag = forms.CharField(help_text='Select a tag to help classify this trip', error_messages={'required': 'Please enter the tags'})
	leader = forms.ChoiceField(help_text='Select a user to be in charge of organizing and leading this trip', error_messages={'required': 'Please enter the leader\'s name'})
	participants = forms.MultipleChoiceField(help_text='Select users who are signed up to go on the trip', error_messages={'required': 'Please enter the participants\' names'})
	drivers = forms.MultipleChoiceField(help_text='Users who have committed to driving', error_messages={'required': 'Please enter the drivers'})


	# class Meta:
	# 	model = User
	# 	fields = ('name', 'description', 'num_seats', 'capacity', 'thumbnail', 'start_time', 'end_time', 'cancelled', 'tag', 'leader', 'participants', 'drivers')