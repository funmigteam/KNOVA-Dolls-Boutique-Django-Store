from django import forms
from django.contrib.auth.models import User
from .models import Address

class RegisterForm(forms.ModelForm):
    password = forms.CharField(label='رمز عبور', widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['first_name','username','email','password']
        labels = {'first_name':'نام شما','username':'نام کاربری','email':'ایمیل'}
    def save(self, commit=True):
        user = super().save(commit=False); user.set_password(self.cleaned_data['password'])
        if commit: user.save()
        return user

class CheckoutForm(forms.Form):
    full_name = forms.CharField(label='نام و نام خانوادگی')
    phone = forms.CharField(label='شماره تماس')
    address = forms.CharField(label='نشانی کامل', widget=forms.Textarea)
    note = forms.CharField(label='یادداشت سفارش', required=False, widget=forms.Textarea)

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['title','receiver','phone','province','city','postal_code','address','is_default']
