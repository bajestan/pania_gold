from django.db.models.signals import pre_save,post_save, post_delete
from django.dispatch import receiver
from decimal import Decimal
from .models import BuyRawInvoice,BuyScrapInvoice, ReciptMeltInvoice,ReciptCraftInvoice






# --------------------------------
@receiver(pre_save, sender=BuyRawInvoice)
def store_previous_weight(sender, instance, **kwargs):
    # مقدار قبلی وزن را ذخیره می‌کنیم
    if instance.pk:
        try:
            instance._previous_weight = instance.__class__.objects.get(pk=instance.pk).net_weight
        except BuyRawInvoice.DoesNotExist:
            instance._previous_weight = Decimal('0.00')
    else:
        instance._previous_weight = Decimal('0.00')


# سیگنال برای به‌روزرسانی ولت هنگام ذخیره فاکتور
@receiver(post_save, sender=BuyRawInvoice)
def update_vault_on_invoice_save(sender, instance, created, **kwargs):
    if instance.vault and instance.net_weight is not None:
        vault = instance.vault
        previous_weight = getattr(instance, '_previous_weight', Decimal('0.00'))
        if created:
            weight_difference = Decimal(instance.net_weight)
        else:
            weight_difference = Decimal(instance.net_weight) - Decimal(previous_weight)
        vault.company_balance = (vault.company_balance or Decimal('0.00')) + weight_difference
        vault.company_assets = (vault.company_assets or Decimal('0.00')) + weight_difference
        vault.save()

# ------------------------------
# سیگنال برای به‌روزرسانی ولت هنگام حذف فاکتور
@receiver(post_delete, sender=BuyRawInvoice)
def update_vault_on_invoice_delete(sender, instance, **kwargs):
    if instance.vault and instance.net_weight is not None:
        vault = instance.vault
        vault.company_balance = (vault.company_balance or Decimal('0')) - Decimal(instance.net_weight)
        vault.company_assets = (vault.company_assets or Decimal('0')) - Decimal(instance.net_weight)
        vault.save()


# =================قیچی ==============================

@receiver(pre_save, sender=BuyScrapInvoice)
def store_previous_weight(sender, instance, **kwargs):
    # مقدار قبلی وزن را ذخیره می‌کنیم
    if instance.pk:
        try:
            instance._previous_weight = instance.__class__.objects.get(pk=instance.pk).net_weight
        except BuyScrapInvoice.DoesNotExist:
            instance._previous_weight = Decimal('0.00')
    else:
        instance._previous_weight = Decimal('0.00')


# سیگنال برای به‌روزرسانی ولت هنگام ذخیره فاکتور
@receiver(post_save, sender=BuyScrapInvoice)
def update_vault_on_invoice_save(sender, instance, created, **kwargs):
    if instance.vault and instance.net_weight is not None:
        vault = instance.vault
        previous_weight = getattr(instance, '_previous_weight', Decimal('0.00'))
        if created:
            weight_difference = Decimal(instance.net_weight)
        else:
            weight_difference = Decimal(instance.net_weight) - Decimal(previous_weight)
        vault.company_balance = (vault.company_balance or Decimal('0.00')) + weight_difference
        vault.company_assets = (vault.company_assets or Decimal('0.00')) + weight_difference
        vault.save()

# ------------------------------
# سیگنال برای به‌روزرسانی ولت هنگام حذف فاکتور
@receiver(post_delete, sender=BuyScrapInvoice)
def update_vault_on_invoice_delete(sender, instance, **kwargs):
    if instance.vault and instance.net_weight is not None:
        vault = instance.vault
        vault.company_balance = (vault.company_balance or Decimal('0')) - Decimal(instance.net_weight)
        vault.company_assets = (vault.company_assets or Decimal('0')) - Decimal(instance.net_weight)
        vault.save()

# ============================  آبشده  =================

@receiver(pre_save, sender=ReciptMeltInvoice)
def store_previous_melt_weight(sender, instance, **kwargs):
    # مقدار قبلی وزن خالص را ذخیره می‌کنیم
    if instance.pk:
        try:
            instance._previous_weight = instance.__class__.objects.get(pk=instance.pk).net_weight
        except ReciptMeltInvoice.DoesNotExist:
            instance._previous_weight = Decimal('0.00')
    else:
        instance._previous_weight = Decimal('0.00')

# ----------------------------
@receiver(post_save, sender=ReciptMeltInvoice)
def update_vault_on_melt_invoice_save(sender, instance, created, **kwargs):
    if instance.vault and instance.net_weight is not None:
        vault = instance.vault
        previous_weight = getattr(instance, '_previous_weight', Decimal('0.00'))
        if created:
            weight_difference = Decimal(instance.net_weight)
        else:
            weight_difference = Decimal(instance.net_weight) - Decimal(previous_weight)
        vault.company_balance = (vault.company_balance or Decimal('0.00')) - weight_difference  # کاهش از موجودی
        vault.company_assets = (vault.company_assets or Decimal('0.00')) - weight_difference  # کاهش از دارایی
        vault.save()
# --------------------------------

@receiver(post_delete, sender=ReciptMeltInvoice)
def update_vault_on_melt_invoice_delete(sender, instance, **kwargs):
    if instance.vault and instance.net_weight is not None:
        vault = instance.vault
        vault.company_balance = (vault.company_balance or Decimal('0')) + Decimal(instance.net_weight)  # کاهش از موجودی
        vault.company_assets = (vault.company_assets or Decimal('0')) + Decimal(instance.net_weight)  # کاهش از دارایی
        vault.save()

# =============================== زینتی =========================


@receiver(pre_save, sender=ReciptCraftInvoice)
def store_previous_craft_weight(sender, instance, **kwargs):
    # مقدار قبلی وزن خالص را ذخیره می‌کنیم
    if instance.pk:
        try:
            instance._previous_weight = instance.__class__.objects.get(pk=instance.pk).net_weight
        except ReciptCraftInvoice.DoesNotExist:
            instance._previous_weight = Decimal('0.00')
    else:
        instance._previous_weight = Decimal('0.00')

# ----------------------------
@receiver(post_save, sender=ReciptCraftInvoice)
def update_vault_on_craft_invoice_save(sender, instance, created, **kwargs):
    if instance.vault and instance.net_weight is not None:
        vault = instance.vault
        previous_weight = getattr(instance, '_previous_weight', Decimal('0.00'))
        if created:
            weight_difference = Decimal(instance.net_weight)
        else:
            weight_difference = Decimal(instance.net_weight) - Decimal(previous_weight)
        vault.company_balance = (vault.company_balance or Decimal('0.00')) - weight_difference  # کاهش از موجودی
        vault.company_assets = (vault.company_assets or Decimal('0.00')) - weight_difference  # کاهش از دارایی
        vault.save()
# --------------------------------

@receiver(post_delete, sender=ReciptCraftInvoice)
def update_vault_on_craft_invoice_delete(sender, instance, **kwargs):
    if instance.vault and instance.net_weight is not None:
        vault = instance.vault
        vault.company_balance = (vault.company_balance or Decimal('0')) + Decimal(instance.net_weight)  # کاهش از موجودی
        vault.company_assets = (vault.company_assets or Decimal('0')) + Decimal(instance.net_weight)  # کاهش از دارایی
        vault.save()