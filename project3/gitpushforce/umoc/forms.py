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