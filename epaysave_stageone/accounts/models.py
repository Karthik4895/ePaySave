from django.db import models
from django.contrib.auth.models import User
from fernet_fields import EncryptedCharField,EncryptedEmailField, EncryptedIntegerField
from django.db.models import signals
from datetime import datetime, timedelta
from django.urls import reverse
from merchants.models import Merchant
from groceries.models import Grocery
from django.template.defaultfilters import slugify
from django.http import JsonResponse


def get_default_my_date():
    return datetime.today()+timedelta(hours=2,minutes=30)

class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    first_name=EncryptedCharField(max_length=50)
    last_name=EncryptedCharField(max_length=50)
    email=EncryptedEmailField()
    password=EncryptedCharField(max_length=50)
    mobile_no= models.CharField(max_length=20,unique=True)
    address_line_1=EncryptedCharField(max_length=50)
    address_line_2=EncryptedCharField(max_length=50,blank=True)
    postal_code=EncryptedCharField(max_length=7)
    city=EncryptedCharField(max_length=20)
    country=EncryptedCharField(max_length=20)
    image=models.ImageField(upload_to='images/',blank=True)
    referral_contact=models.CharField(max_length=15,blank=True)
    promo_coupon=models.CharField(max_length=100,blank=True)
    ic=EncryptedCharField(max_length=50,blank=True,null=True)
    barcode_val=models.CharField(max_length=15,blank=True,null=True)

    def get_absolute_url(self):
        return reverse('accounts:profile_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.mobile_no



class Wallet(models.Model):
    profile=models.OneToOneField(Profile,on_delete=models.CASCADE)
    wallet_id=models.AutoField(primary_key=True,unique=True)
    wallet_bal=models.DecimalField(decimal_places=2,max_digits=10,default=0.00,blank=True)

    total_trans_sent=models.DecimalField(decimal_places=2,max_digits=10,default=0.00,blank=True)
    total_trans_rec=models.DecimalField(decimal_places=2,max_digits=10,default=0.00,blank=True)

    cash_balance=models.DecimalField(decimal_places=2,max_digits=10,default=0.00,blank=True)
    savings=models.DecimalField(decimal_places=2,max_digits=10,default=0.00,blank=True)
    loan_amt=models.DecimalField(decimal_places=2,max_digits=10,default=0.00,blank=True)
    recycle_wallet=models.DecimalField(decimal_places=2,max_digits=10,default=0.00,blank=True)
    incentive_wallet=models.DecimalField(decimal_places=2,max_digits=10,default=0.00,blank=True)
    crowd_wallet=models.DecimalField(decimal_places=2,max_digits=10,default=0.00,blank=True)
    wallet_cash_req=models.DecimalField(decimal_places=2,max_digits=10,default=0.00,blank=True)
    wallet_cash_desc=EncryptedCharField(blank=True,max_length=100)
    wallet_img=models.ImageField(blank=True,null=True,upload_to='receiptcashimgs/')

    wallet_loan_req=models.DecimalField(decimal_places=2,max_digits=10,default=0.00,blank=True)
    wallet_loan_desc=EncryptedCharField(blank=True,max_length=100)
    loan_img=models.ImageField(blank=True,upload_to='receiptloanimgs/',null=True)

    wallet_savings_req=models.DecimalField(decimal_places=2,max_digits=10,default=0.00,blank=True)
    wallet_savings_desc=EncryptedCharField(blank=True,max_length=100)
    savings_img=models.ImageField(blank=True,null=True,upload_to='receiptsavingsimgs/')

    wallet_crowd_req=models.DecimalField(decimal_places=2,max_digits=10,default=0.00,blank=True)
    wallet_crowd_desc=EncryptedCharField(blank=True,max_length=100)
    crowd_img=models.ImageField(blank=True,null=True,upload_to='receiptsavingsimgs/')

    def __str__(self):
        return self.profile.first_name

    class Meta:
        ordering = ('wallet_cash_req','wallet_loan_req','wallet_savings_req','wallet_crowd_req')


def create_wallet(sender, instance, created, **kwargs):
    """Create Wallet for every new Profile."""
    if created:
        Wallet.objects.get_or_create(profile=instance)

signals.post_save.connect(create_wallet, sender=Profile, weak=False,
                          dispatch_uid='models.create_wallet')


class BarCodeTransfer(models.Model):
    sender_profile_id=models.IntegerField()
    receiver_barcode=models.CharField(max_length=15,blank=True,null=True)
    transaction_amount=models.DecimalField(decimal_places=2,max_digits=10,default=0.00,blank=True)
    sender_emailid=EncryptedCharField(max_length=35,blank=True,null=True)
    message=EncryptedCharField(max_length=50,blank=True,null=True)
    transaction_id=models.CharField(max_length=30,blank=True)

class AppTransfer(models.Model):
    sender_profile_id=models.IntegerField()
    receiver_profile_id=models.IntegerField()
    transaction_amount=models.DecimalField(decimal_places=2,max_digits=10,default=0.00,blank=True)
    message=EncryptedCharField(max_length=50,blank=True,null=True)
    transaction_id=models.CharField(max_length=30,blank=True)


class Transaction(models.Model):
    sender=models.ForeignKey(Profile,on_delete=models.CASCADE,related_name='sender')
    receiver=models.ForeignKey(Profile,on_delete=models.CASCADE,related_name='receiver')
    transaction_amount=models.DecimalField(decimal_places=2,max_digits=10,default=0.00,blank=True)
    wallet_balance_sent=models.DecimalField(decimal_places=2,max_digits=10,default=0.00)
    wallet_balance_rec=models.DecimalField(decimal_places=2,max_digits=10,default=0.00)
    date_of_transaction=models.DateTimeField(default=get_default_my_date)
    message=EncryptedCharField(max_length=50,null=True,blank=True)
    transaction_id=models.CharField(max_length=30,blank=True)

    def __str__(self):
        return str(self.sender.first_name)+' to '+str(self.receiver.first_name)+': '+str(self.transaction_amount)


class PurchasedTicket(models.Model):
    user_profile=models.ForeignKey(Profile,on_delete=models.CASCADE,related_name='userprofile')
    merchant_purchased=models.ForeignKey(Merchant,on_delete=models.CASCADE,name='merchant_purchased')
    ticket_amount=models.DecimalField(decimal_places=2,max_digits=10,default=0.00)
    adult_qty= models.IntegerField()
    child_qty= models.IntegerField()
    date_of_purchase=models.DateTimeField(default=get_default_my_date)
    message=EncryptedCharField(max_length=50,null=True,blank=True)
    ticket_id=models.CharField(max_length=30,blank=True)
    transaction_id=models.CharField(max_length=30,blank=True)

    def __str__(self):
        return str(self.user_profile.first_name)+' '+str(self.user_profile.last_name)+' purchased '+str(self.merchant_purchased.merchant_contact_name)+' tickets, Adult:'+str(self.adult_qty)+', Children:'+str(self.child_qty)+' Total Amount: SGD.'+str(self.ticket_amount)


class MerchantTicket(models.Model):
    user_profile=models.ForeignKey(Profile,on_delete=models.CASCADE,related_name='merchantuserprofile')
    merchant_purchased=models.ForeignKey(Merchant,on_delete=models.CASCADE,name='merchant_purchased')
    ticket_amount=models.DecimalField(decimal_places=2,max_digits=10,default=0.00)
    adult_qty= models.IntegerField()
    child_qty= models.IntegerField()
    date_of_purchase=models.DateTimeField(default=get_default_my_date)
    message=EncryptedCharField(max_length=50,null=True,blank=True)
    ticket_id=models.CharField(max_length=30,blank=True)
    transaction_id=models.CharField(max_length=30,blank=True)

    def __str__(self):
        return str(self.user_profile.first_name)+' '+str(self.user_profile.last_name)+' purchased '+str(self.merchant_purchased.merchant_contact_name)+' tickets, Adult:'+str(self.adult_qty)+', Children:'+str(self.child_qty)+' Total Amount: SGD.'+str(self.ticket_amount)


class NewsPort(models.Model):
    news_title_slug=models.SlugField()
    news_editor=EncryptedCharField(max_length=50)
    news_title=EncryptedCharField(max_length=60)
    description=EncryptedCharField(max_length=10000)
    newspic=models.ImageField(blank=True,null=True,upload_to='newsimgs/')
    news_source=EncryptedCharField(max_length=50)
    news_date=models.DateTimeField(default=get_default_my_date)
    news_video_file=models.FileField(upload_to='videos/',null=True,blank=True)

    def __str__(self):
        return self.news_title
    #redefining the save method
    def save(self, *args, **kwargs):
        self.news_title_slug = slugify(self.news_title)
        super(NewsPort, self).save(*args, **kwargs)


class Positions(models.Model):

    profile=models.OneToOneField(Profile,on_delete=models.CASCADE)

    lattitude=models.CharField(default="1",max_length=20)
    longitude=models.CharField(default="1",max_length=20)

    latt_two=models.CharField(default="1",max_length=20)
    long_two=models.CharField(default="1",max_length=20)

    latt_three=models.CharField(default="1",max_length=20)
    long_three=models.CharField(default="1",max_length=20)

    latt_four=models.CharField(default="1",max_length=20)
    long_four=models.CharField(default="1",max_length=20)

    latt_five=models.CharField(default="1",max_length=20)
    long_five=models.CharField(default="1",max_length=20)


    def __str__(self):
        return str(self.profile.first_name+"'s last positions")

    class Meta:
        verbose_name_plural="Positions"


def create_positions(sender, instance, created, **kwargs):
    """Create Position for every new Profile."""
    if created:
        Positions.objects.get_or_create(profile=instance)

signals.post_save.connect(create_positions, sender=Profile, weak=False,
                          dispatch_uid='models.create_positions')


class PurchasedGrocery(models.Model):
    profile = models.ForeignKey(Profile,on_delete=models.CASCADE,related_name='purchased_prof')
    grocery = models.ForeignKey(Grocery,on_delete=models.CASCADE,related_name='purchased_groc')
    ticket_id = models.CharField(max_length=30,blank=True)
    transaction_id = models.CharField(max_length=30,blank=True)
    date_of_purchase=models.DateTimeField(default=get_default_my_date)

    def __str__(self):
        return str(str(self.profile.first_name)+' '+str(self.profile.last_name)+' bought from '+str(self.grocery.grocery_contact_name))

    class Meta:
        verbose_name_plural="Purchased Groceries"


class PurchasedCommodity(models.Model):
    purchased_groc = models.ForeignKey(PurchasedGrocery,on_delete=models.CASCADE,related_name='purch_groc_id')
    commodityitemcode = models.CharField(max_length=50)
    commodityitemname = EncryptedCharField(max_length=100)


    def __str__(self):
        return str(self.commodityitemname)

    class Meta:
        verbose_name_plural="Purchased Commodities"


class PurchasedContent(models.Model):
    purchased_item = models.ForeignKey(PurchasedCommodity,on_delete=models.CASCADE,related_name='purch_content')
    hundredgramqty = EncryptedIntegerField(default=0)
    hundredgramtotprice = models.DecimalField(decimal_places=2,max_digits=10,default=0.0)
    twohundredgramqty = EncryptedIntegerField(default=0)
    twohundredgramtotprice = models.DecimalField(decimal_places=2,max_digits=10,default=0.0)
    fivehundredgramqty = EncryptedIntegerField(default=0)
    fivehundredgramtotprice = models.DecimalField(decimal_places=2,max_digits=10,default=0.0)
    onekgqty = EncryptedIntegerField(default=0)
    onekgtotprice = models.DecimalField(decimal_places=2,max_digits=10,default=0.0)
    fivekgqty = EncryptedIntegerField(default=0)
    fivekgtotprice = models.DecimalField(decimal_places=2,max_digits=10,default=0.0)
    twentyfivekgqty = EncryptedIntegerField(default=0)
    twentyfivekgtotprice = models.DecimalField(decimal_places=2,max_digits=10,default=0.0)
    fiftykgqty = EncryptedIntegerField(default=0)
    fiftykgtotprice = models.DecimalField(decimal_places=2,max_digits=10,default=0.0)
    totalcommamt = models.DecimalField(decimal_places=2,max_digits=10,default=0.0)
    total_packets = EncryptedIntegerField(default=0)
    def __str__(self):
        return str(self.purchased_item.purchased_groc.profile.first_name)+' bought '+str(self.total_packets)+' '+str(self.purchased_item)+' packets'

    class Meta:
        verbose_name_plural="Purchased Contents"

