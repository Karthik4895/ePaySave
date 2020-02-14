from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from .models import AppTransfer,Profile,Wallet,Transaction,BarCodeTransfer,Positions,PurchasedTicket,PurchasedGrocery,PurchasedCommodity,PurchasedContent,NewsPort
from .forms import ProfileForm,UserForm
from rest_framework.authtoken.models import Token
from rest_framework import viewsets
from accounts.serializers import AppTransferSerializer,TransactionDispSerializer,BarCodeSerializer,CommodityItemSerializer,GroceryySerializer,PurchasedContentSerializer,MerchItemSerializer,ProfileSerializer,ProfilesSerializer,WalletSerializer,TransactionSerializer,UserSerializer, RequestsSerializer, LoginSerializer,PurchasedTicketSerializer,MerchSerializer
from decimal import Decimal
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden, JsonResponse
from django.contrib.auth.decorators import login_required,user_passes_test
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from groceries.models import Grocery, Commodity, CommodityItem
from datetime import datetime, timedelta
from merchants.models import Merchant, MerchantItem
import random
import requests
import json
from django.core import serializers
from django.template import RequestContext
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes , renderer_classes
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from django.views.decorators.csrf import ensure_csrf_cookie
# from django.http import HttpResponseRedirect
from django.db import connection





def index(request,pk=None):
    # rpk=request.user.pk
    if request.user.is_anonymous:
        news_portal=NewsPort.objects.all()
        news_little=NewsPort.objects.all()[1:5]
        news_first=NewsPort.objects.all()[1:5]
        return render(request,'accounts/index.html',{'pk': request.user.pk,'news_portal':news_portal,'slug':'',
                                                     'news_little':news_little, 'news_first':news_first, })
    else:
        profile=Profile.objects.get(user=request.user)
        news_portal=NewsPort.objects.all()
        news_little=NewsPort.objects.all()[1:5]

        news_first=NewsPort.objects.all()[1:5]
        return render(request,'accounts/index.html',{'profile':profile,'pk': profile.pk, 'news_first':news_first,
                                                     'news_portal': news_portal,'news_little': news_little,})


def news_desc(request,slug):
    # request.session.flush()
    news=NewsPort.objects.get(news_title_slug=str(slug))
    return render(request,'accounts/newsdesc.html',{'news':news, 'slug':slug})

def news_all(request):
    news_portal=NewsPort.objects.all()
    return render(request,'accounts/news_all.html',{'news_portal':news_portal,})



@login_required
def map_view(request,pk):
    if request.method=="POST":
        if request.POST.get('pos[lat]'):
            profile = Profile.objects.get(pk=pk)
            latt=request.POST.get('pos[lat]')
            lon=request.POST.get('pos[lng]')
            try:
                pos=Positions.objects.get(profile=profile)
                if pos.latt_five!=1 and pos.long_five!=1:
                    Positions.objects.select_for_update().filter(profile=profile).update(latt_five=pos.latt_four,
                                                                                         long_five=pos.long_four)

                    Positions.objects.select_for_update().filter(profile=profile).update(latt_four=pos.latt_three,
                                                                                         long_four=pos.long_three)

                    Positions.objects.select_for_update().filter(profile=profile).update(latt_three=pos.latt_two,
                                                                                         long_three=pos.long_two)

                    Positions.objects.select_for_update().filter(profile=profile).update(latt_two=pos.lattitude,
                                                                                         long_two=pos.longitude)

                    Positions.objects.select_for_update().filter(profile=profile).update(lattitude=latt,
                                                                                         longitude=lon)
                elif pos.latt_four!=1 and pos.long_four!=1:
                    Positions.objects.select_for_update().filter(profile=profile).update(latt_five=pos.latt_four,
                                                                                         long_five=pos.long_four)

                    Positions.objects.select_for_update().filter(profile=profile).update(latt_four=pos.latt_three,
                                                                                         long_four=pos.long_three)

                    Positions.objects.select_for_update().filter(profile=profile).update(latt_three=pos.latt_two,
                                                                                         long_three=pos.long_two)

                    Positions.objects.select_for_update().filter(profile=profile).update(latt_two=pos.lattitude,
                                                                                         long_two=pos.longitude)

                    Positions.objects.select_for_update().filter(profile=profile).update(lattitude=latt,
                                                                                         longitude=lon)

                elif pos.latt_three!=1 and pos.long_three!=1:
                    Positions.objects.select_for_update().filter(profile=profile).update(latt_four=pos.latt_three,
                                                                                         long_four=pos.long_three)

                    Positions.objects.select_for_update().filter(profile=profile).update(latt_three=pos.latt_two,
                                                                                         long_three=pos.long_two)

                    Positions.objects.select_for_update().filter(profile=profile).update(latt_two=pos.lattitude,
                                                                                         long_two=pos.longitude)

                    Positions.objects.select_for_update().filter(profile=profile).update(lattitude=latt,
                                                                                         longitude=lon)

                elif pos.latt_two!=1 and pos.long_two!=1:
                    Positions.objects.select_for_update().filter(profile=profile).update(latt_three=pos.latt_two,
                                                                                         long_three=pos.long_two)

                    Positions.objects.select_for_update().filter(profile=profile).update(latt_two=pos.lattitude,
                                                                                         long_two=pos.longitude)

                    Positions.objects.select_for_update().filter(profile=profile).update(lattitude=latt,
                                                                                         longitude=lon)

                elif pos.lattitude!=1 and pos.longitude!=1:
                    Positions.objects.select_for_update().filter(profile=profile).update(latt_two=pos.lattitude,
                                                                                         long_two=pos.longitude)

                    Positions.objects.select_for_update().filter(profile=profile).update(lattitude=latt,
                                                                                         longitude=lon)
                else:
                    Positions.objects.select_for_update().filter(profile=profile).update(lattitude=latt,
                                                                                         longitude=lon)


                Positions.objects.select_for_update().filter(profile=profile).update(lattitude=latt, longitude=lon)
            except Positions.DoesNotExist:
                position = Positions.objects.create(profile=profile, lattitude=latt, longitude=lon)
                position.save()
            print(request.POST.get('pos[lat]'))
            print(request.POST.get('pos[lng]'))
    return render(request,'accounts/index_with_pk.html',{})

