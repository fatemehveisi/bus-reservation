from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError

class Booking(models.Model):
    class Status(models.TextChoices):
        PENDING="PENDING","در انتظار پرداخت"
        PAID="PAID","پرداخت شده"
        CANCELED="CANCELED","لغو شده"
        REFUNDED="REFUNDED","مسترد شده"
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.PROTECT,related_name="bookings")
    trip=models.ForeignKey("trips.Trip",on_delete=models.PROTECT,related_name="bookings")
    status=models.CharField(max_length=20,choices=Status.choices,default=Status.PENDING)
    created_at=models.DateTimeField(auto_now_add=True)
    total_amount=models.PositiveIntegerField(default=0)
    def __str__(self):
        return f"Booking#{self.id}-{self.user}-{self.trip}"
#------------------------------------------------------
class Ticket(models.Model):
    booking=models.ForeignKey(Booking,on_delete=models.CASCADE,related_name="tickets")
    trip=models.ForeignKey("trips.Trip",on_delete=models.PROTECT,related_name="tickets")
    full_name=models.CharField(max_length=120)
    national_code=models.CharField(max_length=10)
    seat_number=models.PositiveSmallIntegerField()
    
    class Meta:
        constraints=[
            models.UniqueConstraint(fields=["trip","seat_number"],name="unique_seat_per_trip"),
            
        ]
#--------------------------------------------------
class Payment(models.Model):
    class Status(models.TextChoices):
        INITIATED="INITIATED","شروع شده"
        SUCCESS="SUCCESS","موفق"
        FAILED="FAILED","ناموفق"
    booking=models.OneToOneField(Booking,on_delete=models.CASCADE,related_name="payment")
    status=models.CharField(max_length=20,choices=Status.choices,default=Status.INITIATED)
    amount=models.PositiveIntegerField()
    gateway=models.CharField(max_length=50,default="mock")
    ref_id=models.CharField(max_length=100,blank=True,null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    paid_at=models.DateField(blank=True,null=True)
    def __str__(self):
        return f"Payment#{self.id}-{self.status}"
#-------------------------------------------------
class Refund(models.Model):
    class Status(models.TextChoices):
        REQUESTED="REQUESTED","درخواست شده"
        DONE="DONE","انجام شده"
        REJECTED="REJECTED","رد شده"
    booking=models.OneToOneField(Booking,on_delete=models.CASCADE,related_name="refund")
    status=models.CharField(max_length=20,choices=Status.choices,default=Status.REQUESTED)
    amount=models.PositiveIntegerField()
    created_at=models.DateTimeField(auto_now_add=True)
    done_at=models.DateTimeField(blank=True,null=True)
#-----------------------------------------------------
class Passenger(models.Model):
    booking=models.ForeignKey('Booking',on_delete=models.CASCADE)
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    national_code=models.CharField(max_length=10)
    seat_number=models.PositiveIntegerField()
    def __str__(self):
        return f"{self.first_name}{self.last_name} - Seat {self.seat_number}"
    
    def clean(self):
        if not self.booking_id:
            return
        
        trip=self.booking.trip
        reversed_seats=trip.get_reserved_seats()
        
        if self.seat_number in reversed_seats:
            raise ValidationError(
                {"seat_number":"این صندلی قبلا رزرو شده است"}
            )
            
        def save(self,*args,**kwargs):
            self.full_clean()
            super().save(*args,**kwargs)

#------------------------------------------------------------------
