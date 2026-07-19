from django.shortcuts import render,redirect
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm,UserLoginForm
from .models import Wallet
from bookings.models import Ticket

def register_view(request):
    if request.method=='POST':
        form=UserRegisterForm(request.POST)
        if form.is_valid():
            user=form.save()
            login(request,user)
            return redirect('trips:trip_list')
        else:
            print(form.errors)
    
    else:
        form=UserRegisterForm()
    return render(request,'accounts/register.html',{'form':form})
#-----------------------------------------
def login_view(request):
    if request.method=='POST':
        form=UserLoginForm(request.POST)
        if form.is_valid():
            phone_number=form.cleaned_data.get('phone_number')
            password=form.cleaned_data.get('password')
            user=authenticate(request,username=phone_number,password=password)
            if user is not None:
                login(request,user)
                return redirect('accounts:profile')
            else:
                form.add_error(None,"شماره موبایل یا رمز عبور اشتباه است")
    else:
        form=UserLoginForm()
    return render(request,'accounts/login.html',{'form':form})
#------------------------------------------------
def logout_view(request):
    logout(request)
    return redirect('accounts:login')

#-----------------------------------------------
@login_required
def profile_view(request):
    try:
        wallet=Wallet.objects.get(user=request.user)
    except Wallet.DoesNotExist:
        wallet=Wallet.objects.create(user=request.user,balance=1500000)

    tickets=Ticket.objects.filter(booking__user=request.user).select_related('trip','booking')

    return render(request,'accounts/profile.html',{
        'user':request.user,
        'wallet':wallet,
        'tickets':tickets,
    })



    
