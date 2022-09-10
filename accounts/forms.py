import imp
from accounts.models import *
from django.forms import ModelForm
from django.contrib.auth.models import User

#need to imports 
from django.contrib.auth.forms import UserCreationForm
class OrderForm(ModelForm):
    class Meta:
        model = Order
        #__all__ means to take all the columns of Order table
        #have to wirte ['status', 'customer'] to take specific data
        fields = '__all__'
        
class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2']
                
class CustomerProfileSetting(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        exclude=['user','name']