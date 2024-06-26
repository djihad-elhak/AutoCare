from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.models import User
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils import timezone
from django.conf import settings
from django.contrib.sessions.models import Session
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed
from .models import CarBrand, Service, Booking, UnavailableDate, Date, Staff, BookingHistory,Users,Team,Message
from .serializers import CarBrandSerializer, ServiceSerializer, UnavailableDateSerializer, DateSerializer, BookSerializer, UserSerializer,StaffSerializer,HistorySerializer,MessageSerializer
import jwt
import datetime
from jwt.exceptions import DecodeError, ExpiredSignatureError
from.rv_form import BookingForm
import json

from jwt import decode  # Import the decode function from the jwt library


from rest_framework.exceptions import AuthenticationFailed
from rest_framework import status
from rest_framework.response import Response

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import  User
from rest_framework.authtoken.models import Token
from .serializers import UserSerializer
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings 
from .authenticated import JWTAuthentication
import jwt
from jwt import decode
import datetime
from jwt.exceptions import DecodeError, ExpiredSignatureError  # Import DecodeError and ExpiredSignatureError
from rest_framework import generics
from rest_framework.permissions import AllowAny
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .serializers import ChangePassword








@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])

def change_password(request):
  if request.method == 'POST':
        serializer = ChangePassword(data=request.data)
        if serializer.is_valid():
              user = request.user
              if user.check_password(serializer.data.get('old_password')):
                    user.set_password(serializer.data.get('new_password'))
                    user.save()
                    return Response({'message': 'Password changed successfully.'}, status=status.HTTP_200_OK)
              return Response({'error': 'Incorrect old password.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 #Create your views here.
class BookinghistoryView(APIView):
#   serializer_class = BookingSerializer
#    permission_classes = [IsAuthenticated]
#   def get_queryset(self):
#      return Booking.objects.filter(user=self.request.user).order_by('-date') 
    def get(self, request):
        token = request.headers.get('Authorization')
        print(token)
        if not token:
            return Response({'error': 'Authentication credentials were not provided'}, status=401)
        
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
            user_id = payload['id']
            print(user_id)
            user = Users.objects.get(pk=user_id)
        except jwt.ExpiredSignatureError:
            return Response({'error': 'user expired'}, status=401)
        except (jwt.DecodeError, jwt.InvalidTokenError):
            return Response({'error': 'Invalid token'}, status=401)
        except Staff.DoesNotExist:
            return Response({'error': 'user not found'}, status=404)
        bookings = user.get_bookings()
        serializer = BookSerializer(bookings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User
from django.core.mail import send_mail
from django.utils import timezone
from .models import PasswordResetToken
from .serializers import PasswordResetRequestSerializer, PasswordResetSerializer
from django.conf import settings

# users/views.py
from django.db import models
from django.conf import settings
from django.core.mail import send_mail, BadHeaderError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User
from django.utils import timezone
from .models import PasswordResetToken
from .serializers import PasswordResetRequestSerializer, PasswordResetSerializer
import random
import random

def generate_token():
    return ''.join(random.choices('0123456789', k=6))


class PasswordResetRequestView(APIView):
   
    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = Users.objects.get(email=email)
                token_value = generate_token()
                token = PasswordResetToken.objects.create(user=user,token=token_value)
               
                # Send email
                try:
                    
                    send_mail(
                          'Password Reset Request',
                         f'Use the following token to reset your password: {token.token}',
                         settings.DEFAULT_FROM_EMAIL,
                         [email],
                        
                    )
                    return Response({'message': 'Password reset link has been sent to your email.'}, status=status.HTTP_200_OK)
                except BadHeaderError:
                    return Response({'error': 'Invalid header found.'}, status=status.HTTP_400_BAD_REQUEST)
                except Exception as e:
                    return Response({'error': f'Failed to send email. {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            except Users.DoesNotExist:
                return Response({'error': 'User with this email does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetView(APIView):
    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            token = serializer.validated_data['token']
            new_password = serializer.validated_data['new_password']
            try:
                reset_token = PasswordResetToken.objects.get(token=token, expires_at__gte=timezone.now())
                user = reset_token.user
                user.set_password(new_password)
                user.save()
                reset_token.delete()  # Invalidate the token
                return Response({'message': 'Password has been reset successfully.'}, status=status.HTTP_200_OK)
            except PasswordResetToken.DoesNotExist:
                return Response({'error': 'Invalid or expired token.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)







class RegisterAPIView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data) 
       
        if serializer.is_valid(): 
            
                    
            serializer.save()  #
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # def get(self, request):
        # users = User.objects.all()
        # # serializer = UserSerializer(users, many=True)
        # return Response(serializer.data)

class LoginAPIView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        user_queryset = Users.objects.filter(username=username)
         
        if not user_queryset.exists():
            raise AuthenticationFailed('User not found')
    
        user = user_queryset.first()
        
        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password') 
        payload ={
          'id': user.id,
          'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=600),
          'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')
        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {'jwt': token}
        
        return response
class UserView(APIView):
    def get(self, request):
        token = request.headers.get('Authorization')
        if not token:
            raise AuthenticationFailed('Unauthenticated') 
        
        try:
            payload = decode(token, 'secret', algorithms=['HS256'])  # Decode the JWT token
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token expired') 
        
        user = Users.objects.filter(id=payload['id']).first()
        
        if not user:
            raise AuthenticationFailed('User not found')
        
        serializer = UserSerializer(user)
        
        return Response(serializer.data, status=status.HTTP_200_OK)



class LogoutView(APIView):
    def post(self, request):
        response =Response()
        response.delete_cookie('jwt')
        response.data = {
            'message' :'success'
        }
        return response




class staff_login_api(APIView):

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        user_queryset = Staff.objects.filter(username=username)
         
        if not user_queryset.exists():
            raise AuthenticationFailed('staff not found')
        passw = user_queryset.first().password
        user = user_queryset.first()
        
        if password!=passw:
            raise AuthenticationFailed('Incorrect password ') 
        print(user.id)
        payload ={
          'id': user.id,
          'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=1000000000),
          'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')
        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True , secure=True, samesite="None")
        response.data = {'jwt': token}
        staff_profile = user
        print("hahahahahahhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh")

        
        
        
        
        return response



@api_view(['POST'])
def car_fixed_api(request, booking_id):

    token = request.headers.get('Authorization')
    print(token)
    if not token:
        return Response({'error': 'Authentication credentials were not provided'}, status=401)
        
    try:
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        user_id = payload['id']
        staff = Staff.objects.get(pk=user_id)
    except jwt.ExpiredSignatureError:
        return Response({'error': 'Staff expired'}, status=401)
    except (jwt.DecodeError, jwt.InvalidTokenError):
        return Response({'error': 'Invalid token'}, status=401)
    except Staff.DoesNotExist:
        return Response({'error': 'Staff not found'}, status=404)


    # Get the booking object
    booking = get_object_or_404(Booking, id=booking_id)

    # Send email notification to the client
    html_message = render_to_string(
        'car_fixed_email.html',
        {
            'staff' : staff.first_name + " " + staff.last_name,
            'first_name': booking.first_name,
            'last_name': booking.last_name,
            'car_brand': booking.car_brand.name,
            'car_model': booking.car_model,
            # Add more booking data as needed
        }
    )
    subject = 'Your Car Is Fixed'
    from_email = settings.EMAIL_HOST_USER
    to_email = [booking.email]
    email = EmailMultiAlternatives(subject, strip_tags(html_message), from_email, to_email)
    email.attach_alternative(html_message, "text/html")
    email.send(fail_silently=False)

    # Create a booking history entry
    booking_history = BookingHistory(
        car_brand=booking.car_brand,
        car_model=booking.car_model,
        booking_date=booking.booking_date,
        phone_number=booking.phone_number,
        first_name=booking.first_name,
        last_name=booking.last_name,
        car_plate_number=booking.car_plate_number,  
        user=booking.user,
        email=booking.email,
        arrival_status=booking.arrival_status,
        repair_status='REPAIRABLE' , # Assuming the car is repairable
         staff=staff
        
    )
    booking_history.save()

    # Delete the original booking
    booking.delete()

    # Return success response
    return Response({"message": "Car fixed successfully"}, status=status.HTTP_200_OK)



@api_view(['POST'])
def car_irreparable_api(request, booking_id):
    """
    API endpoint to mark the car as irreparable and send an email notification.
    """
    token = request.headers.get('Authorization')
    print(token)
    if not token:
        return Response({'error': 'Authentication credentials were not provided'}, status=401)
        
    try:
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        user_id = payload['id']
        staff = Staff.objects.get(pk=user_id)
    except jwt.ExpiredSignatureError:
        return Response({'error': 'Staff expired'}, status=401)
    except (jwt.DecodeError, jwt.InvalidTokenError):
        return Response({'error': 'Invalid token'}, status=401)
    except Staff.DoesNotExist:
        return Response({'error': 'Staff not found'}, status=404)

    # Get the booking object
    booking = get_object_or_404(Booking, id=booking_id)

    # Send email notification to the client
    html_message = render_to_string(
        'car_irreparable_email.html',
        {
            'first_name': booking.first_name,
            'last_name': booking.last_name,
            'car_brand': booking.car_brand.name,
            'car_model': booking.car_model,
            # Add more booking data as needed
        }
    )
    subject = 'Car Is Irreparable'
    from_email = settings.EMAIL_HOST_USER
    to_email = [booking.email]
    email = EmailMultiAlternatives(subject, strip_tags(html_message), from_email, to_email)
    email.attach_alternative(html_message, "text/html")
    email.send(fail_silently=False)

    # Create a booking history entry
    booking_history = BookingHistory.objects.create(
        car_brand=booking.car_brand,
        car_model=booking.car_model,
        booking_date=booking.booking_date,
        phone_number=booking.phone_number,
        first_name=booking.first_name,
        last_name=booking.last_name,
        car_plate_number=booking.car_plate_number,
        user=booking.user,
        email=booking.email,
        arrival_status=booking.arrival_status,
        repair_status='IRREPAIRABLE',  # Marking the car as irreparable
        staff=staff  # Set the staff member
    )

    # Delete the booking
    booking.delete()

    # Return success response
    return Response({"message": "Car marked as irreparable and email sent successfully"}, status=status.HTTP_200_OK)



@api_view(['POST'])
def car_did_not_arrive_api(request, booking_id):
    """
    API endpoint to mark the car as not arrived and send an email notification.
    """
    token = request.headers.get('Authorization')
    print(token)
    if not token:
        return Response({'error': 'Authentication credentials were not provided'}, status=401)
        
    try:
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        user_id = payload['id']
        staff = Staff.objects.get(pk=user_id)
    except jwt.ExpiredSignatureError:
        return Response({'error': 'Staff expired'}, status=401)
    except (jwt.DecodeError, jwt.InvalidTokenError):
        return Response({'error': 'Invalid token'}, status=401)
    except Staff.DoesNotExist:
        return Response({'error': 'Staff not found'}, status=404)

    # Get the booking object
    booking = get_object_or_404(Booking, id=booking_id)

    # Send email notification to the client
    html_message = render_to_string(
        'booking_not_arrived_email.html',
        {
            'first_name': booking.first_name,
            'last_name': booking.last_name,
            'car_brand': booking.car_brand.name,
            'car_model': booking.car_model,
            # Add more booking data as needed
        }
    )
    subject = 'Car Did Not Arrive'
    from_email = settings.EMAIL_HOST_USER
    to_email = [booking.email]
    email = EmailMultiAlternatives(subject, strip_tags(html_message), from_email, to_email)
    email.attach_alternative(html_message, "text/html")
    email.send(fail_silently=False)

    # Create a booking history entry
    booking_history = BookingHistory.objects.create(
        car_brand=booking.car_brand,
        car_model=booking.car_model,
        booking_date=booking.booking_date,
        phone_number=booking.phone_number,
        first_name=booking.first_name,
        last_name=booking.last_name,
        car_plate_number=booking.car_plate_number,
        user=booking.user,
        email=booking.email,
        arrival_status='NOT_ARRIVED',  # Marking the car as not arrived
        repair_status='NOT_YET',  # Assuming the car repair status is not yet determined
        staff=staff  # Set the staff member
    )

    # Delete the booking
    booking.delete()

    # Return success response
    return Response({"message": "Car marked as not arrived and email sent successfully"}, status=status.HTTP_200_OK)



@api_view(['POST'])
def car_arrived_api(request, booking_id):
    """
    API endpoint to mark the car as not arrived and send an email notification.
    """
    token = request.headers.get('Authorization')
    print(token)
    if not token:
        return Response({'error': 'Authentication credentials were not provided'}, status=401)
        
    try:
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        user_id = payload['id']
        staff = Staff.objects.get(pk=user_id)
    except jwt.ExpiredSignatureError:
        return Response({'error': 'Staff expired'}, status=401)
    except (jwt.DecodeError, jwt.InvalidTokenError):
        return Response({'error': 'Invalid token'}, status=401)
    except Staff.DoesNotExist:
        return Response({'error': 'Staff not found'}, status=404)

    # Get the booking object
    booking = get_object_or_404(Booking, id=booking_id)

    # Send email notification to the client
    html_message = render_to_string(
        'booking_arrived_email.html',
        {
            'first_name': booking.first_name,
            'last_name': booking.last_name,
            'car_brand': booking.car_brand.name,
            'car_model': booking.car_model,
            # Add more booking data as needed
        }
    )
    subject = 'you car arrived '
    from_email = settings.EMAIL_HOST_USER
    to_email = [booking.email]
    email = EmailMultiAlternatives(subject, strip_tags(html_message), from_email, to_email)
    email.attach_alternative(html_message, "text/html")
    email.send(fail_silently=False)
    booking.arrival_status='ARRIVED'    

    booking.save()




    # Return success response
    return Response({"message": "Car marked as  arrived and email sent successfully"}, status=status.HTTP_200_OK)




class staff_dashboard_api(APIView):

    def get(self, request):
        token = request.headers.get('Authorization')
        print(token)
        if not token:
            return Response({'error': 'Authentication credentials were not provided'}, status=401)
        
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
            user_id = payload['id']
            print(user_id)
            staff = Staff.objects.get(pk=user_id)
        except jwt.ExpiredSignatureError:
            return Response({'error': 'Staff expired'}, status=401)
        except (jwt.DecodeError, jwt.InvalidTokenError):
            return Response({'error': 'Invalid token'}, status=401)
        except Staff.DoesNotExist:
            return Response({'error': 'Staff not found'}, status=404)
        bookings = staff.get_bookings()
        serializer = BookSerializer(bookings, many=True)





        team = staff.team.first()
        print(team)
        unarrived_bookings = Booking.objects.filter(
                car_brand=team.car_brand,

                    arrival_status='NOT_YET',
                    booking_date__lt=timezone.now() - timezone.timedelta(hours=24)
                )
        for booking in unarrived_bookings:
                    # Prepare email content
            html_message = render_to_string(
                        'booking_not_arrived_email.html',
                        {
                            'first_name': booking.first_name,
                            'last_name': booking.last_name,
                            'booking_id': booking.id,
                            'car_brand': booking.car_brand.name,
                            'car_model': booking.car_model,
                            'booking_date': booking.booking_date.strftime('%Y-%m-%d'),
                            # Add more booking data as needed
                        }
                    )
                    # Send email notification
            subject = 'Car Did Not Arrive'
            from_email = settings.EMAIL_HOST_USER
            to_email = [booking.email]
                    # Create and send the email
            email = EmailMultiAlternatives(subject, strip_tags(html_message), from_email, to_email)
            email.attach_alternative(html_message, "text/html")
            email.send(fail_silently=False)

            



            booking_history = BookingHistory.objects.create(
            car_brand=booking.car_brand,
            car_model=booking.car_model,
            booking_date=booking.booking_date,
            phone_number=booking.phone_number,
            first_name=booking.first_name,
            last_name=booking.last_name,
            car_plate_number=booking.car_plate_number,
            user=booking.user,
            email=booking.email,
            arrival_status='NOT_ARRIVED',  # Marking the car as not arrived
            repair_status='NOT_YET',  # Assuming the car repair status is not yet determined
            staff=staff  # Set the staff member
    )

            booking.delete()







        return Response(serializer.data, status=status.HTTP_200_OK)

        

class staff_history_api(APIView):

    def get(self, request):
        token = request.headers.get('Authorization')
        print(token)
        if not token:
            return Response({'error': 'Authentication credentials were not provided'}, status=401)
        
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
            user_id = payload['id']
            print(user_id)
            staff = Staff.objects.get(pk=user_id)
        except jwt.ExpiredSignatureError:
            return Response({'error': 'Staff expired'}, status=401)
        except (jwt.DecodeError, jwt.InvalidTokenError):
            return Response({'error': 'Invalid token'}, status=401)
        except Staff.DoesNotExist:
            return Response({'error': 'Staff not found'}, status=404)
        bookings=BookingHistory.objects.filter(staff=staff)

        serializer = HistorySerializer(bookings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class staff_data(APIView):

    def get(self, request):
        token = request.headers.get('Authorization')
        print(token)
        if not token:
            return Response({'error': 'Authentication credentials were not provided'}, status=401)
        
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
            user_id = payload['id']
            print(user_id)
            staff = Staff.objects.get(pk=user_id)
        except jwt.ExpiredSignatureError:
            return Response({'error': 'Staff expired'}, status=401)
        except (jwt.DecodeError, jwt.InvalidTokenError):
            return Response({'error': 'Invalid token'}, status=401)
        except Staff.DoesNotExist:
            return Response({'error': 'Staff not found'}, status=404)
        serializer = StaffSerializer(staff)
        return Response(serializer.data, status=status.HTTP_200_OK)
        




















from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.http import JsonResponse
from .serializers import BookingSerializer
from .models import Booking
import jwt
from django.conf import settings


class MessageFormView(APIView) :
        def post(self, request):
            serializer = MessageSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=201)
            return Response(serializer.errors, status=400)



class BookingFormView(APIView):
    def post(self, request):
        token = request.headers.get('Authorization')
        print(token)
        if not token:
            return Response({'error': 'Authentication credentials were not provided'}, status=401)
        
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
            user_id = payload['id']
            print(user_id)
            print(Users.objects.all())
            user = Users.objects.get(pk=user_id)
            print("cccccccccccccccccccccccccccccccccccccccccc")
            print(user)
            print(user.email)
        except jwt.ExpiredSignatureError:
            return Response({'error': 'Token expired'}, status=401)
        except (jwt.DecodeError, jwt.InvalidTokenError):
            return Response({'error': 'Invalid token'}, status=401)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=404)
        
        # Automatically fill in user and email
        request.data['user'] = user_id
        request.data['email'] = user.email
        serializer = BookingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)





























class CarBrandListAPIView(APIView):
    def get(self, request):
        car_brands = CarBrand.objects.all()
        serializer = CarBrandSerializer(car_brands, many=True)
        return Response(serializer.data)


class ServiceListAPIView(APIView):
    def get(self, request, brand_id):
        services = Service.objects.filter(brand_id=brand_id)
        serializer = ServiceSerializer(services, many=True)
        return Response(serializer.data)


class UnavailableDateAPIView(APIView):
    def get(self, request):
        dates =  UnavailableDate.objects.all()
        serializer1 = UnavailableDateSerializer(dates, many=True)

        dates2 =  Date.objects.filter(booking_count=4)
        serializer2 = DateSerializer(dates2, many=True)

        serializer1_data = serializer1.data
        serializer2_data = serializer2.data


        combined_data = serializer1_data + serializer2_data



        return Response(combined_data)
    











def home(request):
    services = Service.objects.all()
    carbrands = CarBrand.objects.all()
    return render(request, 'index.html', {'services': services, 'carbrands': carbrands})






