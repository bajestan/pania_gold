from django import forms
from .models import BuyRawInvoice,ReciptMeltInvoice, ReciptCraftInvoice,BuyScrapInvoice,Customer,Supplier





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
                "style": "font-family: Vazirmatn, sans-serif; font-size: 12px"
            }),
        }
        labels = {
            'first_name': '',
            'last_name': '',
            'mellicode':'',
            'phone_number': '',
            'city': '',
            'address': '',
        }
# -----------------------------------------

class CompanyCustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['melliserail', 'last_name', 'phone','city', 'address']
        widgets = {
            'melliserail': forms.TextInput(attrs={
                "placeholder": "شناسه ملی شرکت",
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
                "style": "font-family: Vazirmatn, sans-serif; font-size: 12px"
            }),
        }
        labels = {
            'melliserail': '',
            'last_name': '',
            'phone': '',
            'city': '',
            'address': '',
        }
# -------------------------------
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
                "style": "font-family: Vazirmatn, sans-serif; font-size: 12px"
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
# -------------------------------------



class BuyRawInvoiceForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # اصلاح نوع تامین: اضافه کردن گزینه خالی و نادیده گرفتن مقدار پیش‌فرض
        self.fields['supply_type'].choices = [('', '— انتخاب نوع تأمین —')] + list(self.fields['supply_type'].choices)
        self.fields['supply_type'].initial = ''

        # اصلاح فروشنده کمپانی: اضافه کردن گزینه خالی
        self.fields['companyseller'].empty_label = '— انتخاب فروشنده —'
        self.fields['companyseller'].initial = None

    class Meta:
        model = BuyRawInvoice
        fields = [
            'supplier', 'companyseller', 'supply_type',
            'invoice_date', 'net_weight', 'invoice_dailyprice',
            'invoice_price', 'discount', 'notes'
        ]
        widgets = {
            'supplier': forms.Select(attrs={
                'class': 'form-control select2',
                'style': 'font-family: Vazirmatn, sans-serif; font-size: 12px;',
                'required': 'required'
            }),
            'companyseller': forms.Select(attrs={
                "style": "font-family: Vazirmatn, sans-serif; font-size: 12px;",
                'required': 'required'
            }),
            'supply_type': forms.Select(attrs={
                'style': 'font-family: Vazirmatn, sans-serif; font-size: 12px;',
                'required': 'required'
            }),
            'invoice_date': forms.TextInput(attrs={
                'data-jdp': 'true',
                'class': 'form-control',
                "placeholder": "تاریخ فاکتور",
                "style": "font-family: Vazirmatn, sans-serif; font-size: 12px;",
                'required': 'required',
                'autocomplete': 'off'
            }),
            'net_weight': forms.NumberInput(attrs={
                "placeholder": "وزن خالص",
                "style": "font-family: Vazirmatn, sans-serif; font-size: 12px;",
                'required': 'required',
                'min': '0.01'
            }),
            'invoice_dailyprice': forms.NumberInput(attrs={
                "placeholder": "نرخ روز طلا",
                "style": "font-family: Vazirmatn, sans-serif; font-size: 12px;",
                'required': 'required'
            }),
            'invoice_price': forms.NumberInput(attrs={
                "placeholder": "مبلغ فاکتور",
                "style": "font-family: Vazirmatn, sans-serif; font-size: 12px;",
                'required': 'required'
            }),
            'discount': forms.NumberInput(attrs={
                "placeholder": "تخفیف",
                "style": "font-family: Vazirmatn, sans-serif; font-size: 12px;"
            }),
            'notes': forms.TextInput(attrs={
                "placeholder": "توضیحات",
                "style": "font-family: Vazirmatn, sans-serif; font-size: 12px;"
            }),
        }
        labels = {
            'supplier': '',
            'companyseller': '',
            'supply_type': '',
            'invoice_date': '',
            'net_weight': '',
            'invoice_dailyprice': '',
            'invoice_price': '',
            'discount': '',
            'notes': '',
        }


# ---------------قیچی-----------------------

class BuyScrapInvoiceForm(forms.ModelForm):
    class Meta:
        model = BuyScrapInvoice
        fields = [
             'customer', 'companyseller',
            'invoice_date', 'net_weight', 'karat_weight','invoice_dailyprice',
            'invoice_price', 'discount', 'notes'
        ]
        widgets = {
            'customer': forms.Select(
                attrs={'class': 'form-control select2',
                       'style': 'font-family: Vazirmatn, sans-serif; font-size: 12px;', 'required': 'required'}),
            'companyseller': forms.Select(attrs={
                "style": "font-family: Vazirmatn, sans-serif; font-size: 12px",
                'required': 'required'
            }),
            'invoice_date': forms.TextInput(attrs={'data-jdp': 'true','class': 'form-control',"placeholder":"تاریخ فاکتور" ,
                       "style": "font-family: Vazirmatn, sans-serif;"
                        " font-size: 12px", 'required': 'required','autocomplete': 'off'}),
            'net_weight': forms.NumberInput(attrs={
                "placeholder": "وزن ترازو",
                "style": "font-family: Vazirmatn, sans-serif; font-size: 12px",'required': 'required',
                'min': '0.01'
            }),
            'karat_weight': forms.NumberInput(attrs={
                "placeholder": "وزن 740",
                "style": "font-family: Vazirmatn, sans-serif; font-size: 12px", 'required': 'required',
                'min': '0.01'
            }),
            'invoice_dailyprice': forms.NumberInput(attrs={
                "placeholder": "نرخ روز طلا",
                "style": "font-family: Vazirmatn, sans-serif; font-size: 12px",'required': 'required'
            }),
            'invoice_price': forms.NumberInput(attrs={
                "placeholder": "مبلغ فاکتور",
                "style": "font-family: Vazirmatn, sans-serif; font-size: 12px",'required': 'required'
            }),
            'discount': forms.NumberInput(attrs={
                "placeholder": "تخفیف",
                "style": "font-family: Vazirmatn, sans-serif; font-size: 12px",
            }),
            'notes': forms.TextInput(attrs={
                "placeholder": "توضیحات",
                "style": "font-family: Vazirmatn, sans-serif; font-size: 12px",
            }),
        }
        labels = {
            'customer': '',
            'companyseller': '',
            'invoice_date': '',
            'net_weight': '',
            'karat_weight': '',
            'invoice_dailyprice': '',
            'invoice_price': '',
            'discount': '',
            'notes': '',
        }

