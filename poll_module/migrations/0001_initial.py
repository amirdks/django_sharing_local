# Generated by Django 4.2 on 2023-05-03 06:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Poll',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=30, verbose_name='عنوان سوال')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='زمان ساخت')),
                ('is_active', models.BooleanField(default=True, verbose_name='فعال / غیرفعال')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'نظرسنجی',
                'verbose_name_plural': 'نظرسنجی ها',
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='PollOptions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('option', models.CharField(max_length=30, verbose_name='گزینه')),
                ('option_count', models.IntegerField(default=0, verbose_name='شمارش گزینه')),
                ('poll', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='poll_option', to='poll_module.poll', verbose_name='برای نظرسنجی')),
            ],
            options={
                'verbose_name': 'گزینه',
                'verbose_name_plural': 'گزینه ها',
            },
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='زمان ساخت')),
                ('poll', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='poll_module.poll')),
                ('poll_option', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='poll_module.polloptions')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'رای',
                'verbose_name_plural': 'رای ها',
            },
        ),
    ]
