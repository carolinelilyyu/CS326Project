from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from umoc.models import Trip
from django.forms import ModelForm


class RegisterForm(UserCreationForm):
        first_name = forms.CharField(max_length=30, help_text='Required - Please enter your first name.')
        last_name = forms.CharField(max_length=30, help_text='Required - Please enter your last name.')
        email = forms.EmailField(max_length=150, help_text='Required. Please enter your email address.')

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
	num_seats = forms.IntegerField(help_text='Enter number of seats available for the trip', error_messages={'required': 'Please enter the number of seats'})
	capacity = forms.IntegerField(help_text='Enter number of seats available for the trip', error_messages={'required': 'Please enter the capacity'})
	thumbnail = forms.ImageField(help_text='Upload an image to show alongside this trip', error_messages={'required': 'Please enter a thumbnail picture'})
	start_time = forms.DateTimeField(input_formats=['%Y-%m-%d %I:%M %p'], help_text='Select Start Date/Time of the Trip. Format: year-month-date hour:minute (use 24 hour clock). Example: 2016-02-16 23:00', error_messages={'required': 'Please enter a date'})
	end_time = forms.DateTimeField(input_formats=['%Y-%m-%d %I:%M %p'], help_text='Select End Date/Time of the Trip. Format: year-month-date hour:minute (use 24 hour clock). Example: 2016-02-16 23:00', error_messages={'required': 'Please enter a date'})
	cancelled = forms.BooleanField(required=False, help_text='Click to Cancel', error_messages={'required': 'Please enter whether is cancelled or not'})
	tag = forms.ChoiceField(choices=OPTIONS, help_text='Select a tag to help classify this trip', error_messages={'required': 'Please enter the tags'})
	leader = forms.ModelChoiceField(queryset=Trip.objects.all(), help_text='Select a user to be in charge of organizing and leading this trip', error_messages={'required': 'Please enter the leader\'s name'})
	participants = forms.MultipleChoiceField(choices=OPTIONS, help_text='Select users who are signed up to go on the trip', error_messages={'required': 'Please enter the participants\' names'})
	drivers = forms.MultipleChoiceField(choices=OPTIONS, help_text='Users who have committed to driving', error_messages={'required': 'Please enter the drivers'})
	
	class Meta:
		model = Trip
		fields = ('name', 'description', 'num_seats', 'capacity', 'thumbnail', 'start_time', 'end_time', 'cancelled', 'tag', 'leader', 'participants', 'drivers')

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import datetime #for checking renewal date range.
    
class UpdateProfileForm(forms.Form):
    print("Update profile form")
    email = forms.EmailField()
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    dob = forms.DateField()
    phone_num = forms.RegexField(regex=r'^\+?1?\d{9,15}$')
    #spire_id = forms.RegexField(regex=r'\d{8}$', help_text = ("SPIRE ID must be 8 digits"))
