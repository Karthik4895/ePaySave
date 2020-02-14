from django.db import models
from django.contrib.auth.models import User
from fernet_fields import EncryptedCharField,EncryptedEmailField, EncryptedIntegerField
from django.db.models import signals
from datetime import datetime, timedelta
from django.urls import reverse

def get_default_my_date():
    return datetime.today()+timedelta(hours=2,minutes=30)

class Merchant(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    merchant_code=models.CharField(max_length=50,unique=True,primary_key=True)
    merchant_contact_email=EncryptedEmailField()
    merchant_contact_name=EncryptedCharField(max_length=50)
    merchant_contact_no=EncryptedCharField(max_length=20)
    merchant_address=EncryptedCharField(max_length=50)
    merchant_city=EncryptedCharField(max_length=20)
    merchant_country=EncryptedCharField(max_length=20)
    merchant_img=models.ImageField(blank=True,null=True,upload_to='merchantimgs/')
    merchant_wallet=models.DecimalField(decimal_places=2,max_digits=12,default=0.00,blank=True)

    def __str__(self):
        return self.merchant_code


class MerchantItem(models.Model):
    Adult_or_Child = (
        ('A', 'Adult'),
        ('C', 'Child'),
        ('B', 'Both'),
    )
    Gender_Allowed=(
        ('M', 'Male'),
        ('F', 'Female'),
        ('B', 'Both'),
    )
    merchant_code=models.ForeignKey(Merchant,on_delete=models.CASCADE,related_name='merchantcode')
    item_code=models.CharField(primary_key=True,unique=True,max_length=50)
    description=EncryptedCharField(max_length=200)
    adult_child=EncryptedCharField(max_length=2,choices=Adult_or_Child)
    gender_allowed=EncryptedCharField(max_length=1,choices=Gender_Allowed)
    quantity=EncryptedIntegerField(default=0,blank=True)
    price=models.DecimalField(decimal_places=2,default=0.00,max_digits=10,blank=True)
    discount=models.DecimalField(decimal_places=2,default=0.00,max_digits=10,blank=True)

    def __str__(self):
        return self.item_code

