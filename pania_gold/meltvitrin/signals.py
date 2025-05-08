from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from finance.models import SaleMeltInvoicePayment




@receiver(post_save, sender=SaleMeltInvoicePayment)
@receiver(post_delete, sender=SaleMeltInvoicePayment)
def update_invoice_total_paid(sender, instance, **kwargs):
    invoice = instance.meltsaleinvoice
    invoice.update_total_paid()
