
import jdatetime
from django import forms
from django.utils import timezone
from .models import PieceTransfer







class ReceiverForm(forms.ModelForm):
    class Meta:
        model = PieceTransfer
        fields = ['sender', 'sent_at', 'is_sent', 'receiver']
        widgets = {
            'sender': forms.Select(attrs={
                'class': 'form-control select',
                'style': 'font-family: Vazirmatn, sans-serif; font-size: 12px',
                'required': 'required',
            }),
            'sent_at': forms.TextInput(attrs={
                'data-jdp': 'true',
                'class': 'form-control',
                'required': True,
                'placeholder': 'تاریخ ارسال',
                'style': 'font-family: Vazirmatn, sans-serif; font-size: 12px',
                'autocomplete': 'off',
            }),
            'is_sent': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'style': 'margin-top: 8px; transform: scale(1.2);',
            }),
            'receiver': forms.Select(attrs={
                'class': 'form-control select',
                'style': 'font-family: Vazirmatn, sans-serif; font-size: 12px',
                'required': 'required',
            }),
        }
        labels = {
            'sender': '',
            'sent_at': '',
            'is_sent': '',
            'receiver': '',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # فقط ظاهر ورودی فرم شمسی باشد، ولی مقدار واقعی میلادی بماند
        if not self.instance.pk:
            shamsi_today = jdatetime.date.today().strftime('%Y/%m/%d')
            self.fields['sent_at'].widget.attrs['value'] = shamsi_today


