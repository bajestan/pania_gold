# Generated by Django 5.1.3 on 2025-04-14 03:02

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("vitrin", "0026_saleinvoice_net_sale_price"),
    ]

    operations = [
        migrations.AddField(
            model_name="oldpiece",
            name="sale_price_ojrat",
            field=models.IntegerField(default=0, verbose_name="اجرت ریالی فروش"),
        ),
    ]
