# Generated by Django 2.0.2 on 2018-04-05 18:16

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import umoc.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('umoc', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(help_text='Enter your first name', max_length=20, verbose_name='First Name')),
                ('last_name', models.CharField(help_text='Enter your last name', max_length=20, verbose_name='Last Name')),
                ('dob', models.DateField(help_text='Enter your birth date in the format "YYYY-MM-DD"', verbose_name='Date of Birth')),
                ('profile_img', models.ImageField(upload_to=umoc.models.profile_directory_path, verbose_name='Profile Image')),
                ('phone_num', models.CharField(max_length=10, validators=[django.core.validators.RegexValidator(message="Phone number must be 10 digits and entered in the format '##########'.", regex='\\d{10}')], verbose_name='Phone Number')),
                ('contact_name', models.CharField(blank=True, help_text='Enter name of an emergency contact', max_length=40)),
                ('contact_phone', models.CharField(blank=True, help_text='Enter phone number for emergency contact', max_length=10, validators=[django.core.validators.RegexValidator(message="Phone number must be 10 digits and entered in the format '##########'.", regex='\\d{10}')], verbose_name='Contact Phone Number')),
                ('can_comment', models.BooleanField(default=True, help_text='Set whether user can leave comments on trips')),
                ('can_join_trip', models.BooleanField(default=False, help_text='Allow user to sign up for trips?')),
                ('admin_level', models.CharField(choices=[('u', 'User'), ('l', 'Leader'), ('a', 'Admin')], default='u', max_length=1)),
            ],
            options={
                'ordering': ['last_name', 'first_name', 'admin_level'],
            },
        ),
        migrations.AlterField(
            model_name='comment',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='notification',
            name='recipient',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='trip',
            name='leader',
            field=models.ForeignKey(help_text='Select a user to be in charge of organizing and leading this trip', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='trip_leader', to=settings.AUTH_USER_MODEL, verbose_name='Trip Leader/Organizer'),
        ),
        migrations.AlterField(
            model_name='trip',
            name='participants',
            field=models.ManyToManyField(help_text='Select users who are signed up to go on the trip', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='User',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='user',
            field=models.OneToOneField(on_delete='models.SET_NULL', related_name='profile', to=settings.AUTH_USER_MODEL),
        ),
    ]
