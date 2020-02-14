from django.contrib import admin,messages
from .models import Grocery, Commodity, CommodityItem

from django.utils.safestring import mark_safe
from django.utils.html import format_html
from django.urls import reverse,path
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import Group


# class FilterUserAdmin(admin.ModelAdmin):


class GroceryAdmin(admin.ModelAdmin):
    def preview_img(self, obj):
        return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
                url = obj.grocery_img.url,
                width=obj.grocery_img.width,
                height=obj.grocery_img.height,
                )
        )
    fieldsets=(
    (None,{
        'fields':
        (
            ('user'),
            ('grocery_code','grocery_contact_email'),
            ('grocery_contact_no','grocery_contact_name'),
            ('grocery_city','grocery_country'),
            ('grocery_address','grocery_wallet'),
            ('grocery_img','preview_img')
        ),
    }),
    )
    save_on_top=True
    readonly_fields=('preview_img',)
    list_display=('grocery_code','grocery_contact_no','grocery_contact_email','grocery_contact_name','grocery_city',
                   'grocery_country','grocery_address')
    list_display_links=('grocery_code','grocery_contact_email','grocery_contact_no')

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'user', None) is None:
            obj.user = request.user
        obj.save()

    def get_queryset(self, request):
        if request.user.is_superuser:
            return Grocery.objects.all()
        else:
            return Grocery.objects.filter(user=request.user)

    def has_add_permission(self, request, obj=None):
        if not obj:
            return request.user.is_superuser
        return obj.user == request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        if not obj:
            return True
        return obj.user == request.user or request.user.is_superuser



class CommodityAdmin(admin.ModelAdmin):
    fieldsets=(
    # (None,{
    #     'fields':
    #     (
    #         ('grocery_code'),
    #         ('item_code','description'),
    #         ('adult_child','gender_allowed'),
    #         ('quantity','price'),
    #         ('discount'),
    #     ),
    # }),
    )
    save_on_top=True
    # readonly_fields=('',)
    list_display=('commodity_code','grocery_code','commodity_desc')
    # list_filter=('city',)
    list_display_links=('commodity_code','grocery_code')

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'user', None) is None:
            obj.user = request.user
        obj.save()

    def get_queryset(self, request):
        if request.user.is_superuser:
            return Commodity.objects.all()
        else:
            return Commodity.objects.filter(grocery_code__user=request.user)

    def has_change_permission(self, request, obj=None):
        if not obj:
            return True
        return obj.grocery_code.user == request.user or request.user.is_superuser


class CommodityItemAdmin(admin.ModelAdmin):
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
    list_display=('commodity_item_code','commodity','item_desc','brand','hundred_gm',
                   'twohundred_gm','fivehundred_gm','one_kg','five_kg','twentyfive_kg','fifty_kg')
    # list_filter=('city',)
    list_display_links=('commodity_item_code','commodity')

    def commodity(self,obj):
        return obj.commodity_code.commodity_desc

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'user', None) is None:
            obj.user = request.user
        obj.save()

    def get_queryset(self, request):
        if request.user.is_superuser:
            return CommodityItem.objects.all()
        else:
            return CommodityItem.objects.filter(commodity_code__grocery_code__user=request.user)

    def has_change_permission(self, request, obj=None):
        if not obj:
            return True
        return obj.commodity_code.grocery_code.user == request.user or request.user.is_superuser

    def hundred_gm(self,obj):
        return obj.hundred_price

    def twohundred_gm(self,obj):
        return obj.twohundred_price

    def fivehundred_gm(self,obj):
        return obj.fivehundred_price

    def one_kg(self,obj):
        return obj.onekg_price

    def five_kg(self,obj):
        return obj.fivekg_price

    def twentyfive_kg(self,obj):
        return obj.twentyfivekg_price

    def fifty_kg(self,obj):
        return obj.fiftykg_price



admin.site.register(Grocery,GroceryAdmin)
admin.site.register(Commodity,CommodityAdmin)
admin.site.register(CommodityItem,CommodityItemAdmin)
