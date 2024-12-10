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
            "country_or_region",
            "first_name",
            "last_name",
            "username",
            "street_and_house_number",
            "postcode",
            "location",
            "email",
        )
    image = forms.ImageField(required=False,)
    country_or_region = forms.ModelChoiceField(queryset=LandsUndNumbers.objects.all(), required=True, label='lands_and_numbers',)
    first_name =forms.CharField(required=False,)
    last_name =forms.CharField(required=False,)
    username =forms.CharField(required=False,)
    street_and_house_number = forms.CharField(required=False,)
    postcode = forms.CharField(required=False,)
    location = forms.CharField(required=False,)
    email = forms.CharField(required=False,)


class TrackingNumberForm(forms.Form):
    tracking_number = forms.CharField(max_length=100, required=True, label='Трекинговый номер')