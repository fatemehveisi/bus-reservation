from django.shortcuts import render,get_object_or_404,redirect
from.models import Trip, City
import datetime

def trip_list(request):
    origin=request.GET.get('origin')
    destination=request.GET.get('destination')

    if origin or destination:
        if not request.user.is_authenticated:
            return redirect('accounts:login')

    trips=Trip.objects.all()
    cities=City.objects.all()
    if origin:
        trips=trips.filter(origin__id=origin)
    if destination:
        trips=trips.filter(destination__id=destination)
        
    return render(request,'trips/trip_list.html',{'trips':trips , 'cities':cities ,})

def trip_detail(request,pk):
    trip=get_object_or_404(Trip,pk=pk)
    available_seats=trip.get_available_seats()
    
    context= {
        'trip':trip,
        'available_seats':available_seats,
    }
    return render(request,'trips/trip_detail.html',context)
#----------------------------------------------------------
def about_page(request):
    return render(request,'trips/about.html')
#----------------------------------------------------------
from django.shortcuts import render
from .models import Trip

def trip_results(request):
    origin_id = request.GET.get('origin_id')
    destination_id = request.GET.get('destination_id')
    date = request.GET.get('date')

    trips = Trip.objects.all()

    if origin_id:
        trips = trips.filter(origin_id=origin_id)

    if destination_id:
        trips = trips.filter(destination_id=destination_id)

    if date:
        trips = trips.filter(departure_datetime__date=date)

    for trip in trips:
        trip.available_seats_count=len(trip.get_available_seats())

    return render(request, 'trips/trip_results.html', {'trips': trips})





