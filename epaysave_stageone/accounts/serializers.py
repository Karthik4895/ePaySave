from rest_framework import serializers
from .models import AppTransfer,Profile,Wallet,Transaction,PurchasedTicket,PurchasedGrocery, PurchasedContent, PurchasedCommodity ,BarCodeTransfer
from django.contrib.auth.models import User
from drf_writable_nested import WritableNestedModelSerializer
from rest_framework.authtoken.models import Token
# from django.contrib.auth.hashers import make_password
from merchants.models import Merchant,MerchantItem
from drf_braces.forms.serializer_form import SerializerForm
from groceries.models import Grocery,CommodityItem,Commodity
import random

class Base64ImageField(serializers.ImageField):
    """
    A Django REST framework field for handling image-uploads through raw post data.
    It uses base64 for encoding and decoding the contents of the file.

    Heavily based on
    https://github.com/tomchristie/django-rest-framework/pull/1268

    Updated for Django REST framework 3.
    """

    def to_internal_value(self, data):
        from django.core.files.base import ContentFile
        import base64
        import six
        import uuid

        # Check if this is a base64 string
        if isinstance(data, six.string_types):
            # Check if the base64 string is in the "data:" format
            if 'data:' in data and ';base64,' in data:
                # Break out the header from the base64 content
                header, data = data.split(';base64,')
            else:
                return data

            # Try to decode the file. Return validation error if it fails.
            try:
                code = base64.b64encode(data)
                decoded_file = base64.b64decode(code)
                print(decoded_file)
                print(code)
            except TypeError:
                self.fail('invalid_image')

            # Generate file name:
            file_name = str(uuid.uuid4())[:12]   # 12 characters are more than enough.
            # Get the file name extension:
            file_extension = self.get_file_extension(file_name, decoded_file)

            complete_file_name = "%s.%s" % (file_name, file_extension, )

            data = ContentFile(decoded_file, name=complete_file_name)

        return super(Base64ImageField, self).to_internal_value(data)

    def get_file_extension(self, file_name, decoded_file):
        import imghdr

        extension = imghdr.what(file_name, decoded_file)
        extension = "jpg" if extension == "jpeg" else extension

        return extension

class UserSerializer(WritableNestedModelSerializer):
    class Meta:
        model = User
        write_only_fields=('email','password','first_name','last_name',)
        fields = ('email','first_name', 'last_name','username', 'password', 'is_superuser','is_staff')
        extra_kwargs = {'password': {'write_only': True}}

        # def create(self,validated_data):
        #     user = User.objects.create(
        #         email=validated_data['email'],
        #         username=validated_data['username']
        #         # password=make_password(validated_data['password'])
        #     )
        #     user.set_password(validated_data['password'])
        #     user.save()
        #     return user

import itertools

class ProfileSerializer(serializers.HyperlinkedModelSerializer,WritableNestedModelSerializer):
    user = UserSerializer()

    def get_serializer(self, *args, **kwargs):
        kwargs['partial'] = True
        return super(ProfileSerializer, self).get_serializer(*args, **kwargs)

    def create(self,validated_data):
        user_data = validated_data.pop('user',None)
        print(user_data)
        if user_data:
            user=User.objects.get_or_create(**user_data)[0]
            user.set_password(user_data['password'])
            print("HI ",user)
            validated_data['user']=user
            print(validated_data)
        i = 1
        barcode=''
        while (i == 1):
            barcode = ''
            for j in range(1, 14):
                barcode += str(random.randint(0, 9))
            print(barcode)
            try:
                prof = Profile.objects.get(barcode_val=barcode)
                i = 1
            except Profile.DoesNotExist:
                i = 0
        validated_data['barcode_val'] = barcode

        instance = Profile.objects.create(**validated_data)
        return instance

    # def update(self, request, *args, **kwargs):
    #     serializer = self.serializer_class(request.user, data=request.data, partial=True)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(serializer.data, status=status.HTTP_200_OK)

    # def update(self,instance,validated_data):
    #     instance.user = validated_data.get('user', instance.user)
    #     instance.email = validated_data.get('email', instance.email)
    #     instance.first_name = validated_data.get('first_name', instance.first_name)
    #     instance.last_name = validated_data.get('last_name', instance.last_name)
    #     instance.mobile_no = validated_data.get('mobile_no', instance.mobile_no)
    #     instance.address_line_1 = validated_data.get('address_line_1', instance.address_line_1)
    #     instance.address_line_2 = validated_data.get('address_line_2', instance.address_line_2)
    #     instance.city = validated_data.get('city', instance.city)
    #     instance.country = validated_data.get('country', instance.country)
    #     instance.postal_code = validated_data.get('postal_code', instance.postal_code)
    #     instance.ic = validated_data.get('ic', instance.ic)
    #     instance.image = validated_data.get('image',instance.image)
    #     instance.save()
    #     return instance

    image = Base64ImageField(max_length=None, use_url=True, required=False, allow_null=True, allow_empty_file=True)

    class Meta:
        model=Profile
        write_only_fields=('password',)
        fields=('user','id','url','first_name','last_name','mobile_no','email','address_line_1','address_line_2','postal_code','country','city','ic','image')


