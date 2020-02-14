from django.contrib import admin,messages
from accounts.models import AppTransfer,Profile,Wallet,BarCodeTransfer,Transaction,Positions,PurchasedTicket,PurchasedGrocery,PurchasedContent,PurchasedCommodity,NewsPort
from django.utils.safestring import mark_safe
from django.utils.html import format_html
from django.urls import reverse,path
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import Group
import random
class ProfileAdmin(admin.ModelAdmin):
    def preview_image(self, obj):
        return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
                url = obj.image.url,
                width=obj.image.width,
                height=obj.image.height,
                )
        )

    fieldsets=(
    (None,{
        'fields':
        (
            ('user','barcode_val'),
            ('first_name','last_name'),
            ('email','mobile_no'),
            ('city','country'),
            ('ic','referral_contact'),
        ),
    }),
    ('Address Image',{
    'classes':('extrapretty',),
    'fields': ('address_line_1','address_line_2','postal_code','image','preview_image'),
    })
    )
    save_on_top=True
    readonly_fields=('preview_image',)
    list_display=('id','user_contact','fullname','user','email','city',)#'wallet_type')
    # list_filter=('city',)
    list_display_links=('user_contact','fullname','user')
    search_fields=('mobile_no',)
    # actions=[type_one, type_two, type_three]
    #radio_fields={'wallet_type': admin.HORIZONTAL}

    def user_contact(self,obj):
        return obj.__str__()

    def fullname(self,obj):
        return obj.first_name +' '+ obj.last_name

    def get_queryset(self,request):
        queryset=super(ProfileAdmin,self).get_queryset(request)
        queryset=queryset.order_by('user',)
        return queryset

