from django import forms
from django_select2.forms import ModelSelect2Widget
from .models import SaleInvoicePayment,SaleMeltInvoicePayment,BuyRawInvoicePayment,OldPiecePayment













class SaleInvoicePaymentForm(forms.ModelForm):
    class Meta:
        model = SaleInvoicePayment
        fields = [
             'amount', 'pay_date', 'payment_receipt', 'payment_method',
            'discount_code', 'etebar_code', 'payment_explain'
        ]
        widgets = {

            'amount': forms.NumberInput(
                attrs={
                    "placeholder": "مبلغ پرداخت",
                    "style": "font-family: Vazirmatn, sans-serif; font-size: 12px;"
                }
            ),
            'pay_date': forms.TextInput(
                attrs={
                    'data-jdp': 'true',
                    'class': 'form-control',
                    'required': True,
                    "placeholder": "تاریخ فاکتور",
                    "style": "font-family: Vazirmatn, sans-serif; font-size: 12px",
                    'autocomplete': 'off',
                }
            ),
            'payment_receipt': forms.TextInput(
                attrs={
                    "placeholder": "رسید پرداخت",
                    "style": "font-family: Vazirmatn, sans-serif; font-size: 12px"
                }
            ),
            'payment_method': forms.Select(
                choices=[
                    ('نقدی', 'نقدی'),
                    ('اعتباری', 'اعتباری'),
                    ('تهاتر', 'تهاتر'),
                    ('تخفیف', 'تخفیف')
                ],
                attrs={
                    'class': 'form-control',
                    "style": "font-family: Vazirmatn, sans-serif; font-size: 12px"
                }
            ),
            'discount_code': forms.TextInput(
                attrs={
                    "placeholder": "کد تخفیف",
                    "style": "font-family: Vazirmatn, sans-serif; font-size: 12px"
                }
            ),
            'etebar_code': forms.TextInput(
                attrs={
                    "placeholder": "کد اعتبار",
                    "style": "font-family: Vazirmatn, sans-serif; font-size: 12px"
                }
            ),
            'payment_explain': forms.TextInput(
                attrs={
                    "placeholder": "شرح پرداخت",
                    "style": "font-family: Vazirmatn, sans-serif; font-size: 12px"
                }
            ),
        }
        labels = {
            'amount': '',
            'pay_date': '',
            'payment_receipt': '',
            'payment_method': '',
            'discount_code': '',
            'etebar_code': '',
            'payment_explain': '',
        }
# --------------------------------------------

class MeltSaleInvoicePaymentForm(forms.ModelForm):
    class Meta:
        model = SaleMeltInvoicePayment
        fields = [
             'amount', 'pay_date', 'payment_receipt', 'payment_method',
            'discount_code', 'etebar_code', 'payment_explain'
        ]
        widgets = {

            'amount': forms.NumberInput(
                attrs={
                    "placeholder": "مبلغ پرداخت",
                    "style": "font-family: Vazirmatn, sans-serif; font-size: 12px;"
                }
            ),
            'pay_date': forms.TextInput(
                attrs={
                    'data-jdp': 'true',
                    'class': 'form-control',
                    'required': True,
                    "placeholder": "تاریخ فاکتور",
                    "style": "font-family: Vazirmatn, sans-serif; font-size: 12px",
                    'autocomplete': 'off',
                }
            ),
            'payment_receipt': forms.TextInput(
                attrs={
                    "placeholder": "رسید پرداخت",
                    "style": "font-family: Vazirmatn, sans-serif; font-size: 12px"
                }
            ),
            'payment_method': forms.Select(
                choices=[
                    ('نقدی', 'نقدی'),
                    ('اعتباری', 'اعتباری'),
                    ('تهاتر', 'تهاتر'),
                    ('تخفیف', 'تخفیف')
                ],
                attrs={
                    'class': 'form-control',
                    "style": "font-family: Vazirmatn, sans-serif; font-size: 12px"
                }
            ),
            'discount_code': forms.TextInput(
                attrs={
                    "placeholder": "کد تخفیف",
                    "style": "font-family: Vazirmatn, sans-serif; font-size: 12px"
                }
            ),
            'etebar_code': forms.TextInput(
                attrs={
                    "placeholder": "کد اعتبار",
                    "style": "font-family: Vazirmatn, sans-serif; font-size: 12px"
                }
            ),
            'payment_explain': forms.TextInput(
                attrs={
                    "placeholder": "شرح پرداخت",
                    "style": "font-family: Vazirmatn, sans-serif; font-size: 12px"
                }
            ),
        }
        labels = {
            'amount': '',
            'pay_date': '',
            'payment_receipt': '',
            'payment_method': '',
            'discount_code': '',
            'etebar_code': '',
            'payment_explain': '',
        }

