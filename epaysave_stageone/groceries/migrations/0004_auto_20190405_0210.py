# Generated by Django 2.0 on 2019-04-04 20:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groceries', '0003_auto_20190405_0153'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='commodity',
            options={'verbose_name_plural': 'commodities'},
        ),
        migrations.AlterModelOptions(
            name='grocery',
            options={'verbose_name_plural': 'groceries'},
        ),
        migrations.AlterField(
            model_name='commodityitem',
            name='fiftykg_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='commodityitem',
            name='fivehundred_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='commodityitem',
            name='fivekg_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='commodityitem',
            name='hundred_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='commodityitem',
            name='onekg_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='commodityitem',
            name='twentyfivekg_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='commodityitem',
            name='twohundred_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
