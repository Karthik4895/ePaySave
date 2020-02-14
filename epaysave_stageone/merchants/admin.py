from django.contrib import admin,messages
from .models import Merchant, MerchantItem
from accounts.models import MerchantTicket
from django.utils.safestring import mark_safe
from django.utils.html import format_html
from django.urls import reverse,path
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import Group

# class FilterUserAdmin(admin.ModelAdmin):


class MerchantAdmin(admin.ModelAdmin):
    def preview_img(self, obj):
        return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
                url = obj.merchant_img.url,
                width=obj.merchant_img.width,
                height=obj.merchant_img.height,
                )
        )
    fieldsets=(
    (None,{
        'fields':
        (
            ('user'),
            ('merchant_code','merchant_contact_email'),
            ('merchant_contact_no','merchant_contact_name'),
            ('merchant_city','merchant_country'),
            ('merchant_address','merchant_wallet'),
            ('merchant_img','preview_img')
        ),
    }),
    )
    save_on_top=True
    readonly_fields=('preview_img','merchant_wallet')
    list_display=('merchant_code','merchant_contact_no','merchant_contact_email','merchant_contact_name','merchant_city',
                   'merchant_country','merchant_address','merchant_wallet')
    # list_filter=('city',)
    list_display_links=('merchant_code','merchant_contact_email','merchant_contact_no')

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'user', None) is None:
            obj.user = request.user
        obj.save()

    def get_queryset(self, request):
        if request.user.is_superuser:
            return Merchant.objects.all()
        else:
            return Merchant.objects.filter(user=request.user)

    def has_add_permission(self, request, obj=None):
        if not obj:
            return request.user.is_superuser
        return obj.user == request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        if not obj:
            return True
        return obj.user == request.user or request.user.is_superuser

    # def get_queryset(self, request):
    #     qs = super(MerchantAdmin, self).queryset(request)
    #     if request.user.is_superuser:
    #         return qs
    #     return qs.filter(user=request.user)
    # search_fields=('mobile_no',)
    # actions=[type_one, type_two, type_three]
    #radio_fields={'wallet_type': admin.HORIZONTAL}

    # def user_contact(self,obj):
    #     return obj.__str__()
    #
    # def fullname(self,obj):
    #     return obj.first_name +' '+ obj.last_name
    #
    # def get_queryset(self,request):
    #     queryset=super(ProfileAdmin,self).get_queryset(request)
    #     queryset=queryset.order_by('user',)
    #     return queryset



class MerchantItemAdmin(admin.ModelAdmin):
    fieldsets=(
    # (None,{
    #     'fields':
    #     (
    #         ('merchant_code'),
    #         ('item_code','description'),
    #         ('adult_child','gender_allowed'),
    #         ('quantity','price'),
    #         ('discount'),
    #     ),
    # }),
    )
    save_on_top=True
    # readonly_fields=('',)
    list_display=('item_code','merchant_code','description','adult_child','gender_allowed',
                   'quantity','price','discount')
    # list_filter=('city',)
    list_display_links=('item_code','merchant_code')

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'user', None) is None:
            obj.user = request.user
        obj.save()

    def get_queryset(self, request):
        if request.user.is_superuser:
            return MerchantItem.objects.all()
        else:
            return MerchantItem.objects.filter(merchant_code__user=request.user)

    def has_change_permission(self, request, obj=None):
        if not obj:
            return True
        return obj.merchant_code.user == request.user or request.user.is_superuser

class MerchantTicketAdmin(admin.ModelAdmin):

    list_display=('date_of_purchase','ticket_id','profile_user','merchant_purchased','adult_qty','child_qty','ticket_amount')
    list_display_links=('date_of_purchase',)

    def profile_user(self,obj):
        return obj.user_profile.first_name +' '+ obj.user_profile.last_name

    def has_add_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'user', None) is None:
            obj.user = request.user
        obj.save()

    def get_queryset(self, request):
        if request.user.is_superuser:
            return MerchantTicket.objects.all()
        else:
            return MerchantTicket.objects.filter(merchant_purchased__user=request.user)

    def has_change_permission(self, request, obj=None):
        if not obj:
            return True
        return obj.user_profile.user == request.user or request.user.is_superuser


admin.site.register(Merchant,MerchantAdmin)
admin.site.register(MerchantItem,MerchantItemAdmin)
admin.site.register(MerchantTicket,MerchantTicketAdmin)