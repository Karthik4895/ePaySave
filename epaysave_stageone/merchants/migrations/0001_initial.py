# Generated by Django 2.0 on 2019-03-30 10:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import fernet_fields.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Merchant',
            fields=[
                ('merchant_code', models.CharField(max_length=50, primary_key=True, serialize=False, unique=True)),
                ('merchant_contact_email', fernet_fields.fields.EncryptedEmailField(max_length=254)),
                ('merchant_contact_name', fernet_fields.fields.EncryptedCharField(max_length=50)),
                ('merchant_contact_no', fernet_fields.fields.EncryptedCharField(max_length=20)),
                ('merchant_address', fernet_fields.fields.EncryptedCharField(max_length=50)),
                ('merchant_city', fernet_fields.fields.EncryptedCharField(max_length=20)),
                ('merchant_country', fernet_fields.fields.EncryptedCharField(max_length=20)),
                ('merchant_img', models.ImageField(blank=True, null=True, upload_to='merchantimgs/')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='MerchantItem',
            fields=[
                ('item_code', models.CharField(max_length=50, primary_key=True, serialize=False, unique=True)),
                ('description', fernet_fields.fields.EncryptedCharField(max_length=200)),
                ('adult_child', fernet_fields.fields.EncryptedCharField(choices=[('A', 'Adult'), ('C', 'Child'), ('B', 'Both')], max_length=2)),
                ('gender_allowed', fernet_fields.fields.EncryptedCharField(choices=[('M', 'Male'), ('F', 'Female'), ('B', 'Both')], max_length=1)),
                ('quantity', fernet_fields.fields.EncryptedIntegerField(blank=True, default=0)),
                ('price', models.FloatField(blank=True, default=0.0)),
                ('discount', models.FloatField(blank=True, default=0.0)),
                ('merchant_code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='merchantcode', to='merchants.Merchant')),
            ],
        ),
    ]