@login_required
def index_with_pk(request,pk):
    if pk is None:
        return HttpResponseRedirect(reverse('index'))
    # user=User.objects.get(pk=pk)
    profile=Profile.objects.get(pk=pk)
    wallet=Wallet.objects.get(profile=profile)
    user=profile.user
    return render(request,'accounts/index_with_pk.html',{'profile':profile,'wallet':wallet,'pk':profile.pk,'user':user})

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

@login_required
def history_transac(request,pk):
    profile=Profile.objects.get(pk=pk)
    wallet=Wallet.objects.get(profile=profile)
    transac=Transaction.objects.filter(sender=profile)|Transaction.objects.filter(receiver=profile)
    transac_rev=transac.order_by('date_of_transaction').reverse()
    # transac.(Transaction.objects.filter(receiver=profile))
    print(transac.order_by('date_of_transaction').reverse())
    purch=False
    if request.POST.getlist('tran_id'):
        tranid=str(request.POST.getlist('tran_id')[0])

        
        purchased_contents=PurchasedContent.objects.filter(purchased_item__purchased_groc__transaction_id=tranid)
        purch=True
        sno=1
        totalamt=Decimal('0')
        content='<table class="table-hover table table-bordered" style="margin-bottom:30px;"><thead><th>S.No</th><th>Name</th><th>Qty</th><th>Weight</th><th>Price</th><th>Total</th></thead><tbody>'
        for p in purchased_contents:
            commodityitem = CommodityItem.objects.get(commodity_item_code=p.purchased_item.commodityitemcode)
            if p.hundredgramqty:
                content+="<tr><td>"+str(sno)+"</td><td>"+str(p.purchased_item.commodityitemname)+"</td><td>"+str(p.hundredgramqty)+"</td><td>100 gm</td><td>"+str(commodityitem.hundred_price)+"</td><td>"+str(p.hundredgramtotprice)+"</td></tr>"
                sno+=1
            if p.twohundredgramqty:
                content+="<tr><td>"+str(sno)+"</td><td>"+str(p.purchased_item.commodityitemname)+"</td><td>"+str(p.twohundredgramqty)+"</td><td>200 gm</td><td>"+str(commodityitem.twohundred_price)+"</td><td>"+str(p.twohundredgramtotprice)+"</td></tr>"
                sno+=1
            if p.fivehundredgramqty:
                content+="<tr><td>"+str(sno)+"</td><td>"+str(p.purchased_item.commodityitemname)+"</td><td>"+str(p.fivehundredgramqty)+"</td><td>500 gm</td><td>"+str(commodityitem.fivehundred_price)+"</td><td>"+str(p.fivehundredgramtotprice)+"</td></tr>"
                sno+=1
            if p.onekgqty:
                content+="<tr><td>"+str(sno)+"</td><td>"+str(p.purchased_item.commodityitemname)+"</td><td>"+str(p.onekgqty)+"</td><td>1 kg</td><td>"+str(commodityitem.onekg_price)+"</td><td>"+str(p.onekgtotprice)+"</td></tr>"
                sno+=1
            if p.fivekgqty:
                content+="<tr><td>"+str(sno)+"</td><td>"+str(p.purchased_item.commodityitemname)+"</td><td>"+str(p.fivekgqty)+"</td><td>5 kg</td><td>"+str(commodityitem.fivekg_price)+"</td><td>"+str(p.fivekgtotprice)+"</td></tr>"
                sno+=1
            if p.twentyfivekgqty:
                content+="<tr><td>"+str(sno)+"</td><td>"+str(p.purchased_item.commodityitemname)+"</td><td>"+str(p.twentyfivekgqty)+"</td><td>25 kg</td><td>"+str(commodityitem.twentyfivekg_price)+"</td><td>"+str(p.twentyfivekgtotprice)+"</td></tr>"
                sno+=1
            if p.fiftykgqty:
                content+="<tr><td>"+str(sno)+"</td><td>"+str(p.purchased_item.commodityitemname)+"</td><td>"+str(p.fiftykgqty)+"</td><td>50 kg</td><td>"+str(commodityitem.fiftykg_price)+"</td><td>"+str(p.fiftykgtotprice)+"</td></tr>"
                sno+=1
            totalamt+=p.totalcommamt
        dateti=Transaction.objects.get(transaction_id=tranid).date_of_transaction + timedelta(hours=8)
        dateti=dateti.strftime('%d %b-%Y %I:%M %p')
        content+="</tbody></table><h5 class='pb-3'>Purchased Date : "+str(dateti)+" SGT<br>Grand Total: "+str(totalamt)+" SGD.</h5>"
        return JsonResponse(content,safe=False)
    if request.POST.get('tra_id'):
        transid=str(request.POST.getlist('tra_id')[0])
        purchased_tickets=PurchasedTicket.objects.filter(transaction_id=transid)
        purch=True
        sno=1
        ticket_amt=Decimal('0')
        content='<table class="table-hover table table-bordered" style="margin-bottom:30px;"><thead><th>S.No</th><th>Merchant</th><th>Adult/Child</th><th>Qty</th><th>Price</th><th>Discount</th><th>Total</th></thead><tbody>'
        for purchased in purchased_tickets:
            merchant_pur=Merchant.objects.get(merchant_code=purchased.merchant_purchased)
            if purchased.adult_qty>0:
                merchantitms=MerchantItem.objects.filter(merchant_code=purchased.merchant_purchased)
                for m in merchantitms:
                    if m.adult_child=='A':
                        tot=Decimal((m.price-(m.price*m.discount/100))*purchased.adult_qty)
                        tot=round(tot,2)
                        content+='<tr><td>'+str(sno)+'</td><td>'+str(merchant_pur.merchant_contact_name)+'</td><td>Adult</td><td>'+str(purchased.adult_qty)+'</td><td>'+str(m.price)+'</td><td>'+str(m.discount)+'%</td><td>'+str(tot)+'</td></tr>'
                        sno+=1
                    elif m.adult_child=='B':
                        tot=Decimal((m.price-(m.price*m.discount/100))*purchased.adult_qty)
                        tot=round(tot,2)
                        content+='<tr><td>'+str(sno)+'</td><td>'+str(merchant_pur.merchant_contact_name)+'</td><td>Adult</td><td>'+str(purchased.adult_qty)+'</td><td>'+str(m.price)+'</td><td>'+str(m.discount)+'%</td><td>'+str(tot)+'</td></tr>'
                        sno+=1
            if purchased.child_qty>0:
                merchantitms=MerchantItem.objects.filter(merchant_code=purchased.merchant_purchased)
                for m in merchantitms:
                    if m.adult_child=='C':
                        tot=Decimal((m.price-(m.price*m.discount/100))*purchased.child_qty)
                        tot=round(tot,2)
                        content+='<tr><td>'+str(sno)+'</td><td>'+str(merchant_pur.merchant_contact_name)+'</td><td>Child</td><td>'+str(purchased.child_qty)+'</td><td>'+str(m.price)+'</td><td>'+str(m.discount)+'%</td><td>'+str(tot)+'</td></tr>'
                        sno+=1
                    elif m.adult_child=='B':
                        tot=Decimal((m.price-(m.price*m.discount/100))*purchased.child_qty)
                        tot=round(tot,2)
                        content+='<tr><td>'+str(sno)+'</td><td>'+str(merchant_pur.merchant_contact_name)+'</td><td>Child</td><td>'+str(purchased.child_qty)+'</td><td>'+str(m.price)+'</td><td>'+str(m.discount)+'%</td><td>'+str(tot)+'</td></tr>'
                        sno+=1
            ticket_amt=purchased.ticket_amount
        dateti=Transaction.objects.get(transaction_id=transid).date_of_transaction + timedelta(hours=8)
        dateti=dateti.strftime('%d %b-%Y %I:%M %p')
        content+="</tbody></table><h5 class='pb-3'>Purchased Date : "+str(dateti)+" SGT<br>Grand Total: "+str(ticket_amt)+" SGD.</h5>"
        return JsonResponse(content,safe=False)



    return render(request,'accounts/transaction.html',{'profile':profile,'wallet':wallet,'transac':transac,'pk':pk, 'purch':purch, 'transac_rev':transac_rev})