class ProfilesSerializer(serializers.HyperlinkedModelSerializer,WritableNestedModelSerializer):
    user = UserSerializer(read_only=True)

    def get_serializer(self, *args, **kwargs):
        kwargs['partial'] = True
        return super(ProfileSerializer, self).get_serializer(*args, **kwargs)

    # def update(self, request, *args, **kwargs):
    #     serializer = self.serializer_class(request.user, data=request.data, partial=True)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self,instance,validated_data):
        # instance.user = validated_data.get('user', instance.user)
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.mobile_no = validated_data.get('mobile_no', instance.mobile_no)
        instance.address_line_1 = validated_data.get('address_line_1', instance.address_line_1)
        instance.address_line_2 = validated_data.get('address_line_2', instance.address_line_2)
        instance.city = validated_data.get('city', instance.city)
        instance.country = validated_data.get('country', instance.country)
        instance.postal_code = validated_data.get('postal_code', instance.postal_code)
        instance.ic = validated_data.get('ic', instance.ic)
        instance.image = validated_data.get('image',instance.image)
        instance.save()
        return instance

    image = Base64ImageField(max_length=None, use_url=True, required=False, allow_null=True, allow_empty_file=True)

    class Meta:
        model=Profile
        write_only_fields=('password',)
        fields=('user','id','url','first_name','last_name','mobile_no','email','address_line_1','address_line_2','postal_code','country','city','ic','image')



class WalletSerializer(serializers.HyperlinkedModelSerializer):
    profile=ProfileSerializer(read_only=True)

    # def create(self,validated_data):
    #     profile_data = validated_data.pop('profile',None)
    #     if profile_data:
    #         profile=Profile.objects.get_or_create(**profile_data)[0]
    #         validated_data['profile']=profile
    #     instance = Wallet.objects.create(**validated_data)
    #     return instance

    def update(self,instance,validated_data):
        # instance.profile = validated_data.get('profile', instance.profile)
        instance.wallet_bal = validated_data.get('wallet_bal', instance.wallet_bal)
        instance.cash_balance = validated_data.get('cash_balance', instance.cash_balance)
        instance.savings = validated_data.get('savings', instance.savings)
        instance.loan_amt = validated_data.get('loan_amt', instance.loan_amt)
        instance.recycle_wallet = validated_data.get('recycle_wallet', instance.recycle_wallet)
        instance.crowd_wallet = validated_data.get('crowd_wallet', instance.crowd_wallet)
        instance.incentive_wallet = validated_data.get('incentive_wallet',instance.incentive_wallet)
        instance.save()
        return instance
    # profile=ProfileSerializer()

    class Meta:
        model=Wallet
        fields=('profile','wallet_id','url','wallet_bal','cash_balance','savings','loan_amt','recycle_wallet','crowd_wallet','incentive_wallet')


