# Generated by Django 5.1.3 on 2025-01-10 10:50

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("vitrin", "0004_companyvitrin_rename_oldgold_oldpiece_craftpiece_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="craftpiece",
            name="gold_type",
            field=models.CharField(
                blank=True,
                choices=[
                    ("ring", "انگشتر"),
                    ("set", "ست و نیم ست"),
                    ("minimal", "مینیمال"),
                    ("earring", "گوشواره"),
                    ("bracelet", "دستبند"),
                    ("child", "کودک"),
                ],
                max_length=50,
                null=True,
                verbose_name="دسته بندی",
            ),
        ),
    ]
