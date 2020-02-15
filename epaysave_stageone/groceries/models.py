from django.db import models
from django.contrib.auth.models import User
from fernet_fields import EncryptedCharField,EncryptedEmailField, EncryptedIntegerField
from django.db.models import signals
from datetime import datetime, timedelta
from django.urls import reverse

def get_default_my_date():
    return datetime.today()+timedelta(hours=2,minutes=30)

class Grocery(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    grocery_code=models.CharField(max_length=50,unique=True,primary_key=True)
    grocery_contact_email=EncryptedEmailField()
    grocery_contact_name=EncryptedCharField(max_length=50)
    grocery_contact_no=EncryptedCharField(max_length=20)
    grocery_address=EncryptedCharField(max_length=50)
    grocery_city=EncryptedCharField(max_length=20)
    grocery_country=EncryptedCharField(max_length=20)
    grocery_img=models.ImageField(blank=True,null=True,upload_to='merchantimgs/')
    grocery_wallet=models.DecimalField(decimal_places=2,max_digits=12,default=0.00,blank=True)


    def __str__(self):
        return self.grocery_code
    class Meta:
        verbose_name_plural = "groceries"



class Commodity(models.Model):
    grocery_code=models.ForeignKey(Grocery,on_delete=models.CASCADE,related_name='grocery_commodity')
    commodity_code=models.CharField(primary_key=True,unique=True,max_length=50)
    commodity_desc=EncryptedCharField(max_length=200)
    def __str__(self):
        return self.commodity_code
    class Meta:
        verbose_name_plural = "commodities"


class CommodityItem(models.Model):
    commodity_code=models.ForeignKey(Commodity,on_delete=models.CASCADE,related_name='commodity_item')
    commodity_item_code=models.CharField(primary_key=True,unique=True,max_length=50)
    item_desc=EncryptedCharField(max_length=100)
    brand=EncryptedCharField(max_length=50)
    hundred_price=models.DecimalField(decimal_places=2,null=True,max_digits=10,blank=True)
    twohundred_price=models.DecimalField(decimal_places=2,null=True,max_digits=10,blank=True)
    fivehundred_price=models.DecimalField(decimal_places=2,null=True,max_digits=10,blank=True)
    onekg_price=models.DecimalField(decimal_places=2,null=True,max_digits=10,blank=True)
    fivekg_price=models.DecimalField(decimal_places=2,null=True,max_digits=10,blank=True)
    twentyfivekg_price=models.DecimalField(decimal_places=2,null=True,max_digits=10,blank=True)
    fiftykg_price=models.DecimalField(decimal_places=2,null=True,max_digits=10,blank=True)
    def __str__(self):
        return self.item_desc


