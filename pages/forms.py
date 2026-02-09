from django import forms
from .models import VisitorRegistration


class ContactForm(forms.Form):
    name = forms.CharField(max_length=120, widget=forms.TextInput(attrs={"class": "form-control"}))
    phone = forms.CharField(max_length=30, widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Your phone number"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control"}))
    message = forms.CharField(widget=forms.Textarea(attrs={"class": "form-control", "rows": 4}))


class VisitorRegistrationForm(forms.ModelForm):
    class Meta:
        model = VisitorRegistration
        fields = ["name", "email", "phone", "company", "country", "message"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "phone": forms.TextInput(attrs={"class": "form-control"}),
            "company": forms.TextInput(attrs={"class": "form-control"}),
            "country": forms.TextInput(attrs={"class": "form-control"}),
            "message": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }
