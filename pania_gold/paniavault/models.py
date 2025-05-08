from django.db import models
from django_jalali.db import models as jmodels
from decimal import Decimal
from django.utils.timezone import now
from django.core.exceptions import ValidationError
import re






class Supplier(models.Model):
    first_name = models.CharField(max_length=50, verbose_name='نام', null=True, blank=True)
    last_name = models.CharField(max_length=50, verbose_name='نام خانوادگی', null=True, blank=True)
    mellicode = models.CharField(max_length=10, blank=True, null=True,verbose_name='کد ملی')
    phone = models.CharField(max_length=11, verbose_name='شماره ثابت', null=True, blank=True)
    phone_number = models.CharField(max_length=11, verbose_name='تلفن همراه', null=False, blank=False)
    city= models.CharField(max_length=50,verbose_name='شهر', null=True, blank=True)
    code_posti = models.CharField(max_length=15, verbose_name='کدپستی', null=True, blank=True)
    address = models.CharField(max_length=150, verbose_name='آدرس', null=True, blank=True)

    class Meta:
        verbose_name = "تامین کننده"
        verbose_name_plural = "تامین کنندگان"

    def __str__(self):
        return f'{self.first_name} {self.last_name} '

    def clean(self):
        # اعتبارسنجی شماره تلفن همراه
        if self.phone_number:
            mobile_regex = r"^09\d{9}$"
            if not re.match(mobile_regex, self.phone_number):
                raise ValidationError("شماره تلفن را درست وارد نمایید")

# --------------------------------------------
class Customer(models.Model):
    CUSTOMER_TYPE_CHOICES = [
        ('individual', 'حقیقی'),
        ('company', 'حقوقی'),
    ]
    customer_type = models.CharField(max_length=20, choices=CUSTOMER_TYPE_CHOICES, verbose_name='نوع مشتری')
    first_name = models.CharField(max_length=50, verbose_name='نام', null=True, blank=True)
    last_name = models.CharField(max_length=50, verbose_name='نام خانوادگی', null=True, blank=True)
    mellicode = models.CharField(max_length=10, unique=True, blank=True, null=True, verbose_name='کد ملی')
    melliserail = models.CharField(max_length=11, unique=True, blank=True, null=True, verbose_name='شناسه ملی شرکت')
    phone = models.CharField(max_length=11, verbose_name='شماره ثابت', null=True, blank=True)
    phone_number = models.CharField(max_length=11, verbose_name='تلفن همراه', null=True, blank=True)
    city = models.CharField(max_length=50, verbose_name='شهر', null=True, blank=True)
    code_posti = models.CharField(max_length=15, verbose_name='کدپستی', null=True, blank=True)
    address = models.CharField(max_length=150, verbose_name='آدرس', null=True, blank=True)
    total_gold_balance = models.DecimalField(max_digits=20, decimal_places=3, default=0, verbose_name='موجودی طلای مشتری')
    total_gold_reserve = models.DecimalField(max_digits=20, decimal_places=3, default=0, verbose_name='موجودی طلای امانی')

    class Meta:
        verbose_name = "مشتری"
        verbose_name_plural = "مشتریان"

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def clean(self):
        # اعمال اعتبارسنجی فقط برای مشتریان حقیقی
        if self.customer_type == 'individual':
            # اعتبارسنجی کد ملی
            if self.mellicode:
                if len(self.mellicode) != 10 or not self.mellicode.isdigit():
                    raise ValidationError("کد ملی باید شامل ۱۰ رقم باشد")
                digits = [int(digit) for digit in self.mellicode]
                checksum = sum(digits[i] * (10 - i) for i in range(9))
                rem = checksum % 11
                if rem < 2:
                    if digits[9] != rem:
                        raise ValidationError("کد ملی وارد شده معتبر نیست")
                else:
                    if digits[9] != (11 - rem):
                        raise ValidationError("کد ملی وارد شده معتبر نیست")
            # اعتبارسنجی شماره همراه
            if self.phone_number:
                mobile_regex = r"^09\d{9}$"
                if not re.match(mobile_regex, self.phone_number):
                    raise ValidationError("شماره تلفن همراه معتبر نیست")

    def save(self, *args, **kwargs):
        self.full_clean()  # اجرای اعتبارسنجی‌ها قبل از ذخیره
        super().save(*args, **kwargs)


