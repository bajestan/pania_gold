
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.contrib.auth.models import Permission



# =================================کاربران نرم افزار====================
class UserManager(BaseUserManager):
    def create_user(self, mellicod, f_name, l_name, phone, password=None):
        if not mellicod:
            raise ValueError('کاربر باید کد ملی داشته باشد')
        user = self.model(mellicod=mellicod, f_name=f_name, l_name=l_name, phone=phone)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, mellicod, f_name, l_name, phone, password=None):
        user = self.create_user(mellicod, f_name, l_name, phone, password)
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    f_name = models.CharField(max_length=50, verbose_name='نام', blank=True, null=True)
    l_name = models.CharField(max_length=50, verbose_name='فامیلی', blank=True, null=True)
    mellicod = models.CharField(max_length=10, verbose_name='کدملی', unique=True)
    phone = models.BigIntegerField(verbose_name='موبایل', blank=True, null=True)
    create = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    permission = models.ManyToManyField(Permission, related_name='users')

    USERNAME_FIELD = 'mellicod'
    REQUIRED_FIELDS = ['phone', 'f_name', 'l_name']

    objects = UserManager()

    class Meta:
        verbose_name = "کاربر"
        verbose_name_plural = "کاربران"

    def __str__(self):
        return f"{self.f_name} {self.l_name}"

    @property
    def is_staff(self):
        return self.is_admin
# ----------------------------------------
class HomeImage(models.Model):
    image = models.ImageField(upload_to='home_images/')
    description = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.description or "Image"

# -------------------------------------------------
# فرروشنده شرکت
class CompanySeller(models.Model):
    name = models.CharField(max_length=50, verbose_name='نام', null=True, blank=True)
    mellicode = models.CharField(max_length=10, verbose_name='کد ملی', unique=True)
    phone_number = models.CharField(max_length=15, verbose_name='تلفن', null=True, blank=True)
    city = models.CharField(max_length=50, verbose_name='شهر', null=True, blank=True)

    def __str__(self):
        return f'{self.name} '
# --------------------------------------------



