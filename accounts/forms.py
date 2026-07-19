from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(label='نام',error_messages={'required':'این فیلد الزامی است'})
    last_name = forms.CharField(label='نام خانوادگی',error_messages={'required':'این فیلد الزامی است'})
    phone_number = forms.CharField(label='شماره موبایل',error_messages={'required':'این فیلد الزامی است'})

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone_number', 'password1', 'password2']

    def clean_password2(self):
        password1=self.cleaned_data.get('password1')
        password2=self.cleaned_data.get('password2')
        if password1 and password2 and password1 !=password2:
            raise forms.ValidationError('رمز عبور شما مطابقت ندارد')
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.phone_number=self.cleaned_data['phone_number']
        user.username=self.cleaned_data['phone_number']

        if commit:
            user.save()

        return user
#--------------------
class UserLoginForm(forms.Form):
    phone_number=forms.CharField(label='شماره موبایل')
    password=forms.CharField(widget=forms.PasswordInput,label="رمز عبور")    