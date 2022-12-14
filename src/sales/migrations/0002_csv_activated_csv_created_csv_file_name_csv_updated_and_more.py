# Generated by Django 4.0.5 on 2022-06-21 16:19

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='csv',
            name='activated',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='csv',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='csv',
            name='file_name',
            field=models.FileField(default=django.utils.timezone.now, upload_to='csvs'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='csv',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='sale',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='sale',
            name='created',
            field=models.DateTimeField(blank=True),
        ),
    ]