@login_required
def wallet_view(request,pk):
    success=False
    loan=False
    cash=False
    savings=False
    crowd=False
    profile=Profile.objects.get(pk=pk)
    wallet=Wallet.objects.get(profile=profile)
    profiles=serializers.serialize("json",Profile.objects.all())
    w=''
    desc=''
    a=''
    prof=''
    t_id=''
    failed=False
    image=''
    bal_low=False
    mob_wrong=False
    invalid = False
    transact=Transaction.objects.filter(sender=profile)|Transaction.objects.filter(receiver=profile)
    transact_rev=transact.order_by('date_of_transaction').reverse()[0:5]
    print(transact_rev)
    # transact_rev=transact_rev[:5]
    if request.method == "POST":
        invalid = False
        print(request.POST)
        if "cash_req" in request.POST:
            print(request.POST)
            w=request.POST.getlist('cash_req')
            pk=int(request.POST.getlist('profpk1')[0])
            desc=request.POST.getlist('cash_desc')
            if 'cash_img' in request.FILES:
                image=request.FILES['cash_img']
            else:
                pass
            try:
                win=float(w[0])
                if type(win) == type(0.0):
                    print("HII! ",win)
                    try:
                        print(pk)
                        profile=Profile.objects.get(pk=pk)
                        wall=Wallet.objects.get(profile=profile)
                        if wall.profile.mobile_no == profile.mobile_no:
                            cash = True
                            w = w[0]
                            a = float(w)
                            desc = desc[0]
                            wall_cash=wall.wallet_cash_req
                            wall_cash_bal=wall_cash+Decimal(a)
                            t_id=(str('TRAC'+str(wall.wallet_id)[-1]+profile.first_name[2:3]+'AD'+str(random.randint(1,10000)))).upper()
                            if image!='':
                                wall.wallet_img.save(image.name,image)
                            Wallet.objects.select_for_update().filter(profile=profile).update(wallet_cash_req=wall_cash_bal,wallet_cash_desc=desc)
                            wall=Wallet.objects.get(profile=profile)
                            c = wall.wallet_bal
                            Transaction.objects.create(transaction_amount=w,wallet_balance_sent=c,receiver_id=2,sender_id=profile.pk,message="Requested Cash",transaction_id=t_id)

                    except Profile.DoesNotExist:
                        wall_prof=Wallet.objects.create(profile_id=profile.pk,wallet_cash_req=w,wallet_cash_desc=desc,wallet_img=image)
                        wall_prof.save()
                else:
                    print("In other")
                    invalid = True
            except:
                print('In other other')
                invalid = True
            data = {'pk': pk, 'success': success, 'cash': cash, 'loan': loan, 'savings': savings, 'w': w,
                    'desc': desc, 'a': a, 't_id': t_id, 'failed': failed, 'crowd': crowd,
                    'mob_wrong': mob_wrong, 'bal_low': bal_low, 'invalid': invalid}
            return JsonResponse(data)
        elif "save_req" in request.POST:
            print(request.POST)
            w=request.POST.getlist('save_req')
            desc=request.POST.getlist('savings_desc')
            pk=int(request.POST.getlist('profpk2')[0])
            if 'save_img' in request.FILES:
                image = request.FILES['save_img']
            else:
                pass
            print(w[0]+' '+desc[0])
            try:
                win=float(w[0])
                if type(win) == type(0.0):
                    try:
                        profile=Profile.objects.get(pk=pk)
                        wall=Wallet.objects.get(profile=profile)
                        if wall.profile.mobile_no == profile.mobile_no:
                            savings=True
                            a =float(w[0])
                            wall_save=wall.wallet_savings_req
                            wall_save_bal=Decimal(w[0]) + wall_save
                            t_id=(str('TRAS'+str(wall.wallet_id)[-1]+profile.first_name[2:3]+'AD'+str(random.randint(1,10000)))).upper()
                            if image!='':
                                wall.savings_img.save(image.name,image)
                            Wallet.objects.select_for_update().filter(profile=profile).update(wallet_savings_req=wall_save_bal,wallet_savings_desc=desc[0])
                            wall=Wallet.objects.get(profile=profile)
                            c=wall.wallet_bal
                            Transaction.objects.create(transaction_amount=w[0],wallet_balance_sent=c,receiver_id=2,sender_id=profile.pk,message="Requested Savings",transaction_id=t_id)

                    except Profile.DoesNotExist:
                        wall_prof=Wallet.objects.create(profile_id=profile.pk,wallet_savings_req=w[0],wallet_savings_desc=desc[0])
                        wall_prof.save()
                else:
                    invalid = True
            except:
                invalid = True
            data = {'pk': pk, 'success': success, 'cash': cash, 'loan': loan, 'savings': savings, 'w': w,
                    'desc': desc, 'a': a, 't_id': t_id, 'failed': failed, 'crowd': crowd,
                    'mob_wrong': mob_wrong, 'bal_low': bal_low, 'invalid': invalid}
            return JsonResponse(data)
        elif "crowd_req" in request.POST:
            w=request.POST.getlist('crowd_req')
            desc=request.POST.getlist('crowd_desc')
            pk=int(request.POST.getlist('profpk3')[0])
            if 'crowd_img' in request.FILES:
                image = request.FILES['crowd_img']
            else:
                pass
            print(w[0]+' '+desc[0])
            try:
                win=float(w[0])
                if type(win) == type(0.0):
                    try:
                        profile=Profile.objects.get(pk=pk)
                        wall=Wallet.objects.get(profile=profile)
                        if wall.profile.mobile_no == profile.mobile_no:
                            crowd=True
                            a=float(w[0])
                            wall_crowd=wall.wallet_crowd_req
                            wall_crowd_bal=Decimal(w[0])+wall_crowd
                            t_id=(str('TACR'+str(wall.wallet_id)[-1]+profile.first_name[2:3]+'AD'+str(random.randint(1,10000)))).upper()
                            if image!='':
                                wall.crowd_img.save(image.name,image)
                            Wallet.objects.select_for_update().filter(profile=profile).update(wallet_crowd_req=wall_crowd_bal,wallet_crowd_desc=desc[0])
                            wall=Wallet.objects.get(profile=profile)
                            c=wall.wallet_bal
                            Transaction.objects.create(transaction_amount=w[0],wallet_balance_sent=c,receiver_id=2,sender_id=profile.pk,message="Requested Crowd",transaction_id=t_id)

                    except Wallet.DoesNotExist:
                        wall_prof=Wallet.objects.create(profile_id=profile.pk,wallet_crowd_req=w[0],wallet_crowd_desc=desc[0])
                        wall_prof.save()
                else:
                    invalid = True
            except:
                invalid = True
            data = {'pk': pk, 'success': success, 'cash': cash, 'loan': loan, 'savings': savings, 'w': w,
                    'desc': desc, 'a': a, 't_id': t_id, 'failed': failed, 'crowd': crowd,
                    'mob_wrong': mob_wrong, 'bal_low': bal_low, 'invalid': invalid}
            return JsonResponse(data)
        elif "loan_req" in request.POST:
            w=request.POST.getlist('loan_req')
            desc=request.POST.getlist('loan_desc')
            pk=int(request.POST.getlist('profpk4')[0])
            if 'loan_img' in request.FILES:
                image=request.FILES['loan_img']
            else:
                pass
            print(w[0]+' '+desc[0])
            try:
                win=float(w[0])
                if type(win) == type(0.0):
                    try:
                        profile=Profile.objects.get(pk=pk)
                        wall=Wallet.objects.get(profile=profile)
                        if wall.profile.mobile_no == profile.mobile_no:
                            loan=True
                            a=float(w[0])
                            wall_loan=wall.wallet_loan_req
                            wall_loan_bal=Decimal(w[0])+wall_loan
                            t_id=(str('TRAL'+str(wall.wallet_id)[-1]+profile.first_name[2:3]+'AD'+str(random.randint(1,10000)))).upper()
                            if image!='':
                                wall.loan_img.save(image.name,image)
                            Wallet.objects.select_for_update().filter(profile=profile).update(wallet_loan_req=wall_loan_bal,wallet_loan_desc=desc[0])
                            wall=Wallet.objects.get(profile=profile)
                            c=wall.wallet_bal
                            Transaction.objects.create(transaction_amount=w[0],wallet_balance_sent=c,receiver_id=2,sender_id=profile.pk,message="Requested Loan",transaction_id=t_id)

                    except Wallet.DoesNotExist:
                        wall_prof=Wallet.objects.create(profile_id=profile.pk,wallet_loan_req=w[0],wallet_loan_desc=desc[0])
                        wall_prof.save()
                else:
                    invalid = True
            except:
                invalid = True
            data = {'pk': pk, 'success': success, 'cash': cash, 'loan': loan, 'savings': savings, 'w': w,
                    'desc': desc, 'a': a, 't_id': t_id, 'failed': failed, 'crowd': crowd,
                    'mob_wrong': mob_wrong, 'bal_low': bal_low, 'invalid': invalid}
            return JsonResponse(data)
        elif "mobile_no_to" in request.POST:
            receiver_name=''
            num=request.POST.getlist('mobile_no_to')
            print(num[0])
            try:
                if num[0] == profile.mobile_no:
                    failed=True
                elif num[0] == Profile.objects.get(mobile_no=num[0]).mobile_no:
                    prof=Profile.objects.get(mobile_no=num[0])
                    wallet_rec=Wallet.objects.get(profile=prof)
                    if 'demo' in request.POST:
                        c=request.POST.getlist('demo')
                        a=Decimal(c[0])
                        print(a)
                        if a>wallet.cash_balance:
                            bal_low = True
                            # return HttpResponse('Failed Transaction! You cannot attempt to transfer cash more than available balance!!')
                        else:
                            b=wallet.cash_balance-a
                            h=wallet.wallet_bal-a
                            j=wallet.total_trans_sent+a
                            d=wallet_rec.cash_balance+a
                            e=wallet_rec.wallet_bal+a
                            f=wallet_rec.total_trans_rec+a


                            Wallet.objects.select_for_update().filter(profile=profile).update(cash_balance=b)
                            Wallet.objects.select_for_update().filter(profile=profile).update(wallet_bal=h)
                            Wallet.objects.select_for_update().filter(profile=profile).update(total_trans_sent=j)
                            Wallet.objects.select_for_update().filter(profile=prof).update(cash_balance=d)
                            Wallet.objects.select_for_update().filter(profile=prof).update(wallet_bal=e)
                            Wallet.objects.select_for_update().filter(profile=prof).update(total_trans_rec=f)
                            t_id=(str('TRT'+str(wallet_rec.wallet_id)[-1]+profile.first_name[2:3]+'FF'+prof.mobile_no[6:7]+prof.city[:2]+str(random.randint(1,10000)))).upper()
                            wallet_rec = Wallet.objects.get(profile=prof)
                            wallet = Wallet.objects.get(profile=profile)
                            c=wallet.wallet_bal
                            cr=wallet_rec.wallet_bal
                            Transaction.objects.create(transaction_amount=a,wallet_balance_sent=c,wallet_balance_rec=cr,sender_id=profile.pk,receiver_id=prof.pk,message="Transfer",transaction_id=t_id)
                            receiver_name=prof.first_name+" "+prof.last_name
                            success=True
            except Profile.DoesNotExist:
                mob_wrong=True
            data = {'pk': pk, 'success': success, 'cash': cash, 'loan': loan, 'savings': savings, 'w': w,
                    'desc': desc, 'a': a, 't_id': t_id, 'failed': failed, 'crowd': crowd,
                    'mob_wrong': mob_wrong, 'bal_low': bal_low, 'invalid': invalid, 'receiver_name':receiver_name}
            return JsonResponse(data)
                # return HttpResponse('Failed Transaction!!Mobile no doesnt match any number registered on our site! Pls ask your friend to signup!')
        elif "mobile_no_loc" in request.POST:
            receiver_name=''
            mobnum=request.POST.getlist('mobile_no_loc')
            print(mobnum[0])
            try:
                if mobnum[0] == profile.mobile_no:
                    failed=True
                elif mobnum[0] == Profile.objects.get(mobile_no=mobnum[0]).mobile_no:
                    prof=Profile.objects.get(mobile_no=mobnum[0])
                    wallet_rec=Wallet.objects.get(profile=prof)
                    if 'amount_loc' in request.POST:
                        c=request.POST.getlist('amount_loc')
                        a=c[0]
                        a=Decimal(a)
                        print(a)
                        if a>wallet.cash_balance:
                            bal_low=True
                            # return HttpResponse('Failed Transaction! You cannot attempt to transfer cash more than available balance!!')
                        else:
                            b=wallet.cash_balance-a
                            h=wallet.wallet_bal-a
                            j=wallet.total_trans_sent+a

                            d=wallet_rec.cash_balance+a
                            e=wallet_rec.wallet_bal+a
                            f=wallet_rec.total_trans_rec+a

                            Wallet.objects.select_for_update().filter(profile=profile).update(cash_balance=b)
                            Wallet.objects.select_for_update().filter(profile=profile).update(wallet_bal=h)
                            Wallet.objects.select_for_update().filter(profile=profile).update(total_trans_sent=j)

                            Wallet.objects.select_for_update().filter(profile=prof).update(cash_balance=d)
                            Wallet.objects.select_for_update().filter(profile=prof).update(wallet_bal=e)
                            Wallet.objects.select_for_update().filter(profile=prof).update(total_trans_rec=f)

                            t_id=(str('TRT'+str(wallet_rec.wallet_id)[-1]+profile.first_name[2:3]+'FF'+prof.mobile_no[6:7]+prof.city[:2]+str(random.randint(1,10000)))).upper()
                            c=wallet.wallet_bal
                            cr=wallet_rec.wallet_bal
                            Transaction.objects.create(transaction_amount=a,sender_id=profile.pk,wallet_balance_sent=c,wallet_balance_rec=cr,receiver_id=prof.pk,message="Transfer",transaction_id=t_id)
                            success=True
                            receiver_name=prof.first_name+" "+prof.last_name
            except Profile.DoesNotExist:
                mob_wrong=True
                # return HttpResponse('Failed Transaction!!Mobile no doesnt match any number registered on our site! Pls ask your friend to signup!')
            data = {'pk': pk, 'success': success, 'cash': cash, 'loan': loan, 'savings': savings, 'w': w,
                    'desc': desc, 'a': a, 't_id': t_id, 'failed': failed, 'crowd': crowd,
                    'mob_wrong': mob_wrong, 'bal_low': bal_low, 'invalid': invalid, 'receiver_name':receiver_name}
            return JsonResponse(data)

        else:
            pass
        profile=serializers.serialize("json",Profile.objects.all())
        wallet = serializers.serialize("json",Wallet.objects.all())
    return JsonResponse({'profile':profile,'pk':pk,'success':success,'wallet':wallet,
                                                  'cash':cash,'loan':loan,'profiles':profiles,'savings':savings,
                                                                                                                                                                      'w':w,'desc':desc,'prof':prof,'a':a,'t_id':t_id,'failed':failed,
                                                  'image':image,'crowd':crowd,'mob_wrong':mob_wrong,'bal_low':bal_low,
                                                  'invalid':invalid,'transact':transact,'transact_rev':transact_rev})



