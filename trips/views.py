from django.shortcuts import render,get_object_or_404
from.models import Trip,City

def trip_list(request):
    origin=request.GET.get('origin')
    destination=request.GET.get('destination')
    trips=Trip.objects.all()
    if origin:
        trips=trips.filter(origin__icontains=origin)
    if destination:
        trips=trips.filter(destination__icontains=destination)
        
    return render(request,'trips/trip_list.html',{'trips':trips})

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
