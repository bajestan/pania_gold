from django.contrib import admin
from .models import MeltPiece,SaleMeltInvoice
from paniavault.models import Customer,Supplier
from django.utils.html import mark_safe
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import mimetypes






# ----------------------------------------------

@admin.register(SaleMeltInvoice)
class SaleMeltInvoiceAdmin(admin.ModelAdmin):
    list_display = ( 'customer', 'companyseller', 'sale_date', 'total_sale_price', 'sale_tax', 'discount')
    list_filter = ('sale_date','companyseller',)
    search_fields = ('customer__first_name', 'customer__last_name')
    ordering = ('customer',)


# -------------------------------------------
@admin.register(MeltPiece)
class MeltPieceAdmin(admin.ModelAdmin):
    list_display = (
        'name','code','net_weight','weight','karat','ang_number','lab_name', 'supplier', 'is_sold'
    )
    search_fields = ('code','name',)
    list_filter = ('is_sold', 'sale_invoice', 'supplier',)
    ordering = ('created_at',)
    exclude = ('invoice', 'vitrin','sale_invoice')

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super().get_readonly_fields(request, obj)
        if obj:
            readonly_fields = list(readonly_fields) + ['net_weight']
        return readonly_fields