@user_passes_test(lambda u: u.is_anonymous)
def signup(request):
    registered=False
    failed_ref=False
    wrong_ref=False
    if request.method=='POST':
        user_form = UserForm(data=request.POST)
        profile_form = ProfileForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user=user
            profile.save()
            response = {'status':'success','message':'Registered Successfully'}
            return JsonResponse(response,safe=False)

        elif user_form.errors:
            ress = {'status':'Failed','message':'Username already Exists'}
            return JsonResponse(ress,safe=False)
        elif profile_form.errors:
            resss = {'status':'Failed','message':'mobile number already Exists or Check if all values has been entered correctly'}
            return JsonResponse(resss,safe=False)

    else:
        user_form = UserForm()
        profile_form = ProfileForm()
    return JsonResponse({'user_form':user_form,'profile_form':profile_form})




@user_passes_test(lambda u: u.is_anonymous)
def user_login(request):
    user=0
    inactive=0
    context = RequestContext(request)
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(username=username,password=password)
        if user:
            if user.is_active:
                response = {
                    "status":"success",
                    "message":{"username":username,"password":password}
                }

                return JsonResponse(response,safe=False)
            else:
                inactive = 1
                return render(request, 'accounts/login.html', {'user': user, 'inactive':inactive})
        else:
            return JsonResponse({"status":"failed","message":"username or password is incorrect"})
            user=1
            return render(request, 'accounts/login.html', {'user': user, 'inactive': inactive})
    else:
        return render(request,'accounts/login.html',{'user':user, 'inactive': inactive},context_instance=context)