# class MerchantSerializer(serializers.HyperlinkedModelSerializer):
#     user_profile=UserSerializer(read_only=True)
#
#     def update(self,instance,validated_data):
#         instance.merchant_code = validated_data.get('merchant_code', instance.merchant_code)
#         instance.cash_balance = validated_data.get('cash_balance', instance.cash_balance)
#         instance.savings = validated_data.get('savings', instance.savings)
#         instance.loan_amt = validated_data.get('loan_amt', instance.loan_amt)
#         instance.recycle_wallet = validated_data.get('recycle_wallet', instance.recycle_wallet)
#         instance.crowd_wallet = validated_data.get('crowd_wallet', instance.crowd_wallet)
#         instance.incentive_wallet = validated_data.get('incentive_wallet',instance.incentive_wallet)
#         instance.save()
#         return instance
#
#     class Meta:
#         model=Wallet
#         fields=('profile','wallet_id','url','wallet_bal','cash_balance','savings','loan_amt','recycle_wallet','crowd_wallet','incentive_wallet')


class TransactionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model=Transaction
        read_only_fields=('date_of_transaction',)
        fields=('url','transaction_id','sender','receiver','transaction_amount','date_of_transaction','wallet_balance_sent','wallet_balance_rec','message')


class TransactionDispSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model=Transaction
        read_only_fields=('date_of_transaction',)
        fields=('url','transaction_id','sender','receiver','transaction_amount','date_of_transaction','wallet_balance_sent','wallet_balance_rec','message')


class MerchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Merchant
        fields = ('__all__')

class MerchItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MerchantItem
        fields = ('__all__')

class MerchantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Merchant
        fields = ('merchant_code',)

class PurchasedTicketSerializer(serializers.HyperlinkedModelSerializer):
    merchant_purchased = MerchantSerializer()
    class Meta:
        model=PurchasedTicket
        read_only_fields=('date_of_purchase',)
        fields=('url','ticket_id','user_profile','merchant_purchased','adult_qty','child_qty','ticket_amount','date_of_purchase','message')

class GrocerySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model=Grocery
        fields=('grocery_code','grocery_contact_name')


class GroceryySerializer(serializers.HyperlinkedModelSerializer):
    user=UserSerializer()
    class Meta:
        model=Grocery
        fields=('__all__')

class CommoditySerializer(serializers.ModelSerializer):
    class Meta:
        model=Commodity
        fields=('commodity_code','commodity_desc')


class CommodityItemSerializer(serializers.HyperlinkedModelSerializer):
    commodity_code=CommoditySerializer()
    class Meta:
        model = CommodityItem
        fields=('__all__')

class PurchasedGrocerySerializer(serializers.HyperlinkedModelSerializer):
    grocery=GrocerySerializer()
    class Meta:
        model=PurchasedGrocery
        fields=('profile','grocery')

class PurchasedCommoditySerializer(serializers.HyperlinkedModelSerializer):
    purchased_groc = PurchasedGrocerySerializer()
    class Meta:
        model=PurchasedCommodity
        fields=('purchased_groc','commodityitemcode')

class PurchasedContentSerializer(serializers.HyperlinkedModelSerializer):
    purchased_item = PurchasedCommoditySerializer()
    class Meta:
        model=PurchasedContent
        fields=('__all__')


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model=Token
        fields=('key','user','created')


class AppTransferSerializer(serializers.ModelSerializer):
    class Meta:
        model=AppTransfer
        fields=('sender_profile_id','receiver_profile_id','transaction_amount','message')




class BarCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model=BarCodeTransfer
        fields=('sender_profile_id','receiver_barcode','transaction_amount','sender_emailid','message')



