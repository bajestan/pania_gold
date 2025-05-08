from django.db import models
from django_jalali.db import models as jmodels
from decimal import Decimal
from django.utils.timezone import now
from finance.models import SaleInvoicePayment





class CompanyVitrin(models.Model):
    VITRIN_TYPE = [
        ('vitrin', 'بجستان'),
        ('safebox', 'تهران'),

    ]
    vitrin_type = models.CharField(max_length=20,null=True, blank=True, choices=VITRIN_TYPE, verbose_name='نوع ویترین')
    vitrin_balance=models.DecimalField(max_digits=20,decimal_places=3,default=Decimal('0.00'), verbose_name='موجودی ویترین')
    vitrin_ojrat_balance = models.DecimalField(max_digits=20, decimal_places=3, default=Decimal('0.00'),
                                         verbose_name='موجودی اجرت ویترین')
    vitrin_assets =models.DecimalField(max_digits=20,decimal_places=3,default=Decimal('0.00'),null=True, blank=True, verbose_name='دارایی ویترین')
    notes = models.TextField(blank=True, null=True, verbose_name='شرح')
    created_at = models.DateTimeField(default=now, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(default=now, verbose_name='تاریخ به‌روزرسانی')
    def __str__(self):
        return f"فاکتور فروش  {self.vitrin_balance}"








# ==============CRAFTED GOLD  زینتی ================================
# ------------------------  فاکتور فروش زینتی و مستعمل      -----------------------------
class SaleInvoice(models.Model):
    customer = models.ForeignKey('paniavault.Customer', on_delete=models.CASCADE, verbose_name='مشتری')
    companyseller = models.ForeignKey('accounts.CompanySeller', on_delete=models.CASCADE, null=True, blank=True, verbose_name='کارشناس فروش')
    invoice_serial = models.TextField(null=True, blank=True, verbose_name='سریال فاکتور')
    sale_date = jmodels.jDateField(verbose_name='تاریخ فاکتور', null=True, blank=True)
    sale_dailyprice = models.PositiveIntegerField(null=True, blank=True, verbose_name='نرخ روز فروش')
    sale_price = models.BigIntegerField(null=True, blank=True, verbose_name='جمع مبلغ فاکتور')
    discount = models.IntegerField(null=True, blank=True, verbose_name='تخفیف')
    net_sale_price = models.BigIntegerField(null=True, blank=True, verbose_name='خالص مبلغ فاکتور')
    sale_tax = models.BigIntegerField(null=True, blank=True, verbose_name='جمع مالیات')
    notes = models.TextField(blank=True, null=True, verbose_name='شرح')
    total_paid = models.BigIntegerField(default=0, verbose_name='جمع پرداخت‌های مشتری')

    def __str__(self):
        return f" {self.customer} - {self.invoice_serial}"

    class Meta:
        verbose_name = "فاکتور فروش زینتی و مستعمل"
        verbose_name_plural = "فاکتورهای فروش زینتی و مستعمل "

    def update_total_paid(self):
        self.total_paid = sum(payment.amount or 0 for payment in self.salepayments.all())
        self.save()


# -----------------------------------------


def calculate_sale_price(netWeight, saleOjrat, saleDailyPrice,sale_price_ojrat, seller_profit_percent=7):
    # تبدیل مقادیر به Decimal
    netWeight = Decimal(str(netWeight))
    saleOjrat = Decimal(str(saleOjrat))
    saleDailyPrice = Decimal(str(saleDailyPrice))
    sale_price_ojrat = Decimal(str(sale_price_ojrat))
    seller_profit_percent = Decimal(str(seller_profit_percent)) / 100  # تبدیل به درصد

    j8 = netWeight * (1 + (saleOjrat / 100))
    j10 = j8 * (1 + seller_profit_percent)  # اجرت فروشنده
    j14 = j10 * saleDailyPrice
    m6 = netWeight * saleDailyPrice
    m10 = (saleOjrat / 100) * m6
    m12 = (m6 + m10) * seller_profit_percent  # تبدیل 0.07 به Decimal
    saleTax = (m12 + m10) * Decimal('0.1')  # مالیات ارزش افزوده
    salePrice = j14 + saleTax + sale_price_ojrat
    print(
        f"netWeight={netWeight}, saleOjrat={saleOjrat}, saleDailyPrice={saleDailyPrice}, sale_price_ojrat={sale_price_ojrat}, seller_profit_percent={seller_profit_percent}")

    return {
        'sale_price': round(salePrice),
        'sale_tax': round(saleTax)
    }


# ----------------------------------------

def upload_to_craft(instance, filename):
    return f'craftedgold_image/{filename}'

class CraftPiece(models.Model):
    # نام اول دسته بندی برای تولید کد حروف مشابه نباشد
    CATEGORY = [
        ('ring', 'انگشتر'),
        ('set', 'ست و نیم ست'),
        ('minimal', 'مینیمال'),
        ('earring', 'گوشواره'),
        ('bracelet', 'دستبند'),
        ('necklace', 'گردنبند'),
        ('kids', 'کودک'),
        ('coin', 'سکه'),
    ]
    invoice = models.ForeignKey('paniavault.ReciptCraftInvoice', on_delete=models.CASCADE, verbose_name='فاکتور بنکدار',related_name='craft_pieces')
    vitrin = models.ForeignKey(CompanyVitrin, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='ویترین', related_name='craft_vitrin')
    sale_invoice = models.ForeignKey(SaleInvoice, on_delete=models.SET_NULL, null=True, blank=True, related_name='crafted_golds', verbose_name='فاکتور فروش زینتی')
    gold_type = models.CharField(max_length=50, choices=CATEGORY,null=True, blank=True, verbose_name='دسته بندی')
    code = models.CharField(max_length=100,unique=True, null=True, blank=True, verbose_name='کد کار')
    name = models.CharField(max_length=100, null=True, blank=True, verbose_name='نام کالا')
    net_weight = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True,verbose_name='وزن خالص')
    weight_with_accessory = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True,verbose_name='وزن با متعلقات')

    supplier = models.ForeignKey('paniavault.Supplier', on_delete=models.CASCADE, null=True, blank=True, verbose_name='تأمین‌کننده',related_name='craftedpiece_supllier')
    buy_price = models.IntegerField(null=True, blank=True, verbose_name='قیمت خرید')
    buy_date = jmodels.jDateField(verbose_name='تاریخ خرید', null=True, blank=True)
    buy_ojrat = models.DecimalField(max_digits=15, decimal_places=1, null=False, blank=True,default=0, verbose_name='اجرت خرید')
    buy_price_ojrat = models.IntegerField(default=0, verbose_name='اجرت ریالی خرید')
    buy_dailyprice = models.PositiveIntegerField(null=True, blank=True, verbose_name='نرخ روز خرید')

    sale_price = models.IntegerField(null=True, blank=True, verbose_name='قیمت فروش')
    sale_date = jmodels.jDateField(verbose_name='تاریخ فروش', null=True, blank=True)
    seller_profit_percent = models.DecimalField(max_digits=5, decimal_places=1,default=7.0,verbose_name='درصد سود فروشنده')
    sale_ojrat = models.DecimalField(max_digits=15, decimal_places=1, null=False, blank=True,default=0, verbose_name='اجرت فروش')
    sale_price_ojrat = models.IntegerField(default=0, verbose_name='اجرت ریالی فروش')
    sale_tax = models.IntegerField(null=True, blank=True,verbose_name='مالیات فروش')
    notes = models.TextField(blank=True, null=True, verbose_name='شرح')
    is_sold= models.BooleanField(default=False, verbose_name='وضعیت فروش')
    created_at = models.DateTimeField(default=now, verbose_name='تاریخ ایجاد')
    image = models.ImageField(upload_to=upload_to_craft, blank=True, null=True, verbose_name='تصویر بند انگشتی')

    def save(self, *args, **kwargs):
        if self.sale_invoice and self.net_weight is not None and self.sale_ojrat is not None and self.sale_price_ojrat is not None and self.sale_invoice.sale_dailyprice:
            result = calculate_sale_price(self.net_weight, self.sale_ojrat, self.sale_invoice.sale_dailyprice,self.sale_price_ojrat, self.seller_profit_percent)
            sale_price = result.get('sale_price', 0)
            sale_tax = result.get('sale_tax', 0)
            try:
                self.sale_price = int(float(sale_price)) if sale_price is not None else 0
                self.sale_tax = int(float(sale_tax)) if sale_tax is not None else 0
            except (ValueError, TypeError) as e:
                self.sale_price = 0
                self.sale_tax = 0
                print(f"Error converting sale_price or sale_tax to int: {e}")
        super().save(*args, **kwargs)


    def get_type(self):
        return "craft"
    
    def __str__(self):
        return f" {self.name}  کد {self.code}  "

    class Meta:
        verbose_name = 'طلای زینتی'
        verbose_name_plural = 'ویترین زینتی'

