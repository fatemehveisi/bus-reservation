from django.db import models
#-------------------------------------------------
class City(models.Model):
    name=models.CharField(max_length=100,unique=True)
    slug=models.SlugField(max_length=120,unique=True)
    def __str__(self):
        return self.name
#----------------------------------------------------
class Bustype(models.Model):
    name=models.CharField(max_length=80,unique=True)
    seat_count=models.PositiveSmallIntegerField()
    def __str__(self):
        return f"{self.name} ({self.seat_count} seats)"
#----------------------------------------------------
class Bus(models.Model):
    plate_number=models.CharField(max_length=20,unique=True)
    bus_type=models.ForeignKey(Bustype,on_delete=models.PROTECT,related_name="buses")
    def __str__(self):
        return self.plate_number
#----------------------------------------------------
class Trip(models.Model):
    origin=models.ForeignKey(City,on_delete=models.PROTECT,related_name="departing_trips")
    destination=models.ForeignKey(City,on_delete=models.PROTECT,related_name="arriving_trips")
    bus=models.ForeignKey(Bus,on_delete=models.PROTECT,related_name="trips")
    available_seats=models.PositiveBigIntegerField(default=40)
    departure_datetime=models.DateTimeField()
    arrival_datetime=models.DateTimeField(blank=True,null=True)
    price=models.PositiveIntegerField()
    is_active=models.BooleanField(default=True)
    class Meta:
        indexes=[
            models.Index(fields=["origin","destination","departure_datetime"]),
        ]
    def __str__(self):
        return f"{self.origin}->{self.destination}@{self.departure_datetime:%Y-%m-%d %H:%M}"
    
    def save(self,*args,**kwargs):
        if not self.pk or self.available_seats is None:
            self.available_seats=self.bus.bus_type.seat_count
        super().save(*args,**kwargs)

    def get_reserved_seats(self):
        from bookings.models import Ticket
        reversed_seats=Ticket.objects.filter(
            trip=self,
            booking__status='PAID'
        ).values_list('seat_number',flat=True)
        return list(reversed_seats)
    def get_available_seats(self):
        total_seats=self.bus.bus_type.seat_count
        reserved_seats=self.get_reserved_seats()
        return[i for i in range(1,total_seats + 1)if i not in reserved_seats]
    
#----------------------------------------------------









    
    