class RequestsSerializer(serializers.HyperlinkedModelSerializer):

    def get_serializer(self, *args, **kwargs):
        kwargs['partial'] = True
        return super(RequestsSerializer, self).get_serializer(*args, **kwargs)

    def update(self,instance,validated_data):
        instance.wallet_cash_req = validated_data.get('wallet_cash_req', instance.wallet_cash_req)
        instance.wallet_cash_desc = validated_data.get('wallet_cash_desc', instance.wallet_cash_desc)
        print(instance.wallet_cash_desc)
        instance.wallet_img = validated_data.get('wallet_img', instance.wallet_img)

        if instance.wallet_cash_req:
            pk=instance.wallet_id-5000
            profile = Profile.objects.get(pk=pk)
            wall = Wallet.objects.get(profile=profile)
            w = instance.wallet_cash_req
            if w == wall.wallet_cash_req:
                pass
            else:
                t_id = (str('TRAC' + str(wall.wallet_id)[-1] + profile.first_name[2:3] + 'AD' + str(random.randint(1, 10000)))).upper()

                Transaction.objects.create(transaction_amount=w, receiver_id=2, sender_id=profile.pk,message="Requested Cash", transaction_id=t_id)


        instance.wallet_loan_req = validated_data.get('wallet_loan_req', instance.wallet_loan_req)
        instance.wallet_loan_desc = validated_data.get('wallet_loan_desc', instance.wallet_loan_desc)
        instance.loan_img = validated_data.get('loan_img', instance.loan_img)
        if instance.wallet_loan_req:
            pk=instance.wallet_id-5000
            profile = Profile.objects.get(pk=pk)
            wall = Wallet.objects.get(profile=profile)
            w = instance.wallet_loan_req
            if w == wall.wallet_loan_req:
                pass
            else:
                t_id = (str('TRAL' + str(wall.wallet_id)[-1] + profile.first_name[2:3] + 'AD' + str(random.randint(1, 10000)))).upper()

                Transaction.objects.create(transaction_amount=w, receiver_id=2, sender_id=profile.pk,
                                           message="Requested Loan", transaction_id=t_id)


        instance.wallet_savings_req = validated_data.get('wallet_savings_req', instance.wallet_savings_req)
        instance.wallet_savings_desc = validated_data.get('wallet_savings_desc', instance.wallet_savings_desc)
        instance.savings_img = validated_data.get('savings_img', instance.savings_img)
        if instance.wallet_savings_req:
            pk=instance.wallet_id-5000
            profile = Profile.objects.get(pk=pk)
            wall = Wallet.objects.get(profile=profile)
            w = instance.wallet_savings_req
            if w == wall.wallet_savings_req:
                pass
            else:
                t_id = (str('TRAS' + str(wall.wallet_id)[-1] + profile.first_name[2:3] + 'AD' + str(random.randint(1, 10000)))).upper()

                Transaction.objects.create(transaction_amount=w, receiver_id=2, sender_id=profile.pk,
                                           message="Requested Savings", transaction_id=t_id)

        instance.wallet_crowd_req = validated_data.get('wallet_crowd_req', instance.wallet_crowd_req)
        instance.wallet_crowd_desc = validated_data.get('wallet_crowd_desc', instance.wallet_crowd_desc)
        instance.crowd_img = validated_data.get('crowd_img', instance.crowd_img)
        if instance.wallet_crowd_req:
            pk=instance.wallet_id-5000
            profile = Profile.objects.get(pk=pk)
            wall = Wallet.objects.get(profile=profile)
            w = instance.wallet_crowd_req

            if w == wall.wallet_crowd_req:
                pass
            else:
                t_id = (str('TACR' + str(wall.wallet_id)[-1] + profile.first_name[2:3] + 'AD' + str(random.randint(1, 10000)))).upper()

                Transaction.objects.create(transaction_amount=w, receiver_id=2, sender_id=profile.pk,
                                           message="Requested Crowd", transaction_id=t_id)
        instance.save()
        return instance


    def partial_update(self,instance,validated_data):
        instance.wallet_cash_req = validated_data.get('wallet_cash_req', instance.wallet_cash_req)
        instance.wallet_cash_desc = validated_data.get('wallet_cash_desc', instance.wallet_cash_desc)
        print(instance.wallet_cash_desc)
        instance.wallet_img = validated_data.get('wallet_img', instance.wallet_img)

        if instance.wallet_cash_req:
            pk=instance.wallet_id-5000
            profile = Profile.objects.get(pk=pk)
            wall = Wallet.objects.get(profile=profile)
            w = instance.wallet_cash_req
            if w == wall.wallet_cash_req:
                pass
            else:
                t_id = (str('TRAC' + str(wall.wallet_id)[-1] + profile.first_name[2:3] + 'AD' + str(random.randint(1, 10000)))).upper()
                Transaction.objects.create(transaction_amount=w, receiver_id=2, sender_id=profile.pk,message="Requested Cash", transaction_id=t_id)


        instance.wallet_loan_req = validated_data.get('wallet_loan_req', instance.wallet_loan_req)
        instance.wallet_loan_desc = validated_data.get('wallet_loan_desc', instance.wallet_loan_desc)
        instance.loan_img = validated_data.get('loan_img', instance.loan_img)
        if instance.wallet_loan_req:
            pk=instance.wallet_id-5000
            profile = Profile.objects.get(pk=pk)
            wall = Wallet.objects.get(profile=profile)
            w = instance.wallet_loan_req
            if w == wall.wallet_loan_req:
                pass
            else:
                t_id = (str('TRAL' + str(wall.wallet_id)[-1] + profile.first_name[2:3] + 'AD' + str(random.randint(1, 10000)))).upper()

                Transaction.objects.create(transaction_amount=w, receiver_id=2, sender_id=profile.pk,
                                           message="Requested Loan", transaction_id=t_id)


        instance.wallet_savings_req = validated_data.get('wallet_savings_req', instance.wallet_savings_req)
        instance.wallet_savings_desc = validated_data.get('wallet_savings_desc', instance.wallet_savings_desc)
        instance.savings_img = validated_data.get('savings_img', instance.savings_img)
        if instance.wallet_savings_req:
            pk=instance.wallet_id-5000
            profile = Profile.objects.get(pk=pk)
            wall = Wallet.objects.get(profile=profile)
            w = instance.wallet_savings_req
            if w == wall.wallet_savings_req:
                pass
            else:
                t_id = (str('TRAS' + str(wall.wallet_id)[-1] + profile.first_name[2:3] + 'AD' + str(random.randint(1, 10000)))).upper()

                Transaction.objects.create(transaction_amount=w, receiver_id=2, sender_id=profile.pk,
                                           message="Requested Savings", transaction_id=t_id)

        instance.wallet_crowd_req = validated_data.get('wallet_crowd_req', instance.wallet_crowd_req)
        instance.wallet_crowd_desc = validated_data.get('wallet_crowd_desc', instance.wallet_crowd_desc)
        instance.crowd_img = validated_data.get('crowd_img', instance.crowd_img)
        if instance.wallet_crowd_req:
            pk=instance.wallet_id-5000
            profile = Profile.objects.get(pk=pk)
            wall = Wallet.objects.get(profile=profile)
            w = instance.wallet_crowd_req

            if w == wall.wallet_crowd_req:
                pass
            else:
                t_id = (str('TACR' + str(wall.wallet_id)[-1] + profile.first_name[2:3] + 'AD' + str(random.randint(1, 10000)))).upper()

                Transaction.objects.create(transaction_amount=w, receiver_id=2, sender_id=profile.pk,
                                           message="Requested Crowd", transaction_id=t_id)
        instance.save()
        return instance

    wallet_cash_req=serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    wallet_cash_desc = serializers.CharField(required=False,allow_null=True,allow_blank=True)
    wallet_img = Base64ImageField(max_length=None, use_url=True, required=False, allow_null=True, allow_empty_file=True)

    wallet_loan_req=serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    wallet_loan_desc = serializers.CharField(required=False,allow_null=True,allow_blank=True)
    loan_img = Base64ImageField(max_length=None, use_url=True, required=False, allow_null=True, allow_empty_file=True)

    wallet_savings_req=serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    wallet_savings_desc = serializers.CharField(required=False,allow_null=True,allow_blank=True)
    savings_img = Base64ImageField(max_length=None, use_url=True, required=False, allow_null=True, allow_empty_file=True)

    wallet_crowd_req=serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    wallet_crowd_desc = serializers.CharField(required=False,allow_null=True,allow_blank=True)
    crowd_img = Base64ImageField(max_length=None, use_url=True, required=False, allow_null=True, allow_empty_file=True)

    class Meta:
        model=Wallet
        read_only_fields=('wallet_id',)
        fields=('url','wallet_id','wallet_cash_req','wallet_cash_desc','wallet_img','wallet_loan_req','wallet_loan_desc','loan_img','wallet_crowd_req','wallet_crowd_desc','crowd_img','wallet_savings_req','wallet_savings_desc','savings_img')


