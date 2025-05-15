from django import forms
from .models import CraftPiece,OldPiece,SaleInvoice







# -----------------------------------------
class CraftPieceForm(forms.ModelForm):
    class Meta:
        model = CraftPiece
        fields = ['gold_type','name','net_weight','weight_with_accessory', 'buy_ojrat','buy_price_ojrat', 'sale_ojrat','sale_price_ojrat', 'notes','code']
        widgets = {
            'gold_type': forms.Select(attrs={
                "style": "font-family: Vazirmatn, sans-serif; font-size: 12px",
                'required': 'required'
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'نام کالا',
                'style': 'font-family: Vazirmatn, sans-serif; font-size: 12px;',
                'required': 'required',
            }),
            'net_weight': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'وزن قطعه',
                'style': 'font-family: Vazirmatn, sans-serif; font-size: 12px;',
                'required': 'required',
            }),
            'weight_with_accessory': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'وزن با متعلقات',
                'style': 'font-family: Vazirmatn, sans-serif; font-size: 12px;',
            }),
            'buy_ojrat': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'اجرت خرید',
                'style': 'font-family: Vazirmatn, sans-serif; font-size: 12px;',
                'required': 'required',
            }),
            'buy_price_ojrat': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'اجرت ریالی خرید(تومان)',
                'style': 'font-family: Vazirmatn, sans-serif; font-size: 12px;',
            }),
            'sale_ojrat': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'اجرت فروش',
                'style': 'font-family: Vazirmatn, sans-serif; font-size: 12px;',
                'required': 'required',
            }),
            'sale_price_ojrat': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'اجرت ریالی فروش(تومان)',
                'style': 'font-family: Vazirmatn, sans-serif; font-size: 12px;',
            }),
            'code': forms.TextInput(attrs={
                'placeholder': 'کد کالا',
                'style': "font-family: Vazirmatn, sans-serif; font-size: 12px",
                'required': 'required'
            }),
            'notes': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'شرح',
                'style': 'font-family: Vazirmatn, sans-serif; font-size: 12px;',

            }),
        }
        labels = {
            'gold_type': '',
            'name': '',
            'net_weight': '',
            'weight_with_accessory': '',
            'buy_ojrat': '',
            'buy_price_ojrat':'',
            'sale_ojrat': '',
            'sale_price_ojrat': '',
            'code': '',
            'notes': '',
        }


# -------------------------------------------
class OldPieceForm(forms.ModelForm):
    class Meta:
        model = OldPiece
        fields = ['supplier','name','net_weight','weight_with_accessory','sale_price_ojrat', 'buy_price', 'buy_date','buy_dailyprice','code', 'notes']
        widgets = {
            'supplier': forms.Select(attrs={
                'class': 'form-control select2',
                'style': 'font-family: Vazirmatn, sans-serif; font-size: 12px',
                'required': 'required',
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'نام کالا',
                'style': 'font-family: Vazirmatn, sans-serif; font-size: 12px;',
                'required': 'required',
            }),
            'net_weight': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'وزن قطعه',
                'style': 'font-family: Vazirmatn, sans-serif; font-size: 12px;',
                'required': 'required',
            }),
            'weight_with_accessory': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'وزن با متعلقات',
                'style': 'font-family: Vazirmatn, sans-serif; font-size: 12px;',
            }),

            'sale_price_ojrat': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'اجرت ریالی فروش',
                'style': 'font-family: Vazirmatn, sans-serif; font-size: 12px;',
                'required': 'required',
            }),
            'buy_price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'مبلغ خرید',
                'style': 'font-family: Vazirmatn, sans-serif; font-size: 12px;',
                'required': 'required',
            }),
            'buy_date': forms.TextInput(attrs={
                'data-jdp': 'true',
                'class': 'form-control',
                'required': True,
                'placeholder': 'تاریخ فاکتور',
                'style': 'font-family: Vazirmatn, sans-serif; font-size: 12px',
                'autocomplete': 'off',
            }),
            'buy_dailyprice': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'نرخ روز طلا',
                'style': 'font-family: Vazirmatn, sans-serif; font-size: 12px;',
                'required': 'required',
            }),
            'code': forms.TextInput(attrs={
                'placeholder': 'کد کالا',
                'style': "font-family: Vazirmatn, sans-serif; font-size: 12px",
                'required': 'required'
            }),
            'notes': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'شرح',
                'style': 'font-family: Vazirmatn, sans-serif; font-size: 12px;',

            }),
        }
        labels = {
            'supplier': '',
            'name': '',
            'net_weight': '',
            'weight_with_accessory': '',
            'sale_price_ojrat': '',
            'buy_price':'',
            'buy_date': '',
            'buy_dailyprice': '',
            'code': '',
            'notes': '',
        }

# ---------------------------------------
class UploadImageForm(forms.Form):
    image = forms.ImageField(label="", required=True)



# -----------------------------------------
class SaleInvoiceForm(forms.ModelForm):
    class Meta:
        model = SaleInvoice
        fields = ['sale_dailyprice', 'customer', 'companyseller', 'sale_date',
                  'discount', 'sale_price', 'net_sale_price', 'invoice_serial', 'notes']
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
            'discount': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'تخفیف',
                'style': 'font-family: Vazirmatn, sans-serif; font-size: 12px;',
            }),
            'sale_price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'مبلغ فاکتور',
                'style': 'font-family: Vazirmatn, sans-serif; font-size: 12px;',
                'required': 'required',
            }),
            'net_sale_price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'خالص مبلغ فاکتور',
                'style': 'font-family: Vazirmatn, sans-serif; font-size: 12px;',
                'required': 'required',
            }),
            'notes': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'شرح',
                'style': 'font-family: Vazirmatn, sans-serif; font-size: 12px;',
            }),
            'invoice_serial': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'سریال فاکتور',
                'style': 'font-family: Vazirmatn, sans-serif; font-size: 12px;',
                'required': 'required',
            }),
        }
        labels = {
            'customer': '',
            'companyseller': '',
            'sale_date': '',
            'sale_dailyprice': '',
            'sale_price': '',
            'net_sale_price': '',
            'discount': '',
            'notes': '',
            'invoice_serial': '',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # تنظیم مقدار پیش‌فرض تخفیف به ۰
        if not self.initial.get('discount'):
            self.initial['discount'] = 0
