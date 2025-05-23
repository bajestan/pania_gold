# Generated by Django 5.1.3 on 2025-01-10 10:50

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("paniavault", "0016_alter_reciptcraftinvoice_options_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customer",
            name="customer_type",
            field=models.CharField(
                choices=[("individual", "حقیقی"), ("company", "حقوقی")],
                max_length=20,
                verbose_name="نوع مشتری",
            ),
        ),
        migrations.AlterField(
            model_name="supplier",
            name="phone_number",
            field=models.CharField(default=0, max_length=11, verbose_name="تلفن همراه"),
            preserve_default=False,
        ),
    ]
