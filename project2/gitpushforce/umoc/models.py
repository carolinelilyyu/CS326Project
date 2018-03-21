from django.db import models
from django.urls import reverse

# Create your models here.


class User(models.Model): # TODO: CAN_COMMENT, CAN_JOIN_TRIP
	"""
	Model representing a user of the website (UMOC club member). Stores all 
	personal data.
	"""
	first_name = models.CharField(max_length=20, help_text='Enter your first name', verbose_name='First Name')
	last_name = models.CharField(max_length=20, help_text='Enter your last name', verbose_name='Last Name')
	dob = models.DateField(verbose_name='Date of Birth')
	email = models.EmailField(max_length=30, unique=True)
	password = models.CharField(max_length=20) # TODO: store safely using dedicated authentication 
	profile_img = models.ImageField(verbose_name='Profile Image')
	phone_num = models.CharField(max_length=10, verbose_name='Phone Number') # TODO: VALIDATION
	
	# Allowed statuses for admin level 
	ADMIN_LEVELS = (
		('u', 'User'),
		('l', 'Leader'),
		('a', 'Admin'),
	)
	admin_level = models.CharField(max_length=1, choices=ADMIN_LEVELS, default='u')

	#class Meta:
	#	ordering = ['last_name', 'first_name', 'admin_level']	
    
	def __str__(self):
		return '{}, {}'.format(self.last_name, self.first_name)
		

class Trip(models.Model):
	""" 
	Represents a scheduled trip.
	"""
	name = models.CharField(max_length=20)
	description = models.TextField()
	num_seats = models.PositiveSmallIntegerField()
	thumbnail = models.ImageField()
	start_time = models.DateTimeField()
	end_time = models.DateTimeField()
	cancelled = models.BooleanField(default=False)
	
	# Allowed Tags a trip can have
	TAGS = (
		('r', 'Rock Climbing'),
		('h', 'Hiking'),
		('s', 'Ski and Board'),
		('sk', 'Skiing'),
		('sn', 'Snowboarding'),
		('c', 'Cabin Trip'),
	)
	tag = models.CharField(max_length=2, choices=TAGS, blank=True)
	leader = models.ForeignKey(User, on_delete=models.SET_NULL, null=True) # NOTE: NOT SURE IF ON_DELETE AND NULL ARE SET AS WE WANT
	participants = models.ManyToManyField(User, help_text='Users going on the trip', related_name='trip_participants') # TODO: VALIDATE IT IS LESS THAN NUM_SEATS. Also, figure out if this works.
	

	class Meta:
		ordering = ['start_time']

	def get_absolute_url(self):
		"""
		returns the url to access a detail record for the trip
		"""
		return reverse('trip_info', args=[str(self.id)])
    
	def __str__(self):
		return 'Trip "{}", running from {} to {}'.format(self.name, self.start_time, self.end_time)

		
class Comment(models.Model):
	""" 
	Represents a comment left by a user on a trip. Has an author (User), a timestamp, a parent comment if it is a reply (can be None), and the Trip it is commenting on.
	"""
	author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
	parent = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True)
	text = models.CharField(default='', max_length=280)
	time_stamp = models.DateTimeField() # TODO: DEFAULT TO NOW
	trip = models.ForeignKey(Trip, on_delete=models.SET_NULL, null=True)
	
	#class Meta:
	#	ordering = ['trip.id']

	# returns url to trip
	def get_absolute_url(self):
		return reverse('trip_info', args=[str(self.trip.id)])
    
	def __str__(self):
		return 'Comment by {} on trip {}. Replying to {} on {}'.format(self.author.first_name, self.trip.name, self.parent.author.first_name if self.parent else '', self.time_stamp)
		

class Notification(models.Model):
	""" 
	A Notification is sent to a user when something relevant to them occurs. Examples are: one of their comments gets a reply, one of their planned trips is canceled, their trip is coming up soon. A Notification simply stores a reference to the User, a message, a timestamp of when it was sent, and a bool (whether it has been seen yet). It can also include an optional url, which when clicked will direct the user to a relevant page.
	"""
	recipient = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
	message = models.TextField()
	seen = models.BooleanField(default=False)
	link = models.URLField(max_length=100, blank=True)
	time_stamp = models.DateTimeField()