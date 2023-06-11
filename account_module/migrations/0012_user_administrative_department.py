# Generated by Django 4.2 on 2023-06-10 18:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account_module', '0011_administrativedepartment_user_is_head_department'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='administrative_department',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='account_module.administrativedepartment'),
        ),
    ]