# --------------------------------------------

class BuyrawInvoicePaymentForm(forms.ModelForm):
    class Meta:
        model = BuyRawInvoicePayment
        fields = [
             'amount', 'pay_date', 'payment_method',
            'payment_place', 'payment_receipt', 'payment_explain'
        ]
        widgets = {

            'amount': forms.NumberInput(
                attrs={
                    "placeholder": "مبلغ پرداخت",
                    "style": "font-family: Vazirmatn, sans-serif; font-size: 12px;"
                }
            ),
            'pay_date': forms.TextInput(
                attrs={
                    'data-jdp': 'true',
                    'class': 'form-control',
                    'required': True,
                    "placeholder": "تاریخ فاکتور",
                    "style": "font-family: Vazirmatn, sans-serif; font-size: 12px",
                    'autocomplete': 'off',
                }
            ),

            'payment_method': forms.Select(
                choices=[
                    ('حساب رسمی', 'حساب رسمی'),
                    ('حساب غیر رسمی', 'حساب غیر رسمی'),
                ],
                attrs={
                    'class': 'form-control',
                    "style": "font-family: Vazirmatn, sans-serif; font-size: 12px"
                }
            ),
            'payment_place': forms.TextInput(
                attrs={
                    "placeholder": "محل پرداخت",
                    "style": "font-family: Vazirmatn, sans-serif; font-size: 12px"
                }
            ),
            'payment_receipt': forms.TextInput(
                attrs={
                    "placeholder": "رسید پرداخت",
                    "style": "font-family: Vazirmatn, sans-serif; font-size: 12px"
                }
            ),
            'payment_explain': forms.TextInput(
                attrs={
                    "placeholder": "شرح پرداخت",
                    "style": "font-family: Vazirmatn, sans-serif; font-size: 12px"
                }
            ),
        }
        labels = {
            'amount': '',
            'pay_date': '',
            'payment_receipt': '',
            'payment_method': '',
            'payment_place': '',
            'payment_explain': '',
        }
# ---------------------------------------------


class OldPiecePaymentForm(forms.ModelForm):
    class Meta:
        model = OldPiecePayment
        fields = [
             'amount', 'pay_date', 'payment_method',
            'payment_place', 'payment_receipt', 'payment_explain'
        ]
        widgets = {

            'amount': forms.NumberInput(
                attrs={
                    "placeholder": "مبلغ پرداخت",
                    "style": "font-family: Vazirmatn, sans-serif; font-size: 12px;"
                }
            ),
            'pay_date': forms.TextInput(
                attrs={
                    'data-jdp': 'true',
                    'class': 'form-control',
                    'required': True,
                    "placeholder": "تاریخ فاکتور",
                    "style": "font-family: Vazirmatn, sans-serif; font-size: 12px",
                    'autocomplete': 'off',
                }
            ),

            'payment_method': forms.Select(
                choices=[
                    ('حساب رسمی', 'حساب رسمی'),
                    ('حساب غیر رسمی', 'حساب غیر رسمی'),
                ],
                attrs={
                    'class': 'form-control',
                    "style": "font-family: Vazirmatn, sans-serif; font-size: 12px"
                }
            ),
            'payment_place': forms.TextInput(
                attrs={
                    "placeholder": "محل پرداخت",
                    "style": "font-family: Vazirmatn, sans-serif; font-size: 12px"
                }
            ),
            'payment_receipt': forms.TextInput(
                attrs={
                    "placeholder": "رسید پرداخت",
                    "style": "font-family: Vazirmatn, sans-serif; font-size: 12px"
                }
            ),
            'payment_explain': forms.TextInput(
                attrs={
                    "placeholder": "شرح پرداخت",
                    "style": "font-family: Vazirmatn, sans-serif; font-size: 12px"
                }
            ),
        }
        labels = {
            'amount': '',
            'pay_date': '',
            'payment_receipt': '',
            'payment_method': '',
            'payment_place': '',
            'payment_explain': '',
        }
# ---------------------------------------------