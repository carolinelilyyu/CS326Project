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