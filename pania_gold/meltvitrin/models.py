from django.db import models
from django_jalali.db import models as jmodels
from decimal import Decimal
from django.utils.timezone import now







class SaleMeltInvoice(models.Model):
    customer = models.ForeignKey('paniavault.Customer', on_delete=models.CASCADE, verbose_name='مشتری')
    companyseller = models.ForeignKey('accounts.CompanySeller', on_delete=models.CASCADE, null=True, blank=True, verbose_name='کارشناس فروش')
    sale_date = jmodels.jDateField(verbose_name='تاریخ فاکتور', null=True, blank=True)
    sale_dailyprice = models.PositiveIntegerField(null=True, blank=True, verbose_name='نرخ روز فروش')
    total_sale_price = models.BigIntegerField(null=True, blank=True, verbose_name='مجموع مبلغ فاکتور')
    sale_tax = models.BigIntegerField(null=True, blank=True, verbose_name='جمع مالیات')
    discount = models.IntegerField(null=True, blank=True, verbose_name='تخفیف')
    notes = models.TextField(blank=True, null=True, verbose_name='شرح')
    total_paid = models.BigIntegerField(default=0, verbose_name='جمع پرداخت‌های مشتری')

    def __str__(self):
        return f"فاکتور فروش  {self.customer} - {self.sale_date}"
    class Meta:
        verbose_name = "فاکتور فروش آبشده"
        verbose_name_plural = "فاکتورهای فروش آبشده"

    def update_total_paid(self):
        self.total_paid = sum(payment.amount or 0 for payment in self.meltsalepayments.all())
        self.save()
# ---------------------------------------------------------


def upload_to_melt(instance, filename):
    return f'meltgold_image/{filename}'

class MeltPiece(models.Model):
    sale_invoice = models.ForeignKey(SaleMeltInvoice, on_delete=models.SET_NULL, null=True, blank=True,related_name='melt_golds', verbose_name='فاکتور فروش آبشده')
    invoice = models.ForeignKey('paniavault.ReciptMeltInvoice',on_delete=models.CASCADE,verbose_name='فاکتور بنکدار',related_name='melt_pieces')
    vitrin = models.ForeignKey('vitrin.CompanyVitrin', on_delete=models.SET_NULL,null=True, blank=True, verbose_name='ویترین', related_name='melt_vitrin')
    supplier = models.ForeignKey('paniavault.Supplier', on_delete=models.CASCADE, null=True, blank=True,
                                 verbose_name='تأمین‌کننده', related_name='meltpiece_supllier')
    piece_type = models.CharField(max_length=20,choices=[('آبشده', 'آبشده'), ('امانی', 'امانی')],default='آبشده',verbose_name='نوع قطعه')

    name = models.CharField(max_length=50, null=True, blank=True,default='آبشده', verbose_name='نام کالا')
    code = models.CharField(max_length=50, unique=True, null=True, blank=True, verbose_name='کد کار')
    net_weight = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'),verbose_name='وزن عیار 750')
    weight = models.DecimalField(max_digits=10,decimal_places=2,verbose_name='وزن قطعه')
    karat = models.DecimalField(max_digits=3,decimal_places=0,verbose_name='عیارقطعه' )
    ang_number = models.CharField(max_length=50,blank=True,null=True,verbose_name='شماره انگ')
    lab_name = models.CharField( max_length=100,blank=True,null=True,verbose_name='نام آزمایشگاه')
    is_sold = models.BooleanField(default=False, verbose_name='وضعیت فروش')

    sale_price = models.IntegerField(null=True, blank=True, verbose_name='قیمت فروش')
    sale_date = jmodels.jDateField(verbose_name='تاریخ فروش', null=True, blank=True)
    sale_ojrat = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True, verbose_name='اجرت فروش')
    sale_tax = models.IntegerField(null=True, blank=True, verbose_name='مالیات فروش')

    additional_info = models.TextField(verbose_name='اطلاعات اضافی',blank=True,null=True )
    image = models.ImageField(upload_to=upload_to_melt, blank=True, null=True, verbose_name='تصویر بند انگشتی')
    created_at = models.DateTimeField(default=now, verbose_name='تاریخ ایجاد')
    def __str__(self):
        return f"قطعه {self.ang_number} ({self.weight} گرم - {self.karat} عیار)"


    def get_type(self):
        return "melt"


    class Meta:
        verbose_name = 'طلای آبشده'
        verbose_name_plural = 'ویترین آبشده'