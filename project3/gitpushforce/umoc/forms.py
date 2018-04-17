from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class RegisterForm(UserCreationForm):
	first_name = forms.CharField(max_length=30, help_text='Required - Please enter your first name.')
	last_name = forms.CharField(max_length=30, help_text='Required - Please enter your last name.')
	email = forms.EmailField(max_length=150, help_text='Required. Please enter your email address.')
	email_confirm = forms.EmailField(max_length=150, help_text='Required. Please confirm your email address.')

	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'email', 'email_confirm', 'password1', 'password2')


class AdminTripForm(forms.Form):

	name = forms.CharField(max_length=20, help_text='Enter Trip Name')
	description = forms.CharField(help_text='Enter description and informatin for trip')
	num_seats = forms.IntegerField(help_text='Enter number of seats available for the trip')
	capacity = forms.IntegerField(help_text='Enter number of seats available for the trip')
	thumbnail = forms.ImageField(help_text='Upload an image to show alongside this trip')
	start_time = forms.DateTimeField(help_text='Select Start Time of the Trip')
	end_time = forms.DateTimeField(help_text='Select End Time of the Trip')
	# # cancelled = forms.BooleanField(default=False, help_text='Click to Cancel')
	# # tag = forms.CharField(max_length=2, choices=TAG_CHOICES, blank=True, help_text='Select a tag to help classify this trip')
	# # leader = forms.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, help_text='Select a user to be in charge of organizing and leading this trip', verbose_name='Trip Leader/Organizer', related_name='trip_leader') # NOTE: NOT SURE IF ON_DELETE AND NULL ARE SET AS WE WANT
	# # participants = forms.ManyToManyField(UserProfile, help_text='Select users who are signed up to go on the trip', blank=True)
	# # drivers = forms.ManyToManyField(UserProfile, related_name='drivers', help_text='Users who have committed to driving', blank=True)


	class Meta:
		model = User
		fields = ('name', 'description', 'num_seats', 'capacity', 'thumbnail', 'start_time', 'end_time')