from django.db import models

# Create your models here.


class User(models.Model):
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
	ADMIN_STATUS = (
		('u', 'User'),
		('l', 'Leader'),
		('a', 'Admin'),
	)
	admin_level = models.CharField(max_length=1, choices=ADMIN_STATUS, default='u')

	class Meta:
		ordering = ['last_name', 'first_name', 'level']	
    
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
	tag = models.CharField(choices=TAGS, blank=True)
	leader = models.ForeignKey('User', on_delete=models.SET_NULL, null=True) # NOTE: NOT SURE IF ON_DELETE AND NULL ARE SET AS WE WANT
	participants = models.ManyToManyField(User, help_text='Users goign on the trip') # TODO: VALIDATE IT IS LESS THAN NUM_SEATS 
	
	class Meta:
		ordering = ['start_time']
		
	def __str__(self):
		return 'Trip "{}", running from {} to {}'.format(name, start_time, end_time)