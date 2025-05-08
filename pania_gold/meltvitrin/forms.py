from django import forms
from .models import MeltPiece,SaleMeltInvoice




# ----------------------------------
class MeltPieceForm(forms.ModelForm):
    class Meta:
        model = MeltPiece
        fields = ['weight', 'karat', 'ang_number', 'lab_name','sale_ojrat', 'additional_info','net_weight','code']
        widgets = {

            'weight': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'وزن قطعه',
                'style': 'font-family: Vazirmatn, sans-serif; font-size: 12px;','required': 'required',
            }),

            'karat': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'عیار قطعه',
                'style': 'font-family: Vazirmatn, sans-serif; font-size: 12px;','required': 'required',
            }),
            'ang_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'شماره انگ',
                'style': 'font-family: Vazirmatn, sans-serif; font-size: 12px;','required': 'required',
            }),
            'lab_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'نام آزمایشگاه',
                'style': 'font-family: Vazirmatn, sans-serif; font-size: 12px;','required': 'required',
            }),

            'sale_ojrat': forms.NumberInput(attrs={
                'class': 'form-control',
                'required': 'required',
                'placeholder': 'اجرت فروش',
                'style': 'font-family: Vazirmatn, sans-serif; font-size: 12px;',
            }),
            'additional_info': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'شرح',
                'style': 'font-family: Vazirmatn, sans-serif; font-size: 12px;',

            }),
            'net_weight': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'وزن عیار750',
                'style': 'font-family: Vazirmatn, sans-serif; font-size: 12px;', 'required': 'required',
            }),
            'code': forms.TextInput(attrs={
                'placeholder': 'کد کالا',
                'style': "font-family: Vazirmatn, sans-serif; font-size: 12px",
                'required': 'required'
            }),
        }
        labels = {

            'weight': '',
            'net_weight': '',
            'karat': '',
            'ang_number': '',
            'lab_name': '',
            'sale_ojrat': '',
            'additional_info': '',
            'code': '',
        }


# -------------------------------------------

class SaleMeltInvoiceForm(forms.ModelForm):
    class Meta:
        model = SaleMeltInvoice
        fields = ['sale_dailyprice','customer', 'companyseller', 'sale_date', 'total_sale_price','discount', 'notes']
        widgets = {
            'sale_dailyprice': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'نرخ روز طلا',
                'style': 'font-family: Vazirmatn, sans-serif; font-size: 12px;',
                'required': 'required',
            }),
            'customer': forms.Select(attrs={
                'class': 'form-control select2',
                'style': 'font-family: Vazirmatn, sans-serif; font-size: 12px',
                'required': 'required',
            }),
            'companyseller': forms.Select(attrs={
                'class': 'form-control select',
                'style': 'font-family: Vazirmatn, sans-serif; font-size: 12px',
                'required': 'required',
            }),
            'sale_date': forms.TextInput(attrs={
                'data-jdp': 'true',
                'class': 'form-control',
                'required': True,
                'placeholder': 'تاریخ فاکتور',
                'style': 'font-family: Vazirmatn, sans-serif; font-size: 12px',
                'autocomplete': 'off',
            }),

            'total_sale_price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'مبلغ فاکتور',
                'style': 'font-family: Vazirmatn, sans-serif; font-size: 12px;',
                'required': 'required',
            }),
            'discount': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'تخفیف',
                'style': 'font-family: Vazirmatn, sans-serif; font-size: 12px;',
            }),

            'notes': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'شرح',
                'style': 'font-family: Vazirmatn, sans-serif; font-size: 12px;',

            }),
        }
        labels = {
            'sale_dailyprice': '',
            'customer': '',
            'companyseller': '',
            'sale_date': '',
            'discount': '',
            'total_sale_price': '',
            'notes': '',
        }
