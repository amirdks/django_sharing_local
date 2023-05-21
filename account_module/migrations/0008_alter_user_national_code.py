# Generated by Django 4.2 on 2023-05-13 19:18

import account_module.validation
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account_module', '0007_alter_user_national_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='national_code',
            field=models.CharField(max_length=10, null=True, unique=True, validators=[account_module.validation.is_valid_iran_code]),
        ),
    ]