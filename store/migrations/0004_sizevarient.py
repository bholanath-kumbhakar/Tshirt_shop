# Generated by Django 4.1.3 on 2022-11-10 06:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_alter_brand_slug_alter_color_slug_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='SizeVarient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.IntegerField()),
                ('size', models.CharField(choices=[('S', 'small'), ('M', 'medium'), ('L', 'large'), ('XL', 'extra large'), ('XXL', 'extra extra large')], max_length=5)),
                ('tshirt', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.tshirt')),
            ],
        ),
    ]
