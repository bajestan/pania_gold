# Generated by Django 5.1.3 on 2025-05-15 11:05

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("vitrin", "0035_alter_companyvitrin_vitrin_type"),
    ]

    operations = [
        migrations.AlterField(
            model_name="companyvitrin",
            name="vitrin_type",
            field=models.CharField(
                blank=True,
                choices=[
                    ("tehran", "tehran"),
                    ("bajestan", "bajestan"),
                    ("abhar", "abhar"),
                ],
                max_length=20,
                null=True,
                verbose_name="نوع ویترین",
            ),
        ),
    ]
