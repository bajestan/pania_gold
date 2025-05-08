from django.contrib import admin
from .models import OldPiece,CraftPiece,SaleInvoice
from django.utils.html import mark_safe
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
import mimetypes
from django import forms
from io import BytesIO
from django.utils.html import format_html
from django.contrib.admin import SimpleListFilter
from django.utils.translation import gettext_lazy as _
import datetime




# ------------فیلتر تاریخ بر اساس تاریخ فاکتور فروش------------
class SaleDateFilter(SimpleListFilter):
    title = _('تاریخ فروش')
    parameter_name = 'sale_date'

    def lookups(self, request, model_admin):
        return [
            ('today', _('امروز')),
            ('past_7_days', _('۷ روز گذشته')),
            ('this_month', _('ماه جاری')),
        ]

    def queryset(self, request, queryset):
        value = self.value()
        today = datetime.date.today()

        if value == 'today':
            return queryset.filter(sale_invoice__sale_date=today)
        if value == 'past_7_days':
            return queryset.filter(sale_invoice__sale_date__gte=today - datetime.timedelta(days=7))
        if value == 'this_month':
            return queryset.filter(sale_invoice__sale_date__year=today.year, sale_invoice__sale_date__month=today.month)
        return queryset

# --------------------------------------

@admin.register(OldPiece)
class OldPieceAdmin(admin.ModelAdmin):
    list_display = (
        'name','image_thumbnail', 'code',  'net_weight',
         'is_sold','get_sale_date','get_customer_name'
    )
    search_fields = ('code', 'name',)
    list_filter = ('is_sold', SaleDateFilter)

    ordering = ['-sale_invoice__sale_date']
    exclude = ('vitrin', 'sale_invoice')

    def get_customer_name(self, obj):
        if obj.sale_invoice and obj.sale_invoice.customer:
            customer = obj.sale_invoice.customer
            return f"{customer.first_name} {customer.last_name}" if customer.first_name and customer.last_name else 'نامشخص'
        return 'نامشخص'
    get_customer_name.short_description = 'نام مشتری'

    # متد برای نمایش تاریخ فروش
    def get_sale_date(self, obj):
        if obj.sale_invoice and obj.sale_invoice.sale_date:
            return obj.sale_invoice.sale_date.strftime('%Y-%m-%d')  # فرمت تاریخ میلادی
        return 'نامشخص'

    get_sale_date.short_description = 'تاریخ فروش'


    # تابع برای نمایش تصویر بند انگشتی
    def image_thumbnail(self, obj):
        if obj.image:
            img = Image.open(obj.image)
            img.thumbnail((50, 50))  # تنظیم سایز بند انگشتی (50x50)
            img_io = BytesIO()
            img.save(img_io, img.format)
            img_io.seek(0)
            content_type, encoding = mimetypes.guess_type(obj.image.name)
            content_type = content_type or 'image/jpeg'  # پیش فرض برای نوع تصویر
            thumbnail_image = InMemoryUploadedFile(img_io, 'ImageField', obj.image.name, content_type, img_io.tell(), None)
            image_url = obj.image.url if hasattr(obj.image, 'url') else ''
            return mark_safe(f'<img src="{image_url}" width="50" height="50" />')
        return 'بدون تصویر'
    image_thumbnail.short_description = 'تصویر بند انگشتی'