@login_required
def profile_edit(request, pk, template_name='profile_edit.html'):
    prof=Profile.objects.get(pk=pk)
    wallet=Wallet.objects.get(profile=prof)
    if id:
        profile = get_object_or_404(Profile, pk=pk)
        # user = get_object_or_404(User, pk=id)
        if profile.user != request.user:
            return HttpResponseForbidden()
    else:
        profile = Profile(user=request.user)
        if 'image' in request.FILES:
            profile.image = request.FILES['image']
    profile_form = ProfileForm(request.POST,request.FILES, instance=profile)
    if request.POST and profile_form.is_valid():
        profile_form.save()

        redirect_url = reverse('accounts:profile_detail',kwargs={'pk':pk})
        return redirect(redirect_url)
    return render(request,'accounts/profile_edit.html',{'profile_form':profile_form, 'pk':pk, 'wallet':wallet,'profile':profile})

@permission_classes((IsAdminUser,))
class ProfileView(viewsets.ModelViewSet):
    queryset=Profile.objects.all()
    serializer_class=ProfileSerializer
    def list(self,request):
        return Response({'message':'Append Profile ID to the API to view Profile of Particular User'})

    def get_serializer_class(self):
        serializer_class = self.serializer_class

        if self.request.method == 'PUT' or self.request.method == 'PATCH':
            serializer_class = ProfilesSerializer

        return serializer_class



    # def get_permissions(self):
    #     if self.request.method == 'DELETE':
    #         return [IsAdminUser()]
    #     elif self.request.method == 'POST':
    #         return [AllowAny()]
    #     else:
    #         return [IsStaffOrTargetUser()]


