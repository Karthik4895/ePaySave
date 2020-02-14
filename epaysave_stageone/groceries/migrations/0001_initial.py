# Generated by Django 2.0 on 2019-04-04 20:14

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
            name='Commodity',
            fields=[
                ('commodity_code', models.CharField(max_length=50, primary_key=True, serialize=False, unique=True)),
                ('commodity_desc', fernet_fields.fields.EncryptedCharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='CommodityItem',
            fields=[
                ('commodity_item_code', models.CharField(max_length=50, primary_key=True, serialize=False, unique=True)),
                ('item_desc', fernet_fields.fields.EncryptedCharField(max_length=100)),
                ('brand', fernet_fields.fields.EncryptedCharField(max_length=1)),
                ('hundred_price', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10)),
                ('twohundred_price', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10)),
                ('fivehundred_price', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10)),
                ('onekg_price', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10)),
                ('fivekg_price', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10)),
                ('twentyfiveekg_price', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10)),
                ('fiftykg_price', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10)),
                ('commodity_code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='commodity_item', to='groceries.Commodity')),
            ],
        ),
        migrations.CreateModel(
            name='Grocery',
            fields=[
                ('grocery_code', models.CharField(max_length=50, primary_key=True, serialize=False, unique=True)),
                ('grocery_contact_email', fernet_fields.fields.EncryptedEmailField(max_length=254)),
                ('grocery_contact_name', fernet_fields.fields.EncryptedCharField(max_length=50)),
                ('grocery_contact_no', fernet_fields.fields.EncryptedCharField(max_length=20)),
                ('grocery_address', fernet_fields.fields.EncryptedCharField(max_length=50)),
                ('grocery_city', fernet_fields.fields.EncryptedCharField(max_length=20)),
                ('grocery_country', fernet_fields.fields.EncryptedCharField(max_length=20)),
                ('grocery_img', models.ImageField(blank=True, null=True, upload_to='merchantimgs/')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='commodity',
            name='grocery_code',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='grocery_commodity', to='groceries.Grocery'),
        ),
    ]