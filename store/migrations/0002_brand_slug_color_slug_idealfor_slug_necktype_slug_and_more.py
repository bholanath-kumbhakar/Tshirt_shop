# Generated by Django 4.1.3 on 2022-11-10 05:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='brand',
            name='slug',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='color',
            name='slug',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='idealfor',
            name='slug',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='necktype',
            name='slug',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='occasion',
            name='slug',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='sleeve',
            name='slug',
            field=models.CharField(max_length=30, null=True),
        ),
    ]
