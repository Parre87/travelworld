# booking/forms.py
from django import forms

class SearchForm(forms.Form):
    origin = forms.CharField(required=False)
    destination = forms.CharField(required=False)
    depart_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    return_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'})
    )

class BookingForm(forms.Form):
    passengers = forms.IntegerField(min_value=1, max_value=9, initial=1)
    contact_name = forms.CharField(max_length=120)
    contact_email = forms.EmailField()