# ======================== ولت شرکت ==========================
class CompanyVault(models.Model):
    company_balance=models.DecimalField(max_digits=20,decimal_places=3,default=Decimal('0.00'), verbose_name='موجودی شرکت')
    company_assets =models.DecimalField(max_digits=20,decimal_places=3,default=Decimal('0.00'),null=True, blank=True, verbose_name='دارایی شرکت')
    notes = models.TextField(blank=True, null=True, verbose_name='شرح')
    created_at = models.DateTimeField(default=now, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(default=now, verbose_name='تاریخ به‌روزرسانی')
    def __str__(self):
        return f"فاکتور فروش  {self.company_balance}"




# =========================================  فاکتور خرید طلای خام        =======================
class BuyRawInvoice(models.Model):
    SUPPLY_TYPE_CHOICES = (
        ('gallery', 'گالری'),
        ('platform', 'پلتفرم'),
    )
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, null=True, blank=True, verbose_name='تأمین‌کننده', related_name='raw_supllier')
    vault = models.ForeignKey(CompanyVault, on_delete=models.CASCADE, verbose_name='ولت شرکت',related_name='raw_vault', default=1)
    companyseller = models.ForeignKey('accounts.CompanySeller', on_delete=models.CASCADE, verbose_name='کارشناس فروش')
    invoice_date = jmodels.jDateField(verbose_name='تاریخ فاکتور', null=True, blank=True)
    net_weight = models.DecimalField(max_digits=10, decimal_places=2,default=Decimal('0.00'), verbose_name='وزن خالص فاکتور')
    invoice_dailyprice = models.PositiveIntegerField(null=True, blank=True, verbose_name='نرخ روز طلا')
    invoice_price = models.BigIntegerField(null=True, blank=True, verbose_name='مبلغ فاکتور')
    discount = models.IntegerField(null=True, blank=True, verbose_name='تخفیف')
    notes = models.TextField(blank=True, null=True, verbose_name='شرح')
    supply_type = models.CharField(max_length=15,choices=SUPPLY_TYPE_CHOICES,default='gallery',verbose_name='نوع تأمین')
    created_at = models.DateTimeField(default=now,  verbose_name='تاریخ ایجاد')
    def __str__(self):
        return f"فاکتور خرید طلای خام از بنکدار  {self.supplier} - {self.invoice_date}"

    class Meta:
        verbose_name = 'تامین طلای خام'
        verbose_name_plural = 'تامین های طلای خام'
# ==================== قیچی =================================

class BuyScrapInvoice(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True, verbose_name='تأمین‌کننده', related_name='scrap_customer')
    vault = models.ForeignKey(CompanyVault, on_delete=models.CASCADE, verbose_name='ولت شرکت',related_name='scrap_vault', default=1)
    companyseller = models.ForeignKey('accounts.CompanySeller', on_delete=models.CASCADE, verbose_name='کارشناس فروش')
    invoice_date = jmodels.jDateField(verbose_name='تاریخ فاکتور', null=True, blank=True)
    net_weight = models.DecimalField(max_digits=10, decimal_places=2,default=Decimal('0.00'), verbose_name='وزن ترازو')
    karat_weight = models.DecimalField(max_digits=10, decimal_places=2,null=True, blank=True,verbose_name='وزن عیار 740')
    invoice_dailyprice = models.PositiveIntegerField(null=True, blank=True, verbose_name='نرخ روز طلا')
    invoice_price = models.BigIntegerField(null=True, blank=True, verbose_name='مبلغ فاکتور')
    discount = models.IntegerField(null=True, blank=True, verbose_name='تخفیف')
    notes = models.TextField(blank=True, null=True, verbose_name='شرح')
    created_at = models.DateTimeField(default=now,  verbose_name='تاریخ ایجاد')
    def __str__(self):
        return f"فاکتور خرید طلای قیچی  {self.customer} - {self.invoice_date}"

    class Meta:
        verbose_name = 'فاکتور تامین قیچی'
        verbose_name_plural = 'فاکتورهای تامین قیچی'


