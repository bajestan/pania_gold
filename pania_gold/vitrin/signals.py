
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from finance.models import SaleInvoicePayment




@receiver(post_save, sender=SaleInvoicePayment)
@receiver(post_delete, sender=SaleInvoicePayment)
def update_invoice_total_paid(sender, instance, **kwargs):
    invoice = instance.saleinvoice
    invoice.update_total_paid()
