from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from datetime import datetime, timezone


# used for validating phone numbers entered (9 digits)
phone_regex = RegexValidator(regex=r'\d{10}', message="Phone number must be 10 digits and entered in the format '##########'.")


# returns path to user profile photo (MEDIA_ROOT/profiles/<user_id>
def profile_directory_path(instance, filename):
	print ('Received instance {} and filename {}'.format(instance, filename))
	return 'profiles/{}'.format(instance.id)

# Allowed statuses for admin level
ADMIN_LEVELS = (
	('u', 'User'),
	('l', 'Leader'),
	('a', 'Admin'),
)
	
class UserProfile(models.Model): 
	"""
	Model representing a user of the website (UMOC club member). A user has first name, last name and date of birth, as well as a profile image and phone number.
	"""
	user = models.OneToOneField(User, related_name='profile', on_delete='models.SET_NULL')
	first_name = models.CharField(max_length=20, help_text='Enter your first name', verbose_name='First Name')
	last_name = models.CharField(max_length=20, help_text='Enter your last name', verbose_name='Last Name')
	dob = models.DateField(verbose_name='Date of Birth', help_text='Enter your birth date in the format "YYYY-MM-DD"', blank=True, null=True)
	# upload profile to MEDIA_ROOT/profiles/<user_id>
	profile_img = models.ImageField(verbose_name='Profile Image', upload_to=profile_directory_path, blank=True)
	phone_num = models.CharField(max_length=10, verbose_name='Phone Number', validators=[phone_regex], blank=True) 
	contact_name = models.CharField(max_length=40, help_text='Enter name of an emergency contact', blank=True)
	contact_phone = models.CharField(max_length=10, verbose_name='Contact Phone Number', help_text='Enter phone number for emergency contact', validators=[phone_regex], blank=True)
	# date of last club payment
	last_paid = models.DateField(blank=True, null=True, help_text='Date the last time the user paid (blank if never)')
	can_comment = models.BooleanField(help_text='Set whether user can leave comments on trips', default=True)
	can_join_trip = models.BooleanField(help_text='Allow user to sign up for trips?', default=False)
	admin_level = models.CharField(max_length=1, choices=ADMIN_LEVELS, default='u')

	class Meta:
		ordering = ['last_name', 'first_name', 'admin_level']	
    
	def __str__(self):
		return '{}, {}'.format(self.last_name, self.first_name)

	def __equals__(self, other): # TODO: LOOK UP BEST PRACTICE
		return other is not None and isinstance(other, self.__class__) and self.id == other.id
		
	# returns url to user's profile. Todo: change. No user profile pages
	def get_absolute_url(self):
		return reverse('public_profile', args=[str(self.id)])
		
	# returns path to user's profile image. In development.
	def get_profile_img_url(self):
		return 'http://localhost:8000/media/profiles/{}'.format(self.id)
		
		
class Trip(models.Model):
	""" 
	Represents a scheduled trip.
	"""
	name = models.CharField(max_length=40, help_text='Enter Trip Name')
	description = models.TextField(help_text='Enter description and informatin for trip')
	# TODO: DEPRECATE AND REMOVE THIS FIELD.
	num_seats = models.PositiveSmallIntegerField(verbose_name='Number of seats remaining', help_text='Enter number of seats available for the trip')
	capacity = models.PositiveSmallIntegerField(verbose_name='Total Trip Capacity', help_text='Enter number of seats available for the trip')
	thumbnail = models.ImageField(help_text='Upload an image to show alongside this trip')
	start_time = models.DateTimeField(help_text='Select Start Time of the Trip')
	end_time = models.DateTimeField(help_text='Select End Time of the Trip')
	cancelled = models.BooleanField(default=False, help_text='Click to Cancel')

	# Allowed Tags a trip can have: code - (name, color)
	TAGS = {
		'': ('', ''),  # shouldn't be necessary; currently a work-around
		'r': ('Rock Climbing', '#ffff66'),
		'h': ('Hiking', '#5080ef'),
		's': ('Ski and Board', '#00dfff'),
		'sk': ('Skiing', '#99b3ff'),
		'sn': ('Snowboarding', '#ff5050'),
		'c': ('Cabin Trip', '#e7e042'),
	}
	
	# Made for Django choice field
	TAG_CHOICES = (
		('r', 'Rock Climbing'),
		('h', 'Hiking'),
		('s', 'Ski and Board'),
		('sk', 'Skiing'),
		('sn', 'Snowboarding'),
		('c', 'Cabin Trip'),
	)
	
	tag = models.CharField(max_length=2, choices=TAG_CHOICES, blank=True, help_text='Select a tag to help classify this trip')
	leader = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, help_text='Select a user to be in charge of organizing and leading this trip', verbose_name='Trip Leader/Organizer', related_name='trip_leader') # NOTE: NOT SURE IF ON_DELETE AND NULL ARE SET AS WE WANT
	participants = models.ManyToManyField(UserProfile, help_text='Select users who are signed up to go on the trip', blank=True)
	drivers = models.ManyToManyField(UserProfile, related_name='drivers', help_text='Users who have committed to driving', blank=True)

	class Meta:
		ordering = ['-start_time']
		
	# return whether trip has already ended. Compares using UTC time.
	def is_over(self):
		return self.end_time < datetime.now(timezone.utc)
		
	# returns number of seats still open
	def get_seats_remaining(self):
		return self.capacity - len(self.participants.all())
		
	# return full tag name
	def get_tag_name(self):
		return self.TAGS[self.tag][0] if self.tag in self.TAGS else ''
		
	# return hex string of this Trip's tag
	def get_tag_color(self):
		return self.TAGS[self.tag][1] if self.tag in self.TAGS else ''
	
	# route to trip page
	def get_absolute_url(self):
		return reverse('trip_info', args=[str(self.id)])
    
	def __str__(self):
		return 'Trip "{}", running from {} to {}'.format(self.name, self.start_time, self.end_time)


class Comment(models.Model):
	""" 
	Represents a comment left by a user on a trip. Has an author (User), a timestamp, a parent comment if it is a reply (can be None), and the Trip it is commenting on.
	"""
	author = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True)
	parent = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True)
	text = models.CharField(max_length=280)
	time_stamp = models.DateTimeField(auto_now_add=True)
	trip = models.ForeignKey(Trip, on_delete=models.SET_NULL, null=True)
	
	# route to trip page comment is on
	def get_absolute_url(self):
		return reverse('trip_info', args=[str(self.trip.id)]) + '#comment-{}'.format(self.id)
    
	def __str__(self):
		return 'Comment by {} on trip {}. Replying to {} on {}'.format(self.author.first_name, self.trip.name, self.parent.author.first_name if self.parent else '', self.time_stamp)


class Notification(models.Model):
	""" 
	A Notification is sent to a user when something relevant to them occurs. Examples are: one of their comments gets a reply, one of their planned trips is canceled, their trip is coming up soon. A Notification simply stores a reference to the User, a message, a timestamp of when it was sent, and a bool (whether it has been seen yet). It can also include an optional url, which when clicked will direct the user to a relevant page.
	"""
	recipient = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True)
	message = models.TextField()
	seen = models.BooleanField(default=False)
	dismissed = models.BooleanField(default=False)
	link = models.URLField(max_length=100, blank=True)
	# auto_now_add defaults to a timestamp when object is first created
	time_stamp = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['time_stamp']
		
	def __str__(self):
		return 'Notification for {} on {}: "{}. Dismissed = {}"'.format(self.recipient.first_name, self.time_stamp, self.message, self.dismissed)