# -----------------------------------
@admin.register(CraftPiece)
class CraftPieceAdmin(admin.ModelAdmin):

    list_display = (
        'gold_type','image_thumbnail','name', 'code', 'net_weight',
         'is_sold','get_sale_date','get_customer_name',
    )
    search_fields = ('code','name',)
    list_filter = ('is_sold', 'gold_type',SaleDateFilter)
    ordering = ['-sale_invoice__sale_date']
    exclude = ('invoice', 'vitrin', 'sale_invoice')
    actions = ['export_as_excel']

    # متد برای نمایش نام خریدار
    def get_customer_name(self, obj):
        if obj.sale_invoice and obj.sale_invoice.customer:
            customer = obj.sale_invoice.customer
            # فرض بر اینکه فیلدهای first_name و last_name برای نام مشتری موجود است
            return f"{customer.first_name} {customer.last_name}" if customer.first_name and customer.last_name else 'نامشخص'
        return 'نامشخص'
    get_customer_name.short_description = 'نام خریدار'

    # متد برای نمایش تاریخ فروش
    def get_sale_date(self, obj):
        if obj.sale_invoice and obj.sale_invoice.sale_date:
            return obj.sale_invoice.sale_date.strftime('%Y-%m-%d')  # فرمت تاریخ میلادی
        return 'نامشخص'
    get_sale_date.short_description = 'تاریخ فروش'


    def image_thumbnail(self, obj):
        if obj.image:
            img = Image.open(obj.image)
            img.thumbnail((50, 50))  # تنظیم سایز بند انگشتی (50x50)
            img_io = BytesIO()
            img.save(img_io, img.format)
            img_io.seek(0)
            content_type, encoding = mimetypes.guess_type(obj.image.name)
            content_type = content_type or 'image/jpeg'  # پیش فرض برای نوع تصویر
            thumbnail_image = InMemoryUploadedFile(img_io, 'ImageField', obj.image.name, content_type, img_io.tell(), None)
            image_url = obj.image.url if hasattr(obj.image, 'url') else ''
            return mark_safe(f'<img src="{image_url}" width="50" height="50" />')
        return 'بدون تصویر'
    image_thumbnail.short_description = 'تصویر بند انگشتی'




# ------------------------------


class SaleInvoiceForm(forms.ModelForm):
    class Meta:
        model = SaleInvoice
        # به جای '__all__' از لیست فیلدها به صورت دستی استفاده می‌کنیم
        fields = [
            'invoice_serial',
            'customer',
            'companyseller',
            'sale_date',
            'sale_price',
            'discount',
            'net_sale_price',
            'sale_tax',
            'sale_dailyprice',
            'notes',
        ]
        widgets = {
            'invoice_serial': forms.Textarea(attrs={'style': 'width:200px; height:15px;'}),
            'sale_price': forms.NumberInput(attrs={'style': 'width:200px'}),
            'net_sale_price': forms.NumberInput(attrs={'style': 'width:200px'}),
            'discount': forms.NumberInput(attrs={'style': 'width:200px'}),
            'sale_tax': forms.NumberInput(attrs={'style': 'width:200px'}),
            'sale_dailyprice': forms.NumberInput(attrs={'style': 'width:200px'}),
            'notes': forms.Textarea(attrs={'style': 'width:200px; height:50px;'}),

        }


@admin.register(SaleInvoice)
class SaleInvoiceAdmin(admin.ModelAdmin):
    form = SaleInvoiceForm
    readonly_fields = ('formatted_total_paid',)  # ← اینجا تابع رو گذاشتیم
    autocomplete_fields = ['customer']
    list_display = (
        'customer',
        'companyseller',
        'sale_date',
        'invoice_serial',
        'formatted_sale_price',
        'formatted_discount',
        'formatted_net_sale_price'
    )
    list_filter = ('sale_date', 'companyseller',)
    search_fields = ('customer__first_name', 'customer__last_name')
    ordering = ('-sale_date',)

    def formatted_sale_price(self, obj):
        return self._format_currency_field(obj.sale_price)
    formatted_sale_price.short_description = 'جمع مبلغ فاکتور'

    def formatted_discount(self, obj):
        return self._format_currency_field(obj.discount)
    formatted_discount.short_description = 'تخفیف'

    def formatted_net_sale_price(self, obj):
        return self._format_currency_field(obj.net_sale_price)
    formatted_net_sale_price.short_description = 'خالص مبلغ فاکتور'

    def formatted_total_paid(self, obj):
        if obj.total_paid is not None:
            formatted_number = f"{obj.total_paid:,}"
            return format_html('<div style="width: 100px; direction: ltr; text-align: right;">{}</div>', formatted_number)
        return format_html('<div style="width: 100px;"></div>')
    formatted_total_paid.short_description = 'جمع پرداخت‌های مشتری'

    def _format_currency_field(self, value):
        if value is not None:
            formatted_number = f"{value:,}"
            return format_html('<div style="width: 100px; direction: ltr; text-align: right;">{}</div>', formatted_number)
        return format_html('<div style="width: 100px;"></div>')
# --------------------------------