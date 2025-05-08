from django.db import models
from django_jalali.db import models as jmodels
from decimal import Decimal
from django.utils.timezone import now







# ==============================================
class SaleInvoicePayment(models.Model):
    saleinvoice = models.ForeignKey('vitrin.SaleInvoice', on_delete=models.CASCADE, related_name='salepayments', verbose_name='پرداختی فروش زینتی')
    amount =models.PositiveIntegerField( verbose_name='مبلغ پرداخت')
    discount = models.PositiveIntegerField(null=True, blank=True, verbose_name='تخفیف ')
    discount_code = models.CharField(max_length=20, null=True, blank=True, verbose_name='کد تخفیف')  # فیلد کد تخفیف
    etebar = models.PositiveIntegerField(null=True, blank=True, verbose_name='اعتبار ')
    etebar_code = models.CharField(max_length=20, null=True, blank=True, verbose_name='کد اعتبار')
    pay_date=jmodels.jDateField(verbose_name='تاریخ پرداخت')
    payment_method = models.CharField(max_length=50, choices=[('نقدی', 'نقدی'), ('اعتباری', 'اعتباری'),('تهاتر', 'تهاتر'),('تخفیف', 'تخفیف')], verbose_name='روش پرداخت')
    payment_explain = models.CharField(max_length=150, null=True, blank=True,verbose_name='شرح پرداخت')
    payment_receipt = models.CharField(max_length=50,  verbose_name='رسید پرداخت')


    def __str__(self):
        return f"پرداخت {self.amount} "

    class Meta:
        verbose_name = 'پرداخت فروش زینتی'
        verbose_name_plural = 'پرداختهای فروش زینتی'

# -------------------------------------------------------------
class SaleMeltInvoicePayment(models.Model):
    meltsaleinvoice = models.ForeignKey('meltvitrin.SaleMeltInvoice', on_delete=models.CASCADE, related_name='meltsalepayments', verbose_name='پرداختی فروش آبشده')
    amount =models.PositiveIntegerField( verbose_name='مبلغ پرداخت')
    discount = models.PositiveIntegerField(null=True, blank=True, verbose_name='تخفیف ')
    discount_code = models.CharField(max_length=20, null=True, blank=True, verbose_name='کد تخفیف')  # فیلد کد تخفیف
    etebar = models.PositiveIntegerField(null=True, blank=True, verbose_name='اعتبار ')
    etebar_code = models.CharField(max_length=20, null=True, blank=True, verbose_name='کد اعتبار')
    pay_date=jmodels.jDateField(null=True, blank=True,verbose_name='تاریخ پرداخت')
    payment_method = models.CharField(max_length=50, choices=[('نقدی', 'نقدی'), ('اعتباری', 'اعتباری'),('تهاتر', 'تهاتر'),('تخفیف', 'تخفیف')], verbose_name='روش پرداخت')
    payment_explain = models.CharField(max_length=150, null=True, blank=True,verbose_name='شرح پرداخت')
    payment_receipt = models.CharField(max_length=50,  verbose_name='رسید پرداخت')


    def __str__(self):
        return f"پرداخت {self.amount} "

    class Meta:
        verbose_name = 'پرداخت فروش آبشده'
        verbose_name_plural = 'پرداختهای فروش آبشده'

# ---------------------------------------------------------

class BuyRawInvoicePayment(models.Model):
    buyrawinvoice = models.ForeignKey('paniavault.BuyRawInvoice', on_delete=models.CASCADE, related_name='buyrawpayments', verbose_name='پرداختی خرید خام')
    amount =models.PositiveIntegerField( verbose_name='مبلغ پرداخت')
    discount = models.PositiveIntegerField(null=True, blank=True, verbose_name='تخفیف ')
    discount_code = models.CharField(max_length=20, null=True, blank=True, verbose_name='کد تخفیف')  # فیلد کد تخفیف
    pay_date=jmodels.jDateField(null=True, blank=True,verbose_name='تاریخ پرداخت')
    payment_method = models.CharField(max_length=50, choices=[('حساب رسمی', 'حساب رسمی'), ('حساب غیر رسمی', 'حساب غیر رسمی')], verbose_name='روش پرداخت')
    payment_place = models.CharField(max_length=150, null=True, blank=True, verbose_name='حساب پرداخت')
    payment_explain = models.CharField(max_length=150, null=True, blank=True,verbose_name='شرح پرداخت')
    payment_receipt = models.CharField(max_length=50,  verbose_name='رسید پرداخت')
    created_at = models.DateTimeField(default=now, verbose_name='تاریخ ایجاد')


    def __str__(self):
        return f"پرداخت {self.amount} "

    class Meta:
        verbose_name = 'پرداختی خرید خام'
        verbose_name_plural = 'پرداختیهای خرید خام'

# --------------------------------------------------------------


class OldPiecePayment(models.Model):
    oldpiece = models.ForeignKey('vitrin.OldPiece', on_delete=models.CASCADE, related_name='oldpiecepayments', verbose_name='پرداختی خرید مستعمل')
    amount =models.PositiveIntegerField( verbose_name='مبلغ پرداخت')
    discount = models.PositiveIntegerField(null=True, blank=True, verbose_name='تخفیف ')
    discount_code = models.CharField(max_length=20, null=True, blank=True, verbose_name='کد تخفیف')  # فیلد کد تخفیف
    pay_date=jmodels.jDateField(null=True, blank=True,verbose_name='تاریخ پرداخت')
    payment_method = models.CharField(max_length=50, choices=[('حساب رسمی', 'حساب رسمی'), ('حساب غیر رسمی', 'حساب غیر رسمی'),('تهاتر', 'تهاتر')], verbose_name='روش پرداخت')
    payment_place = models.CharField(max_length=150, null=True, blank=True, verbose_name='حساب پرداخت')
    payment_explain = models.CharField(max_length=150, null=True, blank=True,verbose_name='شرح پرداخت')
    payment_receipt = models.CharField(max_length=50,  verbose_name='رسید پرداخت')
    created_at = models.DateTimeField(default=now, verbose_name='تاریخ ایجاد')


    def __str__(self):
        return f"پرداخت {self.amount} "

    class Meta:
        verbose_name = 'پرداختی خرید مستعمل'
        verbose_name_plural = 'پرداختیهای خرید مستعمل'