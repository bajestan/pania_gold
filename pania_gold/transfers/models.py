
from django.db import models
from django_jalali.db import models as jmodels
from decimal import Decimal
from django.utils.timezone import now
from django.core.exceptions import ValidationError
import re






# =========================مدل انتقال و محل نگهداری قطعات=====================

class PieceTransfer(models.Model):
    melt_piece = models.ForeignKey('meltvitrin.MeltPiece', on_delete=models.SET_NULL, null=True, blank=True,verbose_name='قطعه آبشده')
    craft_piece = models.ForeignKey('vitrin.CraftPiece', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='قطعه زینتی')
    old_piece = models.ForeignKey('vitrin.OldPiece', on_delete=models.SET_NULL, null=True, blank=True,verbose_name='قطعه مستعمل')

    sender = models.ForeignKey('accounts.CompanySeller', on_delete=models.SET_NULL, null=True, blank=True, related_name='piece_transfers_sent', verbose_name='انتقال‌دهنده')
    receiver = models.ForeignKey('accounts.CompanySeller', on_delete=models.SET_NULL, null=True, blank=True, related_name='piece_transfers_received', verbose_name='دریافت‌کننده')

    transfer_date = jmodels.jDateField( null=True, blank=True, verbose_name='تاریخ انتقال')
    description = models.TextField(blank=True, null=True, verbose_name='توضیحات')

    # فیلدهای جدید برای مدیریت وضعیت ارسال و تأیید
    is_sent = models.BooleanField(default=False, verbose_name='ارسال شده توسط فرستنده؟')
    sent_at = jmodels.jDateTimeField(null=True, blank=True, verbose_name='زمان ارسال')

    is_received = models.BooleanField(default=False, verbose_name='تأیید شده توسط گیرنده؟')
    received_at = jmodels.jDateTimeField(null=True, blank=True, verbose_name='زمان دریافت')

    def __str__(self):
        piece = self.get_piece()
        return f"انتقال {piece} به {self.receiver} در {self.transfer_date}"

    def get_piece(self):
        if self.melt_piece:
            return self.melt_piece
        elif self.craft_piece:
            return self.craft_piece
        elif self.old_piece:
            return self.old_piece
        return None


    class Meta:
        verbose_name = 'انتقال قطعه'
        verbose_name_plural = 'انتقال قطعات'

# -------------------------------------------------