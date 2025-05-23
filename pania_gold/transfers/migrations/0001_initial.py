# Generated by Django 5.1.3 on 2025-05-14 18:03

import django.db.models.deletion
import django_jalali.db.models
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("accounts", "0003_alter_companyseller_options_and_more"),
        ("meltvitrin", "0004_meltpiece_piece_type"),
        ("vitrin", "0034_alter_craftpiece_buy_ojrat_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="PieceTransfer",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "transfer_date",
                    django_jalali.db.models.jDateField(
                        blank=True, null=True, verbose_name="تاریخ انتقال"
                    ),
                ),
                (
                    "description",
                    models.TextField(blank=True, null=True, verbose_name="توضیحات"),
                ),
                (
                    "is_sent",
                    models.BooleanField(
                        default=False, verbose_name="ارسال شده توسط فرستنده؟"
                    ),
                ),
                (
                    "sent_at",
                    django_jalali.db.models.jDateTimeField(
                        blank=True, null=True, verbose_name="زمان ارسال"
                    ),
                ),
                (
                    "is_received",
                    models.BooleanField(
                        default=False, verbose_name="تأیید شده توسط گیرنده؟"
                    ),
                ),
                (
                    "received_at",
                    django_jalali.db.models.jDateTimeField(
                        blank=True, null=True, verbose_name="زمان دریافت"
                    ),
                ),
                (
                    "craft_piece",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="vitrin.craftpiece",
                        verbose_name="قطعه زینتی",
                    ),
                ),
                (
                    "melt_piece",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="meltvitrin.meltpiece",
                        verbose_name="قطعه آبشده",
                    ),
                ),
                (
                    "old_piece",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="vitrin.oldpiece",
                        verbose_name="قطعه مستعمل",
                    ),
                ),
                (
                    "receiver",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="piece_transfers_received",
                        to="accounts.companyseller",
                        verbose_name="دریافت\u200cکننده",
                    ),
                ),
                (
                    "sender",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="piece_transfers_sent",
                        to="accounts.companyseller",
                        verbose_name="انتقال\u200cدهنده",
                    ),
                ),
            ],
            options={
                "verbose_name": "انتقال قطعه",
                "verbose_name_plural": "انتقال قطعات",
            },
        ),
    ]
