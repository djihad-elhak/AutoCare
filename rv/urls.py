from django.urls import path
from . import views
from django.urls import path,include
from .views import RegisterAPIView, LoginAPIView,UserView,LogoutView,change_password,PasswordResetRequestView,PasswordResetView, BookinghistoryView,MessageFormView





urlpatterns = [
    path('', views.home, name='home-page'),

    path('api/client-booking/', views.BookingFormView.as_view(), name='booking_form_view'),
        path('api/message_form/', views.MessageFormView.as_view(), name='Message_form'),



    path('api/car-brands/', views.CarBrandListAPIView.as_view(), name='CarBrandListAPIView'),
    path('api/services/<int:brand_id>/', views.ServiceListAPIView.as_view(), name='ServiceListAPIView'),
    path('api/unavailable_dates/', views.UnavailableDateAPIView.as_view(), name='UnavailableDateAPIView'),


  path('register/', RegisterAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('user/', UserView.as_view(), name='user'),
    path('logout/', LogoutView.as_view(), name='logout'),




 




    path('api/staff/login/', views.staff_login_api.as_view(), name='staff_login_api'),



        path('api/staff-dashboard/', views.staff_dashboard_api.as_view(), name='staff_dashboard_api'),





        path('api/carfixed/<int:booking_id>/', views.car_fixed_api, name='car_fixed_api'),


        path('api/bookings/<int:booking_id>/car-did-not-arrive/', views.car_did_not_arrive_api, name='car_did_not_arrive_api'),


        path('api/bookings/<int:booking_id>/car-arrived/', views.car_arrived_api, name='car_arrived_api'),


         path('api/staff/history/', views.staff_history_api.as_view(), name='staff-history'),
    path('api/staff/data/', views.staff_data.as_view(), name='staff-data'),


      path('api/booking/<int:booking_id>/irreparable/', views.car_irreparable_api, name='car_irreparable_api'),






  path('change_password/', change_password, name='change_password'),
    path('password-reset-request/', PasswordResetRequestView.as_view(), name='password_reset_request'),
    path('password-reset/', PasswordResetView.as_view(), name='password_reset'),
path('Bookinghistory/', BookinghistoryView.as_view(), name='BookinghistoryView'),










     




]