@permission_classes((IsAdminUser,))
class UserView(viewsets.ViewSet):
    queryset=User.objects.all()
    serializer_class=UserSerializer



@permission_classes((IsAdminUser,))
class LoginView(viewsets.ModelViewSet):
    queryset = Token.objects.all()
    serializer_class = LoginSerializer
    http_method_names = ['get', 'head']




@permission_classes((IsAdminUser,))
class WalletView(viewsets.ModelViewSet):
    queryset=Wallet.objects.all()
    serializer_class=WalletSerializer
    http_method_names = ['get', 'head', 'put', 'patch']
    def list(self,request):
        return Response({'message':'Append Wallet ID to the API to view Wallet of Particular User'})


@permission_classes((IsAdminUser,))
class BarCodeView(viewsets.ModelViewSet):
    queryset=BarCodeTransfer.objects.all()
    serializer_class=BarCodeSerializer
    http_method_names = ['get', 'head', 'post']

    def list(self,request):
        return Response({'message':'You should use POST with parameters'})

    def create(self, request, *args, **kwargs):
        serializer = BarCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        print(serializer.validated_data)
        t_id=''
        if serializer.validated_data['transaction_amount']:
            print(serializer.validated_data)
            pk=serializer.validated_data['sender_profile_id']
            try:
                profile = Profile.objects.get(pk=pk)
                wall = Wallet.objects.get(profile=profile)
                ws = wall.wallet_bal
                cs = wall.cash_balance
                amt = serializer.validated_data['transaction_amount']
                if amt>cs:
                    status='Transaction Failed. Not enough balance to send!'
                    return Response({'status':status})
                else:
                    wse=ws-amt
                    cse=cs-amt
                    Wallet.objects.select_for_update().filter(profile=profile).update(wallet_bal=wse,
                                                                                      cash_balance=cse)

                    barcode=serializer.validated_data['receiver_barcode']
                    prof = Profile.objects.get(barcode_val=barcode)
                    wallrec = Wallet.objects.get(profile=prof)
                    wr = wallrec.wallet_bal
                    cr = wallrec.cash_balance
                    wsr=wr+amt
                    crr=cr+amt
                    Wallet.objects.select_for_update().filter(profile=prof).update(wallet_bal=wsr,
                                                                                      cash_balance=crr)

                    t_id = (str('TRAC' + str(wall.wallet_id)[-1] + profile.first_name[2:3] + 'AD' + str(random.randint(1, 10000)))).upper()
                    Transaction.objects.create(transaction_amount=amt, receiver_id=prof.pk, wallet_balance_sent=wse, wallet_balance_rec=wsr,sender_id=profile.pk,message="BarCode Transfer", transaction_id=t_id)
            except Profile.DoesNotExist:
                status = 'Transaction Failed. Such Profile does not exist!'
                return Response({'status': status})
        bartran = BarCodeTransfer.objects.create(**serializer.validated_data,transaction_id=t_id)
        prof = Profile.objects.get(barcode_val=bartran.receiver_barcode)
        return Response({'status':'Successful Bar Code Transfer','Sender':bartran.sender_profile_id,'Receiver':prof.pk,'Transfer Amt':bartran.transaction_amount,'Transaction ID':bartran.transaction_id})



