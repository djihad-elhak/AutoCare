from django.db import models
from django.contrib.auth.models import User, AbstractUser, Group,Permission
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.conf import settings
from django.utils.translation import gettext as _
from django.utils import timezone


from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.template.loader import render_to_string







class Users(AbstractUser):
    email = models.EmailField(unique=True)  
    password = models.CharField(max_length=128)  
   
    # USERNAME_FIELD = 'email'
    REQUIRED_FIELDS =[]
    groups = models.ManyToManyField(Group, related_name='logsig_users')
    user_permissions = models.ManyToManyField(Permission, related_name='logsig_users_permissions')

    def get_bookings(self):
        user = self
        
        return Booking.objects.filter(user=user)

# Create your models here.



from django.db import models
from .models import User
from django.utils import timezone
import uuid

class PasswordResetToken(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    token = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def __str__(self):
        return f"{self.user} - {self.token}"
    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = timezone.now() + timezone.timedelta(hours=1)
        super().save(*args, **kwargs)
















class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class CarBrand(models.Model):
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='car_brand_logos/', default='car.jpg')  

    def __str__(self):
        return self.name
    
class UnavailableDate(models.Model):
    date = models.DateField()

    def __str__(self):
        return f"{self.date}"


class Date(models.Model):
    date = models.DateField(unique=True)
    booking_count = models.IntegerField(default=0)
    is_full = models.BooleanField(default=False)


    def __str__(self):
        return str(self.date)



class Service(models.Model):
    brand = models.ForeignKey(CarBrand, on_delete=models.CASCADE,null=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name



class Booking(models.Model):
    car_brand = models.ForeignKey(CarBrand, on_delete=models.CASCADE, default=1)
    car_model = models.CharField(max_length=15 ,default='car model' )
    services = models.ManyToManyField(Service)  # Change this line
    booking_date = models.DateField()
    phone_number = models.CharField(max_length=15)  # Add phone_number field
    first_name = models.CharField(max_length=50, default='fname')  # Add first_name field
    last_name = models.CharField(max_length=50, default='lnmae')  # Add last_name field
    car_plate_number = models.CharField(max_length=20, default='car plate number')  # Add car_plate_number field
    user = models.ForeignKey(Users, on_delete=models.CASCADE, default=1)  # Save the user object
    email = models.EmailField(default='example@example.com')  # Save the email
    description = models.CharField(max_length=100, default='description')


    ARRIVAL_CHOICES = [
        ('ARRIVED', 'Arrived'),
        ('NOT_ARRIVED', 'Not arrived'),
        ('NOT_YET', 'Not yet')
    ]
    arrival_status = models.CharField(max_length=20, choices=ARRIVAL_CHOICES, default='NOT_YET')

    REPAIR_CHOICES = [
        ('REPAIRABLE', 'Repairable'),
        ('IRREPAIRABLE', 'Irreparable'),
        ('NOT_YET', 'Not yet')
    ]
    repair_status = models.CharField(max_length=20, choices=REPAIR_CHOICES, default='NOT_YET')





    def __str__(self):
        return self.first_name + " " + str(self.car_model)

    def clean(self):
        # Perform validation for phone number
        if self.phone_number and (not self.phone_number.isdigit() or len(self.phone_number) != 10):
            raise ValidationError("Phone number must be a 10-digit number.")

  





    




from django.contrib.auth.models import Group

class Team(Group):
    car_brand = models.ForeignKey(CarBrand, on_delete=models.CASCADE, default=1)

    class Meta:
        verbose_name = 'Team'
        verbose_name_plural = 'Teams'






    

class Staff(AbstractUser):
    
    first_name = models.CharField(max_length=50, default='fname')  # Add first_name field
    last_name = models.CharField(max_length=50, default='lnmae')  # Add last_name field
    password = models.CharField(max_length=128)  
    team = models.ManyToManyField(Team,  related_name='staff_members')
    REQUIRED_FIELDS =[]
    user_permissions = models.ManyToManyField(Permission, related_name='logsig_staff_permissions')
    
    class Meta:
        db_table = 'staff'

    # Specify unique related_name for groups field
    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        help_text=_('The groups this user belongs to.'),
        related_name='staff_groups'  # Unique related_name for rv.Staff.groups
    )


    def __str__(self):
        return self.first_name + ' ' + self.last_name
    


    def get_bookings(self):
        team = self.team.first()
        
        return Booking.objects.filter(car_brand=team.car_brand)


    
class BookingHistory(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, default=1)  # Save the user object
    car_brand = models.ForeignKey(CarBrand, on_delete=models.CASCADE, default=1)
    car_model = models.CharField(max_length=15 ,default='car model' )
    services = models.ManyToManyField(Service)  # Change this line
    booking_date = models.DateField()
    phone_number = models.CharField(max_length=15)  # Add phone_number field
    first_name = models.CharField(max_length=50, default='fname')  # Add first_name field
    last_name = models.CharField(max_length=50, default='lnmae')  # Add last_name field
    car_plate_number = models.CharField(max_length=20, default='car plate number')  # Add car_plate_number field
    user = models.ForeignKey(Users, on_delete=models.CASCADE, default=1)  # Save the user object
    email = models.EmailField(default='example@example.com')  # Save the email


    ARRIVAL_CHOICES = [
        ('ARRIVED', 'Arrived'),
        ('NOT_ARRIVED', 'Not arrived'),
        ('NOT_YET', 'Not yet')
    ]
    arrival_status = models.CharField(max_length=20, choices=ARRIVAL_CHOICES, default='NOT_YET')

    REPAIR_CHOICES = [
        ('REPAIRABLE', 'Repairable'),
        ('IRREPAIRABLE', 'Irreparable'),
        ('NOT_YET', 'Not yet')
    ]
    repair_status = models.CharField(max_length=20, choices=REPAIR_CHOICES, default='NOT_YET')





    def __str__(self):
        return self.first_name + " " + str(self.car_model)

    def clean(self):
        # Perform validation for phone number
        if self.phone_number and (not self.phone_number.isdigit() or len(self.phone_number) != 10):
            raise ValidationError("Phone number must be a 10-digit number.")

  





class Message(models.Model):
    email = models.EmailField()
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    reply_content = models.TextField(blank=True, null=True)  # New field for reply content



    def __str__(self):
        return f"Message from {self.email} at {self.created_at}"
    