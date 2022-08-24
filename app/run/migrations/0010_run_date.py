# Generated by Django 3.2.9 on 2021-11-24 17:24

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('run', '0009_alter_run_start_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='run',
            name='date',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='day run'),
            preserve_default=False,
        ),
    ]