class WalletAdmin(admin.ModelAdmin):

    def has_add_permission(self, request, obj=None):
        return False

    def wallet_receipt(self, obj):
        return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
                url = obj.wallet_img.url,
                width=150,
                height=200,
                )
        )

    def savings_receipt(self, obj):
        return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
                url = obj.savings_img.url,
                width=150,
                height=200,
                )
        )

    def crowd_receipt(self, obj):
        return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
                url = obj.crowd_img.url,
                width=150,
                height=200,
                )
        )

    def loan_receipt(self, obj):
        return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
                url = obj.loan_img.url,
                width=150,
                height=200,
                )
        )
    actions = ['cash_approve','loan_approve_action','savings_approve_action','crowd_approve_action']

    def cash_approve(self, request, queryset):
        try:
            rows_updated=0
            for wallet in queryset:
                if wallet.wallet_cash_req>0:
                    walletid=wallet.wallet_id
                    wall=wallet.wallet_cash_req
                    prof=Profile.objects.get(pk=walletid-5000).pk
                    amount=wallet.cash_balance+( wall * 90 / 100)
                    amount_four=wallet.total_trans_rec+wall

                    amount_two=wallet.wallet_bal+wall
                    amount_three=wallet.savings+( wall * 10 / 100)
                    profile=Profile.objects.get(pk=prof)

                    t_id=(str('TRAC'+str(walletid)[-1]+profile.mobile_no[2:3]+str(random.randint(1,10000))+'AD')).upper()
                    Wallet.objects.select_for_update().filter(wallet_id=walletid).update(wallet_bal=amount_two,cash_balance=amount,wallet_cash_req=0,loan_amt=amount_three,total_trans_rec=amount_four)
                    cr=wallet.wallet_bal
                    Transaction.objects.create(transaction_amount=wall,wallet_balance_rec=cr,receiver_id=prof,sender_id=2,message="Cash Req Approved",transaction_id=t_id)
                    rows_updated+=1
                else:
                    self.message_user(request, "Cannot approve non-requesting wallets!", level=messages.ERROR)
            if rows_updated == 1:
                message_bit = "1 cash wallet request was"
            elif rows_updated > 1:
                message_bit = "%s cash wallet requests were" % rows_updated
            self.message_user(request, "%s successfully approved." % message_bit)
        except:
            print('Cannot approve non-requested wallets')
    cash_approve.short_description = "Approve Cash Request"

    def loan_approve_action(self, request, queryset):
        try:
            rows_updated=0
            # print(queryset)
            for wallet in queryset:
                if wallet.wallet_loan_req>0:
                    walletid=wallet.wallet_id
                    wall=wallet.wallet_loan_req
                    prof=Profile.objects.get(pk=walletid-5000).pk
                    profile=Profile.objects.get(pk=prof)
                    loan=wallet.loan_amt+wall
                    t_id=(str('TRAL'+str(walletid)[-1]+profile.mobile_no[2:3]+str(random.randint(1,10000))+'AD')).upper()
                    Wallet.objects.select_for_update().filter(wallet_id=walletid).update(loan_amt=loan,wallet_loan_req=0)
                    cr=wallet.wallet_bal
                    Transaction.objects.create(transaction_amount=wall,wallet_balance_rec=cr,receiver_id=prof,sender_id=2,message="Loan Req Approved",transaction_id=t_id)

                    rows_updated+=1
                else:
                    self.message_user(request, "Cannot approve non-requesting wallets!", level=messages.ERROR)
            if rows_updated == 1:
                message_bit = "1 wallet loan request was"
            elif rows_updated > 1:
                message_bit = "%s wallet loan requests were" % rows_updated
            self.message_user(request, "%s successfully approved." % message_bit)

        except:
            print('Cannot approve non-requesting wallets')
    loan_approve_action.short_description = "Approve Loan Request"

    def savings_approve_action(self, request, queryset):
        try:
            rows_updated=0
            for wallet in queryset:
                if wallet.wallet_savings_req>0:
                    walletid=wallet.wallet_id
                    wall_bal= wallet.wallet_bal
                    wall=wallet.wallet_savings_req
                    wal_bal=wall_bal+wall
                    wall_tot_rec=wallet.total_trans_rec
                    wall_tot=wall_tot_rec+wall
                    prof=Profile.objects.get(pk=walletid-5000).pk
                    profile=Profile.objects.get(pk=prof)
                    sav=wall+wallet.savings
                    t_id=(str('TRAS'+str(walletid)[-1]+profile.mobile_no[2:3]+str(random.randint(1,10000))+'AD')).upper()
                    Wallet.objects.select_for_update().filter(wallet_id=walletid).update(savings=sav,wallet_balance_sent=cr,wallet_savings_req=0,wallet_bal=wal_bal,total_trans_rec=wall_tot)
                    wallet=Wallet.objects.get(wallet_id=walletid)
                    cr=wallet.wallet_bal
                    Transaction.objects.create(transaction_amount=wall,wallet_balance_rec=cr,receiver_id=prof,sender_id=2,message="Savings Req Approved",transaction_id=t_id)

                    rows_updated+=1
                else:
                    self.message_user(request, "Cannot approve non-requesting wallets!", level=messages.ERROR)
            if rows_updated == 1:
                message_bit = "1 wallet saving request was"
            elif rows_updated > 1:
                message_bit = "%s wallet saving requests were" % rows_updated
            self.message_user(request, "%s successfully approved." % message_bit)
        except:
            print('Cannot approve non-requesting wallets')
    savings_approve_action.short_description = "Approve Savings Request"


    def crowd_approve_action(self, request, queryset):
        try:
            rows_updated=0
            for wallet in queryset:
                if wallet.wallet_crowd_req>0:
                    walletid=wallet.wallet_id
                    wall=wallet.wallet_crowd_req
                    prof=Profile.objects.get(pk=walletid).pk
                    amount=wallet.crowd_wallet+wall
                    profile=Profile.objects.get(pk=prof-5000)
                    t_id=(str('TACR'+str(walletid)[-1]+profile.mobile_no[2:3]+str(random.randint(1,10000))+'AD')).upper()
                    Wallet.objects.select_for_update().filter(wallet_id=walletid).update(crowd_wallet=amount,wallet_crowd_req=0)
                    crec=wallet.wallet_bal
                    Transaction.objects.create(transaction_amount=wall,wallet_balance_rec=crec,receiver_id=prof,sender_id=2,message="Crowd Req Approved",transaction_id=t_id)

                    rows_updated+=1
                else:
                    self.message_user(request, "Cannot approve non-requesting wallets!", level=messages.ERROR)
            if rows_updated == 1:
                message_bit = "1 crowd wallet request was"
            elif rows_updated > 1:
                message_bit = "%s crowd wallet requests were" % rows_updated
            self.message_user(request, "%s successfully approved." % message_bit)
        except:
            print('Cannot approve non-requested wallets')
    crowd_approve_action.short_description = "Approve Crowd Request"


    fieldsets=(
        (None,
        {
            'fields':
                (('profile',),
                ('wallet_id','wallet_bal'),
                ('cash_balance','savings'),
                ('loan_amt','recycle_wallet'),
                ('incentive_wallet','crowd_wallet'),
                ('total_trans_rec','total_trans_sent'),
                ('wallet_cash_req','wallet_cash_desc',),
                ('wallet_img','wallet_receipt',),
                ('wallet_loan_req','wallet_loan_desc',),
                ('loan_img','loan_receipt',),
                ('wallet_savings_req','wallet_savings_desc',),
                ('savings_img', 'savings_receipt',),
                ('wallet_crowd_req', 'wallet_crowd_desc',),
                ('crowd_img', 'crowd_receipt',),)
        }
        ),
    )
    readonly_fields=('wallet_id','wallet_receipt','savings_receipt','loan_receipt','crowd_receipt','total_trans_sent','total_trans_rec')
    list_display=('name','wallet_id','mobile_number','wallet_bal','cash_balance','savings','loan_amt','crowd_wallet','wallet_cash_req','wallet_actions','wallet_loan_req','loan_actions','wallet_savings_req','savings_action','wallet_crowd_req','crowd_actions')
    list_display_links=('name','wallet_id')
    list_editable=('wallet_bal','cash_balance','savings','loan_amt','crowd_wallet')
    ordering=('wallet_loan_req',)


    def formfield_for_dbfield(self, db_field, **kwargs):
        field = super(WalletAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name in ("wallet_bal","crowd_wallet", "cash_balance","savings","incentive_wallet","recycle_wallet","loan_amt","wallet_cash_req","wallet_loan_req","wallet_savings_req","wallet_cash_desc","wallet_loan_desc","wallet_savings_desc","wallet_crowd_req","wallet_crowd_desc"):
            field.widget.attrs['style'] = 'text-align:center;'
        return field


    def name(self,obj):
        return obj.profile.first_name +' '+ obj.profile.last_name

    def mobile_number(self,obj):
        return obj.profile.mobile_no

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
                path('<int:wallet_id>/cash/approve',self.admin_site.admin_view(self.account_approve),name='account_approve',),
                path('<int:wallet_id>/cash/decline',self.admin_site.admin_view(self.account_decline),name='account_decline',),
                path('<int:wallet_id>/loan/approve',self.admin_site.admin_view(self.loan_approve),name='loan_approve',),
                path('<int:wallet_id>/loan/decline',self.admin_site.admin_view(self.loan_decline),name='loan_decline',),
                path('<int:wallet_id>/savings/decline',self.admin_site.admin_view(self.savings_decline),name='savings_decline',),
                path('<int:wallet_id>/savings/approve',self.admin_site.admin_view(self.savings_approve),name='savings_approve',),
                path('<int:wallet_id>/crowd/approve', self.admin_site.admin_view(self.crowd_approve),name='crowd_approve', ),
                path('<int:wallet_id>/crowd/decline', self.admin_site.admin_view(self.crowd_decline),name='crowd_decline', ),
        ]
        return custom_urls + urls

    def wallet_actions(self, obj):
        return format_html('<a class="button" href="{}">Approve</a>&nbsp;''<a class="button" href="{}">Decline</a>',reverse('admin:account_approve', args=[obj.wallet_id]),reverse('admin:account_decline', args=[obj.wallet_id]),)
    wallet_actions.short_description = 'Wallet Actions'
    wallet_actions.allow_tags = True

    def account_approve(modeladmin,request,wallet_id,*args,**kwargs):
        profile=''
        message=''
        wall=0
        try:
            wallet=Wallet.objects.get(wallet_id=wallet_id).profile
            wall=Wallet.objects.get(wallet_id=wallet_id).wallet_cash_req
            if wall>0:
                w=Wallet.objects.get(wallet_id=wallet_id).wallet_bal
                c=Wallet.objects.get(wallet_id=wallet_id).cash_balance
                s=Wallet.objects.get(wallet_id=wallet_id).savings
                t=Wallet.objects.get(wallet_id=wallet_id).total_trans_rec
                prof=Profile.objects.get(mobile_no=wallet).pk
                profile=Profile.objects.get(pk=prof)
                amount = c + (wall * 90 / 100)
                amount_two = w + wall
                amount_three = s + (wall * 10 / 100)
                amount_four= t + wall
                t_id=(str('TRAC'+str(wallet_id)[-1]+profile.mobile_no[2:3]+str(random.randint(1,10000))+'AD')).upper()
                Wallet.objects.select_for_update().filter(wallet_id=wallet_id).update(wallet_bal=amount_two,cash_balance=amount,savings=amount_three,total_trans_rec=amount_four)
                Wallet.objects.select_for_update().filter(wallet_id=wallet_id).update(wallet_cash_req=0)
                cr=Wallet.objects.get(wallet_id=wallet_id).wallet_bal
                Transaction.objects.create(transaction_amount=wall,wallet_balance_rec=cr,receiver_id=prof,sender_id=2,message="Cash Req Approved",transaction_id=t_id)
                message="Cash Added"
        except Wallet.DoesNotExist:
            return HttpResponse('Failed!')
        return render(request,'accounts/admin_approval.html',{'wall':wall,'profile':profile,'message':message})

    def account_decline(modeladmin,request,wallet_id,*args,**kwargs):
        try:
            # wall_mob=Wallet.objects.get(wallet_id=wallet_id).mobile_no
            # profile=Profile.objects.get(mobile_no=wall_mob)
            wallet=Wallet.objects.get(wallet_id=wallet_id).profile
            wall=Wallet.objects.get(wallet_id=wallet_id).wallet_cash_req
            if wall>0:
                prof=Profile.objects.get(mobile_no=wallet).pk
                profile=Profile.objects.get(pk=prof)
                t_id=(str('TRAC'+str(wallet_id)[-1]+profile.mobile_no[2:3]+str(random.randint(1,10000))+'AD')).upper()
                Wallet.objects.select_for_update().filter(wallet_id=wallet_id).update(wallet_cash_req=0)
                cr=Wallet.objects.get(wallet_id=wallet_id).wallet_bal
                Transaction.objects.create(transaction_amount=wall,receiver_id=prof,wallet_balance_rec=cr,sender_id=2,message="CASH req DECLINED!",transaction_id=t_id)
                message="Cash Denied"
        except Wallet.DoesNotExist:
            return HttpResponse('Failed')
        return render(request,'accounts/admin_approval.html',{'wall':wall,'profile':profile,'message':message})


    def loan_actions(self, obj):
        return format_html('<a class="button" href="{}">Approve</a>&nbsp;''<a class="button" href="{}">Decline</a>',reverse('admin:loan_approve', args=[obj.wallet_id]),reverse('admin:loan_decline', args=[obj.wallet_id]),)
    loan_actions.short_description = 'Loan Action'
    loan_actions.allow_tags = True

    def loan_approve(modeladmin,request,wallet_id,*args,**kwargs):
        profile=''
        message=''
        wall=0
        try:
            wall=Wallet.objects.get(wallet_id=wallet_id).wallet_loan_req
            # profile=Profile.objects.get(mobile_no=wall_mob)
            if wall>0:
                la=Wallet.objects.get(wallet_id=wallet_id).loan_amt
                wallet=Wallet.objects.get(wallet_id=wallet_id).profile
                prof=Profile.objects.get(mobile_no=wallet).pk
                profile=Profile.objects.get(pk=prof)
                t_id=(str('TRAL'+str(wallet_id)[-1]+profile.mobile_no[2:3]+str(random.randint(1,10000))+'AD')).upper()
                Wallet.objects.select_for_update().filter(wallet_id=wallet_id).update(loan_amt=la+wall)
                Wallet.objects.select_for_update().filter(wallet_id=wallet_id).update(wallet_loan_req=0)
                crec=Wallet.objects.get(wallet_id=wallet_id).wallet_bal
                Transaction.objects.create(transaction_amount=wall,wallet_balance_rec=crec,receiver_id=prof,sender_id=2,message="Loan Req Approved",transaction_id=t_id)
                message="Loan Added"
        except Wallet.DoesNotExist:
            return HttpResponse('Failed!')
        return render(request,'accounts/admin_approval.html',{'wall':wall,'profile':profile,'message':message})

    def loan_decline(modeladmin,request,wallet_id,*args,**kwargs):
        try:
            wallet=Wallet.objects.get(wallet_id=wallet_id).profile
            wall=Wallet.objects.get(wallet_id=wallet_id).wallet_loan_req
            if wall>0:
                prof=Profile.objects.get(mobile_no=wallet).pk
                profile=Profile.objects.get(pk=prof)
                t_id=(str('TRAL'+str(wallet_id)[-1]+profile.mobile_no[2:3]+str(random.randint(1,10000))+'AD')).upper()
                Wallet.objects.select_for_update().filter(wallet_id=wallet_id).update(wallet_loan_req=0)
                cr = Wallet.objects.get(wallet_id=wallet_id).wallet_bal
                Transaction.objects.create(transaction_amount=wall,wallet_balance_rec=cr,receiver_id=prof,sender_id=2,message="Loan req DECLINED!",transaction_id=t_id)
                message="Loan Denied"
        except Wallet.DoesNotExist:
            return HttpResponse('Failed')
        return render(request,'accounts/admin_approval.html',{'wall':wall,'profile':profile,'message':message})


    def crowd_actions(self, obj):
        return format_html('<a class="button" href="{}">Approve</a>&nbsp;''<a class="button" href="{}">Decline</a>',reverse('admin:crowd_approve', args=[obj.wallet_id]),reverse('admin:crowd_decline', args=[obj.wallet_id]),)
    crowd_actions.short_description = 'Crowd Action'
    crowd_actions.allow_tags = True



    def crowd_approve(modeladmin,request,wallet_id,*args,**kwargs):
        profile=''
        message=''
        wall=0
        try:
            wall=Wallet.objects.get(wallet_id=wallet_id).wallet_crowd_req
            # profile=Profile.objects.get(mobile_no=wall_mob)
            if wall>0:
                cr=Wallet.objects.get(wallet_id=wallet_id).crowd_wallet
                wallet=Wallet.objects.get(wallet_id=wallet_id).profile
                prof=Profile.objects.get(mobile_no=wallet).pk
                profile=Profile.objects.get(pk=prof)
                t_id=(str('TACR'+str(wallet_id)[-1]+profile.mobile_no[2:3]+str(random.randint(1,10000))+'AD')).upper()
                Wallet.objects.select_for_update().filter(wallet_id=wallet_id).update(crowd_wallet=cr+wall)
                Wallet.objects.select_for_update().filter(wallet_id=wallet_id).update(wallet_crowd_req=0)
                crec = Wallet.objects.get(wallet_id=wallet_id).wallet_bal
                Transaction.objects.create(transaction_amount=wall,wallet_balance_rec=crec,receiver_id=prof,sender_id=2,message="Crowd Req Approved",transaction_id=t_id)
                message="Crowd Added"
        except Wallet.DoesNotExist:
            return HttpResponse('Failed!')
        return render(request,'accounts/admin_approval.html',{'wall':wall,'profile':profile,'message':message})

    def crowd_decline(modeladmin,request,wallet_id,*args,**kwargs):
        try:
            wallet=Wallet.objects.get(wallet_id=wallet_id).profile
            wall=Wallet.objects.get(wallet_id=wallet_id).wallet_crowd_req
            if wall>0:
                prof=Profile.objects.get(mobile_no=wallet).pk
                profile=Profile.objects.get(pk=prof)
                t_id=(str('TACR'+str(wallet_id)[-1]+profile.mobile_no[2:3]+str(random.randint(1,10000))+'AD')).upper()
                Wallet.objects.select_for_update().filter(wallet_id=wallet_id).update(wallet_crowd_req=0)
                crec = Wallet.objects.get(wallet_id=wallet_id).wallet_bal
                Transaction.objects.create(transaction_amount=wall,receiver_id=prof,wallet_balance_rec=crec, sender_id=2,message="Crowd req DECLINED!",transaction_id=t_id)
                message="Crowd Denied"
        except Wallet.DoesNotExist:
            return HttpResponse('Failed')
        return render(request,'accounts/admin_approval.html',{'wall':wall,'profile':profile,'message':message})



    def savings_action(self, obj):
        return format_html('<a class="button" href="{}">Approve</a>&nbsp;''<a class="button" href="{}">Decline</a>',reverse('admin:savings_approve', args=[obj.wallet_id]),reverse('admin:savings_decline', args=[obj.wallet_id]),)
    savings_action.short_description = 'Savings Action'
    savings_action.allow_tags = True

    def savings_approve(modeladmin,request,wallet_id,*args,**kwargs):
        profile=''
        message=''
        wall=0
        try:
            wall=Wallet.objects.get(wallet_id=wallet_id).wallet_savings_req
            sav=Wallet.objects.get(wallet_id=wallet_id).savings
            w=Wallet.objects.get(wallet_id=wallet_id).wallet_bal
            # profile=Profile.objects.get(mobile_no=wall_mob)
            if wall>0:
                wallet=Wallet.objects.get(wallet_id=wallet_id).profile
                prof=Profile.objects.get(mobile_no=wallet).pk
                profile=Profile.objects.get(pk=prof)
                t_id=(str('TRAS'+str(wallet_id)[-1]+profile.mobile_no[2:3]+str(random.randint(1,10000))+'AD')).upper()
                Wallet.objects.select_for_update().filter(wallet_id=wallet_id).update(savings=sav+wall,wallet_bal=w+wall)
                Wallet.objects.select_for_update().filter(wallet_id=wallet_id).update(wallet_savings_req=0)
                crec=Wallet.objects.get(wallet_id=wallet_id).wallet_bal
                Transaction.objects.create(transaction_amount=wall,wallet_balance_rec=crec,receiver_id=prof,sender_id=2,message="Savings Req Approved",transaction_id=t_id)
                message="Savings Added"
        except Wallet.DoesNotExist:
            return HttpResponse('Failed!')
        return render(request,'accounts/admin_approval.html',{'wall':wall,'profile':profile,'message':message})

    def savings_decline(modeladmin,request,wallet_id,*args,**kwargs):
        try:
            wallet=Wallet.objects.get(wallet_id=wallet_id).profile
            wall=Wallet.objects.get(wallet_id=wallet_id).wallet_savings_req
            if wall>0:
                prof=Profile.objects.get(mobile_no=wallet).pk
                profile=Profile.objects.get(pk=prof)
                t_id=(str('TRAS'+str(wallet_id)[-1]+profile.mobile_no[2:3]+str(random.randint(1,10000))+'AD')).upper()
                Wallet.objects.select_for_update().filter(wallet_id=wallet_id).update(wallet_savings_req=0)
                crec=Wallet.objects.get(wallet_id=wallet_id).wallet_bal
                Transaction.objects.create(transaction_amount=wall,wallet_balance_rec=crec,receiver_id=prof,sender_id=2,message="Savings req DECLINED!",transaction_id=t_id)
                message="Savings Denied"
        except Wallet.DoesNotExist:
            return HttpResponse('Failed')
        return render(request,'accounts/admin_approval.html',{'wall':wall,'profile':profile,'message':message})



