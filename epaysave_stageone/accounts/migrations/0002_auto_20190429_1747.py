# Generated by Django 2.0 on 2019-04-29 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wallet',
            name='wallet_id',
            field=models.AutoField(default=5001, primary_key=True, serialize=False, unique=True),
        ),
    ]