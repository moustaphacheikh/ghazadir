# Generated by Django 2.0.8 on 2018-09-06 05:57

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20180809_0305'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=models.CharField(max_length=8, validators=[django.core.validators.RegexValidator(message='يجب أن تحتوي أرقام الهاتف على 8 أرقام.', regex='^\\d{8}$')], verbose_name='الهاتف'),
        ),
    ]