class TransactionAdmin(admin.ModelAdmin):

    list_display=('date_of_transaction','transaction_id','sender_name','receiver_name','transaction_amount','message')
    list_display_links=('date_of_transaction',)

    def sender_name(self,obj):
        return obj.sender.first_name +' '+ obj.sender.last_name

    def receiver_name(self,obj):
        return obj.receiver.first_name+' '+obj.receiver.last_name

    def has_add_permission(self, request):
        return False

class PurchasedTicketAdmin(admin.ModelAdmin):

    list_display=('date_of_purchase','ticket_id','transaction_id','profile_user','merchant_purchase','adult_qty','child_qty','ticket_amount')
    list_display_links=('date_of_purchase',)

    def profile_user(self,obj):
        return obj.user_profile.first_name +' '+ obj.user_profile.last_name

    def merchant_purchase(self,obj):
        return obj.merchant_purchased.merchant_contact_name

    def has_add_permission(self, request):
        return False

class UserAdmin(admin.ModelAdmin):
    list_display=('username','email_address','staff_status','super_user_status')


class PositionsAdmin(admin.ModelAdmin):
    list_display=('name','lattitude','longitude','previous_lattitude','previous_longitude','third_last_lattitude','third_last_longitude')

    def has_add_permission(self, request, obj=None):
        return False

    def name(self,obj):
        return obj.profile.first_name+' '+obj.profile.last_name

    def previous_lattitude(self,obj):
        return obj.latt_two
    def previous_longitude(self,obj):
        return obj.long_two

    def third_last_lattitude(self,obj):
        return obj.latt_three
    def third_last_longitude(self,obj):
        return obj.long_three

