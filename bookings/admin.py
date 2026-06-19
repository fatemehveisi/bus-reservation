from django.contrib import admin
from .models import Booking,Ticket,Payment,Refund

admin.site.register(Booking)
admin.site.register(Ticket)
admin.site.register(Payment)
admin.site.register(Refund)