# ======================== OLD GOLD طلای مستعمل  ==============

def upload_to_old(instance, filename):
    return f'oldgold_image/{filename}'

class OldPiece(models.Model):
    sale_invoice = models.ForeignKey(SaleInvoice, on_delete=models.SET_NULL, null=True, blank=True, related_name='old_gold', verbose_name='فاکتور فروش مستعمل')
    vitrin = models.ForeignKey(CompanyVitrin, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='ویترین',related_name='old_vitrin')
    code = models.CharField(max_length=100,unique=True, null=True, blank=True, verbose_name='کد کار')
    name = models.CharField(max_length=100, null=True, blank=True, verbose_name='نام کالا')
    net_weight = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True,verbose_name='وزن خالص')
    weight_with_accessory = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True,verbose_name='وزن با متعلقات')

    supplier = models.ForeignKey('paniavault.Customer', on_delete=models.CASCADE, null=True, blank=True, verbose_name='تأمین‌کننده',related_name='old_supllier')
    buy_price = models.IntegerField(null=True, blank=True, verbose_name='قیمت خرید')
    buy_date = jmodels.jDateField(verbose_name='تاریخ خرید', null=True, blank=True)
    buy_dailyprice = models.PositiveIntegerField(null=True, blank=True, verbose_name='نرخ روز خرید')

    sale_price = models.IntegerField(null=True, blank=True, verbose_name='قیمت فروش')
    sale_date = jmodels.jDateField(verbose_name='تاریخ فروش', null=True, blank=True)
    seller_profit_percent = models.DecimalField(max_digits=5, decimal_places=1, default=7.0,verbose_name='درصد سود فروشنده')
    sale_ojrat = models.DecimalField(max_digits=15, decimal_places=1, null=False, blank=True, default=0, verbose_name='اجرت فروش')
    sale_price_ojrat = models.IntegerField(default=0, verbose_name='اجرت ریالی فروش')
    sale_tax = models.IntegerField(null=True, blank=True,verbose_name='مالیات فروش')
    notes = models.TextField(blank=True, null=True, verbose_name='شرح')
    is_sold= models.BooleanField(default=False, verbose_name='وضعیت فروش')
    created_at = models.DateTimeField(default=now, verbose_name='تاریخ ایجاد')
    image = models.ImageField(upload_to=upload_to_old, blank=True, null=True, verbose_name='تصویر بند انگشتی')

    def save(self, *args, **kwargs):
        if self.sale_invoice and self.net_weight is not None and self.sale_ojrat is not None and self.sale_invoice.sale_dailyprice:
            result = calculate_sale_price(self.net_weight, self.sale_ojrat, self.sale_invoice.sale_dailyprice,self.sale_price_ojrat, self.seller_profit_percent)
            sale_price = result.get('sale_price', 0)
            sale_tax = result.get('sale_tax', 0)
            try:
                self.sale_price = int(float(sale_price)) if sale_price is not None else 0
                self.sale_tax = int(float(sale_tax)) if sale_tax is not None else 0
            except (ValueError, TypeError) as e:
                self.sale_price = 0
                self.sale_tax = 0
                print(f"Error converting sale_price or sale_tax to int: {e}")
        super().save(*args, **kwargs)

    def get_type(self):
        return "old"

    def __str__(self):
        return f" {self.net_weight}"

    class Meta:
        verbose_name = 'طلای  مستعمل'
        verbose_name_plural = 'ویترین مستعمل'

# --------------------------------------