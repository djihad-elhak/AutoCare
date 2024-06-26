from django.apps import AppConfig

class YourAppNameConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'rv'

    def ready(self):
        from .signals import update_full_date_on_booking_save, update_full_date_on_booking_delete
        from .models import Booking
        from django.db.models.signals import post_save, post_delete



        # Connect signal handlers
        post_save.connect(update_full_date_on_booking_save, sender=Booking)
        post_delete.connect(update_full_date_on_booking_delete, sender=Booking)