# -----------------------------------------
class ReciptMeltInvoiceForm(forms.ModelForm):
    class Meta:
        model = ReciptMeltInvoice
        fields = ['melt_type','supplier',  'invoice_date','invoice_serial', 'net_weight']
        widgets = {
            'melt_type': forms.Select(attrs={
                "style": "font-family: Vazirmatn, sans-serif; font-size: 12px",
                'required': 'required'
            }),
            'supplier': forms.Select(attrs={
                'class': 'form-control select2',
                'style': 'font-family: Vazirmatn, sans-serif; font-size: 12px;',
                'required': 'required',
            }),
            'invoice_date': forms.TextInput(attrs={
                'data-jdp': 'true',
                'class': 'form-control',
                'required': True,
                'placeholder': 'تاریخ فاکتور',
                'style': 'font-family: Vazirmatn, sans-serif; font-size: 12px',
                'autocomplete': 'off',
            }),
            'invoice_serial': forms.TextInput(attrs={
                'placeholder': 'سریال فاکتور',
                'style': "font-family: Vazirmatn, sans-serif; font-size: 12px",

            }),
            'net_weight': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'وزن خالص فاکتور',
                'style': 'font-family: Vazirmatn, sans-serif; font-size: 12px;',
                'required': 'required',
                'min': '0.01',
            }),
        }
        labels = {
            'supplier': '',
            'invoice_date': '',
            'invoice_serial': '',
            'net_weight': '',
        }

# ----------------------------

class ReciptCraftInvoiceForm(forms.ModelForm):
    class Meta:
        model = ReciptCraftInvoice
        fields = ['pay_type','supplier', 'companyseller' ,'invoice_date','invoice_serial', 'net_weight','accessory_weight','qty','invoice_dailyprice','discount','notes']
        widgets = {
            'pay_type': forms.Select(attrs={
                "style": "font-family: Vazirmatn, sans-serif; font-size: 12px",
                'required': 'required'
            }),
            'supplier': forms.Select(attrs={
                'class': 'form-control select2',
                'style': 'font-family: Vazirmatn, sans-serif; font-size: 12px;',
                'required': 'required',
            }),
            'companyseller': forms.Select(attrs={
                'class': 'form-control select',
                'style': 'font-family: Vazirmatn, sans-serif; font-size: 12px;',
                'required': 'required',
            }),
            'invoice_date': forms.TextInput(attrs={
                'data-jdp': 'true',
                'class': 'form-control',
                'required': True,
                'placeholder': 'تاریخ فاکتور',
                'style': 'font-family: Vazirmatn, sans-serif; font-size: 12px',
                'autocomplete': 'off',
            }),
            'invoice_serial': forms.TextInput(attrs={
                'placeholder': 'سریال فاکتور',
                'style': "font-family: Vazirmatn, sans-serif; font-size: 12px",

            }),
            'net_weight': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'وزن خالص فاکتور',
                'style': 'font-family: Vazirmatn, sans-serif; font-size: 12px;',
                'required': 'required',
                'min': '0.01',
            }),
            'accessory_weight': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'وزن با متعلقات فاکتور',
                'style': 'font-family: Vazirmatn, sans-serif; font-size: 12px;',
            }),
            'qty': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'تعداد اقلام فاکتور',
                'style': 'font-family: Vazirmatn, sans-serif; font-size: 12px;',
                'required': 'required',
            }),
            'invoice_dailyprice': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'نرخ روز طلا',
                'style': 'font-family: Vazirmatn, sans-serif; font-size: 12px;',
                'required': 'required',
            }),
            'discount': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'تخفیف',
                'style': 'font-family: Vazirmatn, sans-serif; font-size: 12px;',

            }),
            'notes': forms.TextInput(attrs={
                "placeholder": "توضیحات",
                "style": "font-family: Vazirmatn, sans-serif; font-size: 12px",
            }),
        }
        labels = {
            'supplier': '',
            'companyseller':'',
            'invoice_date': '',
            'invoice_serial': '',
            'net_weight': '',
            'accessory_weight': '',
            'qty': '',
            'invoice_dailyprice':'',
            'discount': '',
            'notes':'',
        }