# from django.contrib.admin.models import LogEntry, DELETION
# from django.utils.html import escape
from django.urls import reverse

from django.contrib.admin.models import LogEntry
from django.contrib.contenttypes.models import ContentType


class PurchasedGroceryAdmin(admin.ModelAdmin):

    list_display=('profile_user','grocery_purchased','date_of_purchase','transaction_id','ticket_id','transaction_id')
    list_display_links=('date_of_purchase','ticket_id')
    readonly_fields = ('profile','grocery','date_of_purchase','transaction_id','ticket_id','transaction_id')

    def profile_user(self,obj):
        return obj.profile.first_name +' '+ obj.profile.last_name

    def grocery_purchased(self,obj):
        return obj.grocery.grocery_contact_name

    def has_add_permission(self, request):
        return False

class PurchasedCommodityAdmin(admin.ModelAdmin):

    list_display = ('profile_user','grocery','date_of_purchase','transaction_id','ticket_id','commodity_name','commodity_code')
    list_display_links = ('date_of_purchase','transaction_id')
    readonly_fields = ('purchased_groc','commodityitemcode','commodityitemname')

    def profile_user(self,obj):
        return obj.purchased_groc.profile.first_name +' '+ obj.purchased_groc.profile.last_name

    def grocery(self,obj):
        return obj.purchased_groc.grocery.grocery_contact_name

    def date_of_purchase(self,obj):
        return obj.purchased_groc.date_of_purchase

    def transaction_id(self,obj):
        return obj.purchased_groc.transaction_id

    def ticket_id(self,obj):
        return obj.purchased_groc.ticket_id

    def commodity_name(self,obj):
        return obj.commodityitemname

    def commodity_code(self,obj):
        return obj.commodityitemcode


    def has_add_permission(self, request):
        return False



