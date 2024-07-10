from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from orders.models import LandsUndNumbers
from users.models import User

class UserLoginForm(AuthenticationForm):
    
    username =forms.CharField()
    password =forms.CharField()

    class Meta:
        model = User
        fields = (
            "username",
            "password"
        )

class UserRegistrationForm(UserCreationForm):

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "username",
            "email",
            "password1",
            "password2"
        )

    first_name =forms.CharField()
    last_name =forms.CharField()
    username =forms.CharField()
    email =forms.CharField()
    password1 =forms.CharField()
    password2 =forms.CharField()

class ProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = (
            "image",
            "first_name",
            "last_name",
            "username",
            "country_or_region",
            "street_and_house_number",
            "additional_address",
            "postcode",
            "location",
            "email",

        )
    image = forms.ImageField(required=False)
    first_name =forms.CharField()
    last_name =forms.CharField()
    username =forms.CharField()
    country_or_region = forms.ModelChoiceField(queryset=LandsUndNumbers.objects.all(), required=True, label='lands_and_numbers')
    street_and_house_number = forms.CharField()
    additional_address = forms.CharField()
    postcode = forms.CharField()
    location = forms.CharField()
    email = forms.CharField()

