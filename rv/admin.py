from django.contrib import admin
from .models import  CarBrand, Service , Booking ,UnavailableDate ,Staff,Users,Team,BookingHistory,Message

admin.site.register((CarBrand))
admin.site.register((Service))
admin.site.register((Booking))
admin.site.register(UnavailableDate)
admin.site.register(Team)

admin.site.register(Staff)
admin.site.register(Users)

admin.site.register((BookingHistory))
class MessageAdmin(admin.ModelAdmin):
    list_display = ('email', 'content', 'created_at')
    readonly_fields = ('email', 'content', 'created_at')

    def has_add_permission(self, request):
        # Disable add
        return False

    def has_change_permission(self, request, obj=None):
        # Disable change
        return False

    

admin.site.register(Message, MessageAdmin)





