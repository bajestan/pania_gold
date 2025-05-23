# Generated by Django 5.1.3 on 2025-01-17 04:44

import django.db.models.deletion
import vitrin.models
from django.db import migrations, models
from meltvitrin.models import upload_to_melt



class Migration(migrations.Migration):
    dependencies = [
        ("vitrin", "0013_meltpiece_image"),
    ]

    operations = [
        migrations.RenameField(
            model_name="saleinvoice",
            old_name="total_amount",
            new_name="sale_price",
        ),
        migrations.AddField(
            model_name="saleinvoice",
            name="sale_tax",
            field=models.BigIntegerField(
                blank=True, null=True, verbose_name="جمع مالیات"
            ),
        ),
        migrations.AlterField(
            model_name="craftpiece",
            name="image",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to=vitrin.models.upload_to_craft,
                verbose_name="تصویر بند انگشتی",
            ),
        ),
        migrations.AlterField(
            model_name="craftpiece",
            name="sale_invoice",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="crafted_golds",
                to="vitrin.saleinvoice",
                verbose_name="فاکتور فروش زینتی",
            ),
        ),
        migrations.AlterField(
            model_name="meltpiece",
            name="image",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to=upload_to_melt,

                verbose_name="تصویر بند انگشتی",
            ),
        ),
        migrations.AlterField(
            model_name="oldpiece",
            name="image",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to=vitrin.models.upload_to_old,
                verbose_name="تصویر بند انگشتی",
            ),
        ),
        migrations.AlterField(
            model_name="oldpiece",
            name="sale_invoice",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="old_piece",
                to="vitrin.saleinvoice",
                verbose_name="فاکتور فروش مستعمل",
            ),
        ),
    ]
