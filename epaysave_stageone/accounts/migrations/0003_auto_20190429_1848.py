# Generated by Django 2.0 on 2019-04-29 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20190429_1747'),
    ]

    operations = [
        migrations.AddField(
            model_name='merchantticket',
            name='transaction_id',
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AddField(
            model_name='purchasedticket',
            name='transaction_id',
            field=models.CharField(blank=True, max_length=30),
        ),
    ]
