# Generated by Django 4.2 on 2023-06-01 10:19

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_module', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='HyperLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('image', models.ImageField(upload_to='images/hyper_link')),
                ('link', models.TextField(validators=[django.core.validators.URLValidator()])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'لینک خارجی',
                'verbose_name_plural': 'لینک های خارجی',
            },
        ),
    ]