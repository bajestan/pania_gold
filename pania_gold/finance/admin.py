
from .forms import SaleInvoicePaymentForm,MeltSaleInvoicePaymentForm,BuyrawInvoicePaymentForm,OldPiecePaymentForm
from django.contrib import admin
from .models import SaleInvoicePayment, SaleMeltInvoicePayment, BuyRawInvoicePayment, OldPiecePayment




# ---------------- SaleInvoicePayment -------------------
#
class SaleInvoicePaymentAdmin(admin.ModelAdmin):
    form = SaleInvoicePaymentForm
    list_display = ['saleinvoice', 'amount', 'payment_receipt', 'payment_method', 'pay_date']
    search_fields = ['saleinvoice__customer__last_name','saleinvoice__customer__first_name']
    list_filter = ['payment_method', 'pay_date']

    class Media:
        css = {
            'all': ('finance/css/custom_admin.css',)
        }


admin.site.register(SaleInvoicePayment, SaleInvoicePaymentAdmin)


# ---------------- SaleMeltInvoicePayment -------------------


class SaleMeltInvoicePaymentAdmin(admin.ModelAdmin):
    form = MeltSaleInvoicePaymentForm
    list_display = ['meltsaleinvoice', 'amount', 'payment_receipt', 'payment_method', 'pay_date']
    search_fields = ['meltsaleinvoice__customer__last_name', 'meltsaleinvoice__customer__first_name']
    list_filter = ['payment_method', 'pay_date']

    class Media:
        css = {
            'all': ('finance/css/custom_admin.css',)
        }

admin.site.register(SaleMeltInvoicePayment, SaleMeltInvoicePaymentAdmin)


# ---------------- BuyRawInvoicePayment -------------------
class BuyRawInvoicePaymentAdmin(admin.ModelAdmin):
    form = BuyrawInvoicePaymentForm
    list_display = ['buyrawinvoice', 'amount', 'payment_receipt', 'payment_method', 'pay_date']
    search_fields = ['buyrawinvoice__supplier__name']  # فرض بر این است که تأمین‌کننده فیلد نام دارد
    list_filter = ['payment_method', 'pay_date']

    class Media:
        css = {
            'all': ('finance/css/custom_admin.css',)
        }

admin.site.register(BuyRawInvoicePayment, BuyRawInvoicePaymentAdmin)

# ---------------- OldPiecePayment -------------------

class OldPiecePaymentAdmin(admin.ModelAdmin):
    form = OldPiecePaymentForm
    list_display = ['oldpiece', 'amount', 'payment_receipt', 'payment_method', 'pay_date']
    search_fields = ['oldpiece__seller__last_name', 'oldpiece__seller__first_name']  # فرض بر این است که فروشنده دارد
    list_filter = ['payment_method', 'pay_date']

    class Media:
        css = {
            'all': ('finance/css/custom_admin.css',)
        }

admin.site.register(OldPiecePayment, OldPiecePaymentAdmin)

# ------------------------------------------------