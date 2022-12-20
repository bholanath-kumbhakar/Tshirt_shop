from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm
from store.models import Order


##############################################

class Userform(UserCreationForm):
    username=forms.EmailField(required=True,label="Email")
    first_name=forms.CharField(required=True)
    last_name=forms.CharField(required=True)

    def clean_first_name(self):
        value=self.cleaned_data.get('first_name')
        if len(value.strip()) < 3 :
            raise ValidationError('Name must be at least 3 char')
        return value.strip()

    class Meta:
        model=User
        fields=['username','first_name','last_name']

#############################################

class LoginForm(AuthenticationForm):
    username=forms.EmailField(required=True, label='Email')
    


###########################################

class CheckoutForm(forms.ModelForm):
    class Meta:
        model=Order
        fields=['shipping_address','phone','payment_method']