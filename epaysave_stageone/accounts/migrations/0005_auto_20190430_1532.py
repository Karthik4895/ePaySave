# Generated by Django 2.0 on 2019-04-30 10:02

from django.db import migrations
import fernet_fields.fields


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20190429_1851'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newsport',
            name='description',
            field=fernet_fields.fields.EncryptedCharField(max_length=10000),
        ),
    ]