@permission_classes((IsAdminUser,))
class AppTransferView(viewsets.ModelViewSet):
    queryset=AppTransfer.objects.all()
    serializer_class=AppTransferSerializer
    http_method_names = ['get', 'head', 'post']
    def list(self,request):
        return Response({'message':'You should use POST with parameters'})

    def create(self, request, *args, **kwargs):
        serializer = AppTransferSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        print(serializer.validated_data)
        t_id=''
        if serializer.validated_data['transaction_amount']:
            print(serializer.validated_data)
            pk=serializer.validated_data['sender_profile_id']
            try:
                profile = Profile.objects.get(pk=pk)
                wall = Wallet.objects.get(profile=profile)
                ws = wall.wallet_bal
                cs = wall.cash_balance
                amt = serializer.validated_data['transaction_amount']
                if amt>cs:
                    return Response({'status': 'No Enough Funds for Transfer'})
                else:
                    wse=ws-amt
                    cse=cs-amt
                    Wallet.objects.select_for_update().filter(profile=profile).update(wallet_bal=wse,
                                                                                      cash_balance=cse)

                    pkr=serializer.validated_data['receiver_profile_id']
                    prof = Profile.objects.get(pk=pkr)
                    wallrec = Wallet.objects.get(profile=prof)
                    wr = wallrec.wallet_bal
                    cr = wallrec.cash_balance
                    wsr=wr+amt
                    crr=cr+amt
                    Wallet.objects.select_for_update().filter(profile=prof).update(wallet_bal=wsr,
                                                                                      cash_balance=crr)

                    t_id = (str('TRAC' + str(wall.wallet_id)[-1] + profile.first_name[2:3] + 'AD' + str(random.randint(1, 10000)))).upper()
                    Transaction.objects.create(transaction_amount=amt, receiver_id=prof.pk, wallet_balance_sent=wse, wallet_balance_rec=wsr,sender_id=profile.pk,message="App Transfer", transaction_id=t_id)
            except Profile.DoesNotExist:
                message='Sorry! Cannot transfer! Profile does not exist!'
                return Response({'messages':message,})
        app = AppTransfer.objects.create(**serializer.validated_data,transaction_id=t_id,)
        return Response({'message':'Transfer Successful','Transfer Amt':app.transaction_amount,'Sender':app.sender_profile_id,'Receiver':app.receiver_profile_id,'Transaction ID':app.transaction_id})


