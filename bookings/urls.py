from django.urls import path
from . import views

app_name="bookings"

urlpatterns=[
    path("buy/<int:trip_id>/",views.buy_ticket,name="buy_ticket"),
    path('ticket-success/<int:ticket_id>/',views.ticket_success,name='ticket_success'),
]