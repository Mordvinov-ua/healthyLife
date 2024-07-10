
from django import forms

class CreateOrderForm(forms.Form):
    country_or_region = forms.CharField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    phone_number = forms.CharField()
    street_and_house_number = forms.CharField()
    postcode = forms.CharField()
    location = forms.CharField()
    e_mail = forms.CharField()
    delivery_address = forms.CharField(required=False) 

    def clean_delivery_address(self):
        country_or_region = self.cleaned_data.get('country_or_region')
        street_and_house_number = self.cleaned_data.get('street_and_house_number')
        additional_address = self.cleaned_data.get('additional_address')
        postcode = self.cleaned_data.get('postcode')
        location = self.cleaned_data.get('location')
        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')

        # Собираем все части адреса в одну строку
        
        delivery_address = f"{first_name}, {last_name}\n{country_or_region}, {street_and_house_number}, {postcode}, {location}"
        return delivery_address