@permission_classes((IsAdminUser,))
class TransactionView(viewsets.ModelViewSet):
    queryset=Transaction.objects.all()
    serializer_class=TransactionSerializer
    http_method_names = ['get', 'head']




@permission_classes((IsAdminUser,))
class TransactionsView(viewsets.ViewSet):
    serializer_class = TransactionSerializer
    def list(self,request):
        # transac=Transaction.objects.all().values()
        return Response({'message':'Append Profile ID to the API to view Transactions of Particular User'})

    def retrieve(self,request,pk=None):
        try:
            profile=Profile.objects.get(pk=pk)
            transact=(Transaction.objects.filter(sender=profile) | Transaction.objects.filter(receiver=profile)).values()
            if len(transact) != 0:
                tran_rev=transact.order_by('date_of_transaction').reverse()
                return Response({'Transactions':list(tran_rev)})
            else:
                return Response({'Transactions':'No Transactions Yet'})

        except Profile.DoesNotExist:
            return Response({'Transactions':"Profile Does not Exist"})



# @permission_classes((IsAdminUser,))
# class TransferView(viewsets.ViewSet):
#     serializer_class = TransferSerializer
#
#     def update(self,request):
#         try:
#             profile=Profile.objects.get(pk=pk)
#             transact=(Transaction.objects.filter(sender=profile) | Transaction.objects.filter(receiver=profile)).values()
#             if len(transact) != 0:
#                 return Response({'Transactions':list(transact)})
#             else:
#                 return Response({'Transactions':'No Transactions Yet'})
#
#         except Profile.DoesNotExist:
#             return Response({'Transactions':"Profile Does not Exist"})






@permission_classes((IsAdminUser,))
class TokenIDView(viewsets.ViewSet):
    serializer_class = LoginSerializer
    def list(self,request):
        # transac=Transaction.objects.all().values()
        return Response({'message':'Append Login Token Key to the API to view Profile Details of User'})

    def retrieve(self,request,pk=None):
        try:
            TokenObj=Token.objects.get(key=pk)
            user=User.objects.get(username=TokenObj.user)
            profile=Profile.objects.get(user=user)
            url="http://127.0.0.1:8000/home/profiles/"+str(profile.pk)+"/"
            return Response({'ProfileDetail': {'id':profile.pk,'first_name':profile.first_name,
                                               'detailed_profile_url':url,'last_name':profile.last_name,
                                               'wallet_id':int(profile.pk)+5000}})

        except (Profile.DoesNotExist,Token.DoesNotExist,User.DoesNotExist):
            return Response({'ProfileDetail': "Token Does not Match any profile!"})



@permission_classes((IsAdminUser,))
class PurchasedTicketView(viewsets.ModelViewSet):
    queryset=PurchasedTicket.objects.all()
    serializer_class=PurchasedTicketSerializer
    http_method_names = ['get', 'head']


@permission_classes((IsAdminUser,))
class MerchantView(viewsets.ModelViewSet):
    queryset=Merchant.objects.all()
    serializer_class=MerchSerializer
    http_method_names = ['get', 'head']

@permission_classes((IsAdminUser,))
class MerchantItemView(viewsets.ModelViewSet):
    queryset=MerchantItem.objects.all()
    serializer_class=MerchItemSerializer
    http_method_names = ['get', 'head']

@permission_classes((IsAdminUser,))
class GroceryView(viewsets.ModelViewSet):
    queryset=Grocery.objects.all()
    serializer_class=GroceryySerializer
    http_method_names = ['get', 'head']

@permission_classes((IsAdminUser,))
class CommodityItemView(viewsets.ModelViewSet):
    queryset=CommodityItem.objects.all()
    serializer_class=CommodityItemSerializer
    http_method_names = ['get', 'head']


@permission_classes((IsAdminUser,))
class PurchasedContentView(viewsets.ModelViewSet):
    queryset=PurchasedContent.objects.all()
    serializer_class=PurchasedContentSerializer
    http_method_names = ['get', 'head']


@permission_classes((IsAdminUser,))
class RequestsView(viewsets.ModelViewSet):
    queryset=Wallet.objects.all()
    serializer_class = RequestsSerializer
    http_method_names = ['get', 'head', 'put', 'patch']

def profile_detail(request,pk):
    profile=Profile.objects.get(pk=pk)
    wallet=Wallet.objects.get(profile=profile)
    user_accnt=User.objects.get(username=profile.user)
    return render(request,'accounts/profile_detail.html',{'profile':profile,'pk':pk,'user_accnt':user_accnt,'wallet':wallet})
