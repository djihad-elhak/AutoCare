# serializers.py

from rest_framework import serializers
from .models import CarBrand, Service,Booking, UnavailableDate,Date,Users,Staff,BookingHistory,Message

from .models import User




class ChangePassword(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

class PasswordResetSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=6)
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match")
        return data



class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = Users
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True},
        }
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = self.Meta.model(**validated_data)
        if password is not None:
            user.set_password(password)
        user.save()
        return user



class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = ['first_name', 'last_name', 'username','team']
















class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingHistory
        fields = '__all__'


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id','brand', 'name']

class CarBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarBrand
        fields = ['id', 'name']



class BookSerializer(serializers.ModelSerializer):
    services = ServiceSerializer(many=True, read_only=True)
    car_brand=CarBrandSerializer(read_only=True)
    class Meta:
        model = Booking
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['user', 'email', 'first_name', 'last_name', 'phone_number', 'car_plate_number', 'booking_date', 'car_brand', 'car_model', 'services', "description"]





class UnavailableDateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnavailableDate
        fields = ['id','date']






class DateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Date
        fields = ['id','date']



class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'email', 'content', 'created_at','reply_content']
        read_only_fields = ['id', 'created_at']