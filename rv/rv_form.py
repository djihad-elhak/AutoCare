from django import forms
from .models import Booking


from django.contrib.auth.forms import AuthenticationForm

class StaffLoginForm(AuthenticationForm):
    # You can customize the login form if needed
    pass



class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['first_name', 'last_name', 'phone_number', 'car_plate_number','booking_date', 'car_brand', 'car_model','services']