class PurchasedContentAdmin(admin.ModelAdmin):

    list_display=('profile_user','grocery','date_of_purchase','transaction_id','commodity_name','qty_100gm','qty_200gm','qty_500gm','qty_1kg','qty_5kg','qty_25kg','qty_50kg','total_amt')
    list_display_links=('date_of_purchase','transaction_id')

    readonly_fields = ('purchased_item','hundredgramqty','twohundredgramqty','fivehundredgramqty','onekgqty','fivekgqty','twentyfivekgqty','fiftykgqty',
                       'hundredgramtotprice','twohundredgramtotprice','fivehundredgramtotprice','onekgtotprice','fivekgtotprice',
                       'twentyfivekgtotprice','fiftykgtotprice','totalcommamt')

    def profile_user(self,obj):
        return obj.purchased_item.purchased_groc.profile.first_name +' '+ obj.purchased_item.purchased_groc.profile.last_name

    def qty_100gm(self,obj):
        return obj.hundredgramqty

    def qty_200gm(self,obj):
        return obj.twohundredgramqty

    def total_amt(self,obj):
        return obj.totalcommamt

    def qty_500gm(self,obj):
        return obj.fivehundredgramqty

    def qty_1kg(self,obj):
        return obj.onekgqty

    def qty_5kg(self,obj):
        return obj.fivekgqty

    def qty_25kg(self,obj):
        return obj.twentyfivekgqty

    def qty_50kg(self,obj):
        return obj.fiftykgqty

    def grocery(self,obj):
        return obj.purchased_item.purchased_groc.grocery.grocery_contact_name

    def date_of_purchase(self,obj):
        return obj.purchased_item.purchased_groc.date_of_purchase

    def transaction_id(self,obj):
        return obj.purchased_item.purchased_groc.transaction_id

    def ticket_id(self,obj):
        return obj.purchased_item.purchased_groc.ticket_id

    def commodity_name(self,obj):
        return obj.purchased_item.commodityitemname

    def commodity_code(self,obj):
        return obj.purchased_item.commodityitemcode

    def has_add_permission(self, request):
        return False


    fieldsets=(
        (None,
        {
            'fields':
                (('purchased_item',),
                ('hundredgramqty','hundredgramtotprice',),
                ('twohundredgramqty','twohundredgramtotprice',),
                ('fivehundredgramqty', 'fivehundredgramtotprice',),
                ('onekgqty', 'onekgtotprice',),
                ('fivekgqty', 'fivekgtotprice',),
                ('twentyfivekgqty', 'twentyfivekgtotprice',),
                ('fiftykgqty', 'fiftykgtotprice'),
                ('totalcommamt',),)
        }
        ),
    )


class NewsPortAdmin(admin.ModelAdmin):
    readonly_fields=('news_title_slug',)


admin.site.register(Profile,ProfileAdmin)
admin.site.register(Positions,PositionsAdmin)
admin.site.register(Wallet,WalletAdmin)
admin.site.register(Transaction,TransactionAdmin)
admin.site.register(PurchasedTicket,PurchasedTicketAdmin)
admin.site.site_header='ePaySave ADMIN'
admin.site.site_title='ePaySave Admin Login'
admin.site.register(PurchasedContent,PurchasedContentAdmin)
admin.site.register(PurchasedCommodity,PurchasedCommodityAdmin)
admin.site.register(PurchasedGrocery,PurchasedGroceryAdmin)
admin.site.register(NewsPort,NewsPortAdmin)
admin.site.register(BarCodeTransfer)
admin.site.register(AppTransfer)