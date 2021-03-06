# Generated by Django 2.0 on 2019-04-29 12:04

import accounts.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import fernet_fields.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('groceries', '0005_grocery_grocery_wallet'),
        ('merchants', '0003_merchant_merchant_wallet'),
    ]

    operations = [
        migrations.CreateModel(
            name='MerchantTicket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ticket_amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('adult_qty', models.IntegerField()),
                ('child_qty', models.IntegerField()),
                ('date_of_purchase', models.DateTimeField(default=accounts.models.get_default_my_date)),
                ('message', fernet_fields.fields.EncryptedCharField(blank=True, max_length=50, null=True)),
                ('ticket_id', models.CharField(blank=True, max_length=30)),
                ('merchant_purchased', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='merchants.Merchant')),
            ],
        ),
        migrations.CreateModel(
            name='NewsPort',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('news_title_slug', models.SlugField()),
                ('news_editor', fernet_fields.fields.EncryptedCharField(max_length=50)),
                ('news_title', fernet_fields.fields.EncryptedCharField(max_length=60)),
                ('description', fernet_fields.fields.EncryptedCharField(max_length=300)),
                ('newspic', models.ImageField(blank=True, null=True, upload_to='newsimgs/')),
                ('news_source', fernet_fields.fields.EncryptedCharField(max_length=50)),
                ('news_date', models.DateTimeField(default=accounts.models.get_default_my_date)),
                ('news_video_file', models.FileField(null=True, upload_to='videos/')),
            ],
        ),
        migrations.CreateModel(
            name='Positions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lattitude', models.CharField(default='1', max_length=20)),
                ('longitude', models.CharField(default='1', max_length=20)),
                ('latt_two', models.CharField(default='1', max_length=20)),
                ('long_two', models.CharField(default='1', max_length=20)),
                ('latt_three', models.CharField(default='1', max_length=20)),
                ('long_three', models.CharField(default='1', max_length=20)),
                ('latt_four', models.CharField(default='1', max_length=20)),
                ('long_four', models.CharField(default='1', max_length=20)),
                ('latt_five', models.CharField(default='1', max_length=20)),
                ('long_five', models.CharField(default='1', max_length=20)),
            ],
            options={
                'verbose_name_plural': 'Positions',
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', fernet_fields.fields.EncryptedCharField(max_length=50)),
                ('last_name', fernet_fields.fields.EncryptedCharField(max_length=50)),
                ('email', fernet_fields.fields.EncryptedEmailField(max_length=254)),
                ('password', fernet_fields.fields.EncryptedCharField(max_length=50)),
                ('mobile_no', models.CharField(max_length=20, unique=True)),
                ('address_line_1', fernet_fields.fields.EncryptedCharField(max_length=50)),
                ('address_line_2', fernet_fields.fields.EncryptedCharField(blank=True, max_length=50)),
                ('postal_code', fernet_fields.fields.EncryptedCharField(max_length=7)),
                ('city', fernet_fields.fields.EncryptedCharField(max_length=20)),
                ('country', fernet_fields.fields.EncryptedCharField(max_length=20)),
                ('image', models.ImageField(blank=True, upload_to='images/')),
                ('referral_contact', models.CharField(blank=True, max_length=15)),
                ('promo_coupon', models.CharField(blank=True, max_length=100)),
                ('ic', fernet_fields.fields.EncryptedCharField(blank=True, max_length=50, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PurchasedCommodity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('commodityitemcode', models.CharField(max_length=50)),
                ('commodityitemname', fernet_fields.fields.EncryptedCharField(max_length=100)),
            ],
            options={
                'verbose_name_plural': 'Purchased Commodities',
            },
        ),
        migrations.CreateModel(
            name='PurchasedContent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hundredgramqty', fernet_fields.fields.EncryptedIntegerField(default=0)),
                ('hundredgramtotprice', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('twohundredgramqty', fernet_fields.fields.EncryptedIntegerField(default=0)),
                ('twohundredgramtotprice', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('fivehundredgramqty', fernet_fields.fields.EncryptedIntegerField(default=0)),
                ('fivehundredgramtotprice', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('onekgqty', fernet_fields.fields.EncryptedIntegerField(default=0)),
                ('onekgtotprice', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('fivekgqty', fernet_fields.fields.EncryptedIntegerField(default=0)),
                ('fivekgtotprice', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('twentyfivekgqty', fernet_fields.fields.EncryptedIntegerField(default=0)),
                ('twentyfivekgtotprice', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('fiftykgqty', fernet_fields.fields.EncryptedIntegerField(default=0)),
                ('fiftykgtotprice', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('totalcommamt', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('total_packets', fernet_fields.fields.EncryptedIntegerField(default=0)),
                ('purchased_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='purch_content', to='accounts.PurchasedCommodity')),
            ],
            options={
                'verbose_name_plural': 'Purchased Contents',
            },
        ),
        migrations.CreateModel(
            name='PurchasedGrocery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ticket_id', models.CharField(blank=True, max_length=30)),
                ('transaction_id', models.CharField(blank=True, max_length=30)),
                ('date_of_purchase', models.DateTimeField(default=accounts.models.get_default_my_date)),
                ('grocery', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='purchased_groc', to='groceries.Grocery')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='purchased_prof', to='accounts.Profile')),
            ],
            options={
                'verbose_name_plural': 'Purchased Groceries',
            },
        ),
        migrations.CreateModel(
            name='PurchasedTicket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ticket_amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('adult_qty', models.IntegerField()),
                ('child_qty', models.IntegerField()),
                ('date_of_purchase', models.DateTimeField(default=accounts.models.get_default_my_date)),
                ('message', fernet_fields.fields.EncryptedCharField(blank=True, max_length=50, null=True)),
                ('ticket_id', models.CharField(blank=True, max_length=30)),
                ('merchant_purchased', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='merchants.Merchant')),
                ('user_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='userprofile', to='accounts.Profile')),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_amount', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10)),
                ('wallet_balance_sent', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('wallet_balance_rec', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('date_of_transaction', models.DateTimeField(default=accounts.models.get_default_my_date)),
                ('message', fernet_fields.fields.EncryptedCharField(blank=True, max_length=50, null=True)),
                ('transaction_id', models.CharField(blank=True, max_length=30)),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='receiver', to='accounts.Profile')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sender', to='accounts.Profile')),
            ],
        ),
        migrations.CreateModel(
            name='Wallet',
            fields=[
                ('wallet_id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('wallet_bal', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10)),
                ('total_trans_sent', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10)),
                ('total_trans_rec', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10)),
                ('cash_balance', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10)),
                ('savings', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10)),
                ('loan_amt', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10)),
                ('recycle_wallet', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10)),
                ('incentive_wallet', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10)),
                ('crowd_wallet', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10)),
                ('wallet_cash_req', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10)),
                ('wallet_cash_desc', fernet_fields.fields.EncryptedCharField(blank=True, max_length=100)),
                ('wallet_img', models.ImageField(blank=True, null=True, upload_to='receiptcashimgs/')),
                ('wallet_loan_req', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10)),
                ('wallet_loan_desc', fernet_fields.fields.EncryptedCharField(blank=True, max_length=100)),
                ('loan_img', models.ImageField(blank=True, null=True, upload_to='receiptloanimgs/')),
                ('wallet_savings_req', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10)),
                ('wallet_savings_desc', fernet_fields.fields.EncryptedCharField(blank=True, max_length=100)),
                ('savings_img', models.ImageField(blank=True, null=True, upload_to='receiptsavingsimgs/')),
                ('wallet_crowd_req', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10)),
                ('wallet_crowd_desc', fernet_fields.fields.EncryptedCharField(blank=True, max_length=100)),
                ('crowd_img', models.ImageField(blank=True, null=True, upload_to='receiptsavingsimgs/')),
                ('profile', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='accounts.Profile')),
            ],
            options={
                'ordering': ('wallet_cash_req', 'wallet_loan_req', 'wallet_savings_req', 'wallet_crowd_req'),
            },
        ),
        migrations.AddField(
            model_name='purchasedcommodity',
            name='purchased_groc',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='purch_groc_id', to='accounts.PurchasedGrocery'),
        ),
        migrations.AddField(
            model_name='positions',
            name='profile',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='accounts.Profile'),
        ),
        migrations.AddField(
            model_name='merchantticket',
            name='user_profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='merchantuserprofile', to='accounts.Profile'),
        ),
    ]