# =============================فاکتوردریافت آبشده از تامین ====================
class ReciptMeltInvoice(models.Model):
    MELTTYPE = [
        ('vault', 'برداشت از ولت'),
        ('scrap', 'تهاترباقیچی'),
    ]
    melt_type = models.CharField(max_length=50, choices=MELTTYPE,null=True, blank=True, verbose_name='روش تامین')
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, null=True, blank=True, verbose_name='تأمین‌کننده',related_name='melt_supllier')
    vault = models.ForeignKey(CompanyVault, on_delete=models.CASCADE, verbose_name='ولت شرکت',null=False, blank=False, related_name='melt_vault')
    invoice_date = jmodels.jDateField(verbose_name='تاریخ فاکتور', null=True, blank=True)
    invoice_serial = models.CharField(max_length=20,verbose_name='سریال فاکتور', null=True, blank=True)
    net_weight = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'),verbose_name='وزن خالص فاکتور')
    created_at = models.DateTimeField(default=now, verbose_name='تاریخ ایجاد')
    def __str__(self):
        return f"فاکتور آب‌شده - {self.invoice_date}"

    class Meta:
        verbose_name = 'فاکتور تامین آبشده'
        verbose_name_plural = 'فاکتورهای تامین آبشده'

# ======================== کلیات فاکتور تامین زینتی از بنکدار  ======================

class ReciptCraftInvoice(models.Model):
    PAYTYPE = [
        ('vault', 'برداشت از ولت'),
        ('melt', 'تهاتر با آبشده'),
        ('both', 'هردو'),
    ]
    pay_type = models.CharField(max_length=50, choices=PAYTYPE, verbose_name='نوع پرداخت')
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, null=True, blank=True, verbose_name='تأمین‌کننده',related_name='whole_supllier')
    vault = models.ForeignKey(CompanyVault, on_delete=models.CASCADE, null=True, blank=True, verbose_name='ولت شرکت',related_name='whole_vault')
    companyseller = models.ForeignKey('accounts.CompanySeller', on_delete=models.CASCADE, verbose_name='کارشناس شرکت')
    invoice_serial = models.CharField(max_length=100,  null=True, blank=True, verbose_name='سریال فاکتور')
    invoice_date = jmodels.jDateField(verbose_name='تاریخ فاکتور', null=True, blank=True)
    qty =models.PositiveIntegerField(null=True, blank=True, verbose_name='تعداد کالای فاکتور')
    net_weight = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='وزن خرید فاکتور')
    accessory_weight = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True,verbose_name='وزن خریدبا متعلقات فاکتور')
    invoice_dailyprice = models.PositiveIntegerField(null=True, blank=True, verbose_name='نرخ روز طلا')
    invoice_price = models.BigIntegerField(null=True, blank=True, verbose_name='مبلغ فاکتور')
    discount = models.IntegerField(null=True, blank=True, verbose_name='تخفیف')
    notes = models.TextField(blank=True, null=True, verbose_name='شرح')
    created_at = models.DateTimeField(default=now, verbose_name='تاریخ ایجاد')
    def __str__(self):
        return f"فاکتور خرید از بنکدار   {self.invoice_date}"

    class Meta:
        verbose_name = 'فاکتور تامین زینتی'
        verbose_name_plural = 'فاکتورهای تامین زینتی'