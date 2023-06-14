# Generated by Django 4.2 on 2023-06-14 11:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('account_module', '0014_alter_administrativedepartment_options_and_more'),
        ('contact_module', '0007_contact_head_administrative_department'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contact',
            options={'verbose_name': 'ارتباط کاربران', 'verbose_name_plural': 'ارتباطات کاربران'},
        ),
        migrations.AlterModelOptions(
            name='contactreport',
            options={'verbose_name': 'گزارش ارتباط', 'verbose_name_plural': 'گزارشات ارتباط'},
        ),
        migrations.AlterModelOptions(
            name='unusualcontactreason',
            options={'verbose_name': 'دلیل ارتباط', 'verbose_name_plural': 'دلایل ارتباط'},
        ),
        migrations.AlterField(
            model_name='contact',
            name='head_administrative_department',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='account_module.administrativedepartmenthead'),
        ),
        migrations.CreateModel(
            name='ContactFormModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('unusual_contact_reason', models.ManyToManyField(to='contact_module.unusualcontactreason')),
                ('users', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'فرم',
                'verbose_name_plural': 'لیست فرم ها',
            },
        ),
    ]
