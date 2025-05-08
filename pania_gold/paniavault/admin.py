from django.contrib import admin, messages
from .models import BuyRawInvoice,BuyScrapInvoice,ReciptMeltInvoice,ReciptCraftInvoice
from .models import Customer,Supplier








class CustomerAdmin(admin.ModelAdmin):
    list_display = ('last_name','first_name',  'customer_type', 'phone_number', 'city', 'total_gold_balance', 'total_gold_reserve')
    search_fields = ('first_name', 'last_name', 'mellicode', 'phone_number')
    list_filter = ('customer_type', 'city')
    ordering = ('last_name',)
# ----------------------------------




class SupplierAdmin(admin.ModelAdmin):
    list_display = ('last_name','first_name', 'phone_number',  'mellicode', 'phone', 'city', 'code_posti', 'address')
    list_filter = ('city',)
    search_fields = ('first_name', 'last_name', 'mellicode', 'phone_number')  # قابلیت جستجو
    ordering = ('last_name',)

    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    full_name.short_description = "نام کامل"



# ------------------------------------------

class BuyRawInvoiceAdmin(admin.ModelAdmin):
    list_display = (
         'supplier',  'invoice_date',
        'net_weight', 'invoice_price', 'notes'
    )
    search_fields = ('supplier__first_name', 'supplier__last_name')
    list_filter = ( 'supplier',  'companyseller', 'invoice_date')
    fieldsets = (
        (None, {
            'fields': ( 'supplier',  'companyseller', 'invoice_date')
        }),
        ('مالی', {
            'fields': ('net_weight', 'invoice_dailyprice', 'invoice_price', 'discount')
        }),
        ('توضیحات', {
            'fields': ('notes',)
        })
    )
    list_per_page = 20
# -------------------------------

class BuyScrapInvoiceAdmin(admin.ModelAdmin):
    list_display = (
         'customer',  'invoice_date',
        'net_weight','karat_weight' ,'invoice_price', 'notes'
    )
    search_fields = ('customer__first_name', 'customer__last_name' )
    list_filter = ( 'customer',  'companyseller', 'invoice_date')
    fieldsets = (
        (None, {
            'fields': ( 'customer',  'companyseller', 'invoice_date')
        }),
        ('مالی', {
            'fields': ('net_weight','karat_weight' , 'invoice_dailyprice', 'invoice_price', 'discount')
        }),
        ('توضیحات', {
            'fields': ('notes',)
        })
    )
    list_per_page = 20

# ----------------------------------
class ReciptMeltInvoiceAdmin(admin.ModelAdmin):
    list_display = ('supplier', 'invoice_date', 'net_weight', 'invoice_serial')
    search_fields = ('supplier__first_name', 'supplier__last_name', 'invoice_serial')  # اصلاح فیلد جستجو
    list_filter = ('supplier', 'invoice_date')
    fieldsets = (
        (None, {
            'fields': ('melt_type', 'supplier', 'invoice_date', 'invoice_serial')
        }),
        ('مالی', {
            'fields': ('net_weight',)
        }),
    )
    list_per_page = 20


# -------------------------------------------
class ReciptCraftInvoiceAdmin(admin.ModelAdmin):
    list_display = (
        'supplier', 'invoice_date', 'net_weight','invoice_serial'
    )
    search_fields = ('supplier__first_name', 'supplier__last_name')
    list_filter = ('supplier',  'invoice_date')
    fieldsets = (
        (None, {
            'fields': ('pay_type','supplier',  'invoice_date','invoice_serial','qty')
        }),
        ('مالی', {
            'fields': ('net_weight','accessory_weight','invoice_dailyprice','invoice_price','discount')
        }),
    )
    list_per_page = 20






admin.site.register(Customer, CustomerAdmin)
admin.site.register(Supplier, SupplierAdmin)
admin.site.register(BuyScrapInvoice, BuyScrapInvoiceAdmin)
admin.site.register(BuyRawInvoice, BuyRawInvoiceAdmin)
admin.site.register(ReciptMeltInvoice, ReciptMeltInvoiceAdmin)
admin.site.register(ReciptCraftInvoice, ReciptCraftInvoiceAdmin)