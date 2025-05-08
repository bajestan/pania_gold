from django import forms
from paniavault.models import Customer,Supplier
from django.core.exceptions import ValidationError
import re


# ------------------------------------------

class IndividualCustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = [ 'mellicode', 'first_name', 'last_name', 'phone_number', 'city', 'address']
        widgets = {
            'mellicode': forms.TextInput(attrs={
                "placeholder": "کد ملی",
                "style": "font-family: Vazirmatn, sans-serif; font-size: 12px",
                'autocomplete': 'off',
                'required': 'required'
            }),
            'first_name': forms.TextInput(attrs={
                "placeholder": "نام",
                "style": "font-family: Vazirmatn, sans-serif; font-size: 12px",
                'required': 'required'
            }),
            'last_name': forms.TextInput(attrs={
                "placeholder": "نام خانوادگی",
                "style": "font-family: Vazirmatn, sans-serif; font-size: 12px",
                'required': 'required'
            }),
            'phone_number': forms.TextInput(attrs={
                "placeholder": "شماره همراه",
                "style": "font-family: Vazirmatn, sans-serif; font-size: 12px",
                'autocomplete': 'off',
                'required': 'required'
            }),
            'city': forms.TextInput(attrs={
                "placeholder": "شهر",
                "style": "font-family: Vazirmatn, sans-serif; font-size: 12px",
                'required': 'required'
            }),
            'address': forms.Textarea(attrs={
                "placeholder": "آدرس",
                "style": "font-family: Vazirmatn, sans-serif; font-size: 12px",
                'required': 'required'
            }),
        }
        labels = {
            'mellicode': '',
            'first_name': '',
            'last_name': '',
            'phone_number': '',
            'city': '',
            'address': '',
        }



# -----------------------------------------

class CompanyCustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['mellicode', 'last_name', 'phone','city', 'address']
        widgets = {
            'mellicode': forms.TextInput(attrs={
                "placeholder": "کد ملی",
                "style": "font-family: Vazirmatn, sans-serif; font-size: 12px",
                'autocomplete': 'off',
                'required': 'required'
            }),
            'last_name': forms.TextInput(attrs={
                "placeholder": "نام شرکت",
                "style": "font-family: Vazirmatn, sans-serif; font-size: 12px",
                'required': 'required'
            }),
            'phone': forms.TextInput(attrs={
                "placeholder": "شماره تلفن",
                "style": "font-family: Vazirmatn, sans-serif; font-size: 12px",
                'autocomplete': 'off',
                'required': 'required'
            }),
            'city': forms.TextInput(attrs={
                "placeholder": "شهر",
                "style": "font-family: Vazirmatn, sans-serif; font-size: 12px",
                'required': 'required'
            }),
            'address': forms.Textarea(attrs={
                "placeholder": "آدرس",
                "style": "font-family: Vazirmatn, sans-serif; font-size: 12px",
                'required': 'required'

            }),
        }
        labels = {
            'mellicode': '',
            'last_name': '',
            'phone': '',
            'city': '',
            'address': '',
        }
# -----------------------------------

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['first_name', 'last_name','mellicode', 'phone_number', 'city', 'address']
        widgets = {
            'first_name': forms.TextInput(attrs={
                "placeholder": "نام",
                "style": "font-family: Vazirmatn, sans-serif; font-size: 12px",
                'required': 'required'
            }),
            'last_name': forms.TextInput(attrs={
                "placeholder": "نام خانوادگی",
                "style": "font-family: Vazirmatn, sans-serif; font-size: 12px",
                'required': 'required'
            }),
            'mellicode': forms.TextInput(attrs={
                "placeholder": "کد ملی",
                "style": "font-family: Vazirmatn, sans-serif; font-size: 12px",
                'autocomplete': 'off',
            }),
            'phone_number': forms.TextInput(attrs={
                "placeholder": "شماره همراه",
                "style": "font-family: Vazirmatn, sans-serif; font-size: 12px",
                'autocomplete': 'off',
                'required': 'required'
            }),
            'city': forms.TextInput(attrs={
                "placeholder": "شهر",
                "style": "font-family: Vazirmatn, sans-serif; font-size: 12px",
                'required': 'required'
            }),
            'address': forms.Textarea(attrs={
                "placeholder": "آدرس",
                "style": "font-family: Vazirmatn, sans-serif; font-size: 12px",
                 'required': 'required'
            }),
        }
        labels = {
            'first_name': '',
            'last_name': '',
            'mellicode': '',
            'phone_number': '',
            'city': '',
            'address': '',
        }
