from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction
from django.core.exceptions import ValidationError
from trips.models import Trip
from bookings.models import Booking, Ticket, Payment
from accounts.models import Wallet

def buy_ticket(request, trip_id):
    trip = get_object_or_404(Trip, id=trip_id)
    wallet, created = Wallet.objects.get_or_create(user=request.user, defaults={'balance': 12000000})
    price = trip.price 

    reserved_seats = list(Ticket.objects.filter(trip=trip).values_list('seat_number', flat=True))
    reserved_seats = [int(s) for s in reserved_seats]
    total_seats_range = list(range(1, 33))


    if request.method == "POST":
        full_name = request.POST.get("full_name", "").strip()
        national_code = request.POST.get("national_code", "").strip()
        seat_number_raw = request.POST.get("seat_number", "").strip()


        if not full_name:
            messages.error(request, "نام و نام خانوادگی را وارد کنید")
        elif not national_code:
            messages.error(request, "کد ملی را وارد کنید")
        elif not seat_number_raw:
            messages.error(request, "لطفاً ابتدا صندلی مورد نظر خود را انتخاب کنید")
        else:
            try:
                seat_number = int(seat_number_raw)
                
                if seat_number in reserved_seats:
                    messages.error(request, f"صندلی شماره {seat_number} قبلاً رزرو شده است.")
                elif wallet.balance < price:
                    messages.error(request, "موجودی کیف پول شما کافی نیست.")
                else:
                    with transaction.atomic():
                        booking = Booking.objects.create(
                            user=request.user,
                            trip=trip,
                            status="confirmed"
                        )

                        ticket = Ticket.objects.create(
                            booking=booking,
                            trip=trip,
                            seat_number=seat_number,
                            full_name=full_name,
                            national_code=national_code
                        )

                        Payment.objects.create(
                            booking=booking,
                            amount=price,
                            status="paid",
                            gateway="wallet"
                        )

                
                        wallet.balance -= price
                        wallet.save()
                        
                        if trip.available_seats is None:
                            messages.error(request,"ظرفیت این سفر مشخص نیست")
                            return redirect("bookings:buy_ticket",trip_id=trip.id)
                        
                        if trip.available_seats<=0:
                            messages.error(request,"متاسفانه ظرفیت این سفر تکمیل شده است")
                            return redirect("bookings:buy_ticket",trip_id=trip.id)
                        trip.available_seats -= 1
                        trip.save()

                    messages.success(request, f"بلیت شما برای صندلی {seat_number} با موفقیت صادر شد.")
                    return redirect("bookings:ticket_success", ticket_id=ticket.id)
            
            except ValueError:
                messages.error(request, "شماره صندلی نامعتبر است.")
            except Exception as e:
                messages.error(request, f"خطایی در ثبت رزرو رخ داد: {str(e)}")

    context = {
        "trip": trip,
        "price": price,
        "balance": wallet.balance,
        "reserved_seats": reserved_seats,
        "total_seats_range": total_seats_range,
    }
    return render(request, "bookings/confirm_buy.html", context)
#------------------------------------------------------------
def add_credit(request):
    if request.method=="POST":
        amount=int(request.POST.get("amount"))
        wallet=Wallet.objects.get(user=request.user)
        wallet.balance += amount
        wallet.save()
        messages.success(request,f"{amount}تومان به کیف پول شما اضافه شد")
    return render(request,"bookings/add_credit.html")
#--------------------------------------------------------------

def ticket_success(request,ticket_id):
    ticket=get_object_or_404(Ticket,id=ticket_id)
    return render(request,'bookings/ticket_success.html',{'ticket':ticket})


