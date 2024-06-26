from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Booking, Date

@receiver(post_save, sender=Booking)
def update_full_date_on_booking_save(sender, instance, created, **kwargs):
    if created:
        booking_date = instance.booking_date
        date, _ = Date.objects.get_or_create(date=booking_date)
        date.booking_count += 1
        date.save()  # Save the changes to the Date model
        
@receiver(post_delete, sender=Booking)
def update_full_date_on_booking_delete(sender, instance, **kwargs):
    booking_date = instance.booking_date
    date, _ = Date.objects.get_or_create(date=booking_date)
    if date.booking_count > 0:
        date.booking_count -= 1
        date.save()  # Save the changes to the Date model
        
        if date.booking_count==0 :
            date.delete()
    