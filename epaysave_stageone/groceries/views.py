from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from accounts.models import Profile,Wallet,Transaction,PurchasedTicket, PurchasedContent, PurchasedCommodity, PurchasedGrocery
from merchants.models import Merchant,MerchantItem
from .models import Grocery,Commodity,CommodityItem
from decimal import Decimal
# from accounts.models import TicketModel
from rest_framework.authtoken.models import Token
from rest_framework import viewsets
from accounts.serializers import ProfileSerializer,ProfilesSerializer,WalletSerializer,TransactionSerializer,UserSerializer, RequestsSerializer, LoginSerializer
import random
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden,JsonResponse
from django.contrib.auth.decorators import login_required,user_passes_test
from rest_framework.permissions import IsAuthenticated,IsAdminUser

from rest_framework.decorators import api_view, permission_classes

from django.http import HttpResponseRedirect
from rest_framework.views import APIView
from django.db import connection
from rest_framework.response import Response


@login_required
def grocery_page(request,pk,comm):
    rang_comm=[]
    rang_commitems=[]
    success=False
    profile=Profile.objects.get(pk=pk)
    wallet=Wallet.objects.get(profile=profile)
    groceries=Grocery.objects.all()
    gro_id=0
    rang_groc=range(0,len(groceries))
    grocode=0
    for grocery in groceries:
        # rang_comm[gro_id]=range(0,len(grocery.commodity_set.count()))
        if gro_id+1==comm:
            grocode=grocery.grocery_code
        gro_id+=1
    commodities=Commodity.objects.all()
    comm=0
    commod=[]
    i=0
    for commodity in commodities:
        if commodity.grocery_code==grocode:
            commod[i]=commodity
            i+=1
        comm+=1
    range_comm=range(0,len(commod))
    commodityitems=CommodityItem.objects.all()
    # for i in range_comm:
    #     for commitems in commodityitems:
    #         if commitems.commodity_code==comm[i].commodity_code:
    #             commitem[j]=commitem

    print(rang_commitems)
    print(rang_comm)
    print(rang_groc)
    return render(request, 'groceries/grocery_page.html', {'profile': profile, 'wallet': wallet, 'pk': pk,
                                                           'groceries': groceries, 'commodities': commodities,
                                                           'commodityitems':commodityitems,'range_comm':rang_comm,
                                                           'rang_commitems':rang_commitems,'rang_groc':rang_groc,
                                                           'success': success})

@login_required
def grocery_list(request,pk):
    success=False
    profile=Profile.objects.get(pk=pk)
    wallet=Wallet.objects.get(profile=profile)
    groceries=Grocery.objects.all()
    rang_groc=range(0,len(groceries))
    commodityitems=CommodityItem.objects.all()
    if request.method=="POST":
        print(request.POST)
        if "grandtotcheckin" in request.POST:
            print(request.POST.getlist)

            hunqtys = list((request.POST.getlist('grocqtyhun')[0]).split(','))
            hunqty = [int(i) for i in hunqtys]

            twohunqtys = list((request.POST.getlist('grocqtytwohun')[0]).split(','))
            twohunqty = [int(i) for i in twohunqtys]

            fivehunqtys = list((request.POST.getlist('grocqtyfivehun')[0]).split(','))
            fivehunqty = [int(i) for i in fivehunqtys]

            onekgqtys = list((request.POST.getlist('grocqtyonekg')[0]).split(','))
            onekgqty = [int(i) for i in onekgqtys]


            fivekgqtys = list((request.POST.getlist('grocqtyfivekg')[0]).split(','))
            fivekgqty = [int(i) for i in fivekgqtys]

            twentyfivekgqtys = list((request.POST.getlist('grocqtytwentyfivekg')[0]).split(','))
            twentyfivekgqty = [int(i) for i in twentyfivekgqtys]

            fiftykgqtys = list((request.POST.getlist('grocqtyfiftykg')[0]).split(','))
            fiftykgqty = [int(i) for i in fiftykgqtys]

            hunpris = list((request.POST.getlist('hunpricearr')[0]).split(','))
            hunpri = [round(Decimal(i),2) for i in hunpris]

            twohunpris = list((request.POST.getlist('twohunpricearr')[0]).split(','))
            twohunpri = [round(Decimal(i),2) for i in twohunpris]

            fivehunpris = list((request.POST.getlist('fivehunpricearr')[0]).split(','))
            fivehunpri = [round(Decimal(i),2) for i in fivehunpris]

            onekgpris = list((request.POST.getlist('onekgpricearr')[0]).split(','))
            onekgpri = [round(Decimal(i),2) for i in onekgpris]

            fivekgpris = list((request.POST.getlist('fivekgpricearr')[0]).split(','))
            fivekgpri = [round(Decimal(i),2) for i in fivekgpris]

            twentyfivekgpris = list((request.POST.getlist('twentyfivekgpricearr')[0]).split(','))
            twentyfivekgpri = [round(Decimal(i)) for i in twentyfivekgpris]

            fiftykgpris = list((request.POST.getlist('fiftykgpricearr')[0]).split(','))
            fiftykgpri = [round(Decimal(i)) for i in fiftykgpris]

            commoditycodes = list((request.POST.getlist('commodity_codess')[0].split(',')))
            commoditynames = list((request.POST.getlist('commodity_descs')[0].split(',')))
            grocerynames = list((request.POST.getlist('grocery_descs')[0].split(',')))
            purchased_commodity = []
            t_id=''
            total_amt=str(list(request.POST.getlist('grandtotcheckin'))[0])
            print(total_amt)
            # tick_id=(str('TIGR'+str(profile.first_name)[1:4]+str(total_amt)[:1]+str(profile.last_name)+str(wallet.wallet_bal)[2:3]+str(random.randint(1,10000))).upper())
            profpk=int(list(request.POST.getlist('profpk1'))[0])
            total_amt=total_amt[0:-5]
            print(total_amt)
            total_amt=float(total_amt)
            prof=Profile.objects.get(pk=profpk)
            wallet=Wallet.objects.get(profile=prof)
            b = wallet.cash_balance - Decimal.from_float(total_amt)
            if b<0:
                if request.user.groups.filter(name="Privileged Members").exists():
                    h = wallet.wallet_bal - Decimal.from_float(total_amt)
                    j = wallet.total_trans_sent + Decimal.from_float(total_amt)
                    Wallet.objects.select_for_update().filter(profile=profile).update(cash_balance=b)
                    Wallet.objects.select_for_update().filter(profile=profile).update(wallet_bal=h)
                    Wallet.objects.select_for_update().filter(profile=profile).update(total_trans_sent=j)
                    t_id = (str('TRGR' + str(wallet.wallet_id)[-1] + profile.first_name[2:3] + profile.mobile_no[2:4] + str(random.randint(1,10000))).upper())
                    wallet=Wallet.objects.get(profile=profile)
                    c = wallet.wallet_bal
                    Transaction.objects.create(transaction_amount=total_amt, sender_id=profile.pk, receiver_id=2, wallet_balance_sent=c,
                                               message="Purchased Grocery Items", transaction_id=t_id)
                    success = True
                    for i in range(0,len(commoditynames)):
                        if hunqty[i] or twohunqty[i] or fivehunqty[i] or onekgqty[i] or fivekgqty[i] or twentyfivekgqty[i] or fiftykgqty[i]:
                            purchased_commodity=[grocerynames[i],commoditynames[i],commoditycodes[i],hunqty[i],twohunqty[i],fivehunqty[i],onekgqty[i],fivekgqty[i],
                                                 twentyfivekgqty[i],fiftykgqty[i],hunpri[i],twohunpri[i],fivehunpri[i],onekgpri[i],fivekgpri[i],
                                                 twentyfivekgpri[i],fiftykgpri[i]]
                            total_qty=hunqty[i]+twohunqty[i]+fivehunqty[i]+onekgqty[i]+fivekgqty[i]+twentyfivekgqty[i]+fiftykgqty[i]
                            print(purchased_commodity)
                            tick_id=(str('TIGR'+str(profile.first_name)[1:4]+str(profile.last_name)[2:3]+str(grocerynames[i])[2:3]+str(commoditynames[i])[1:2]+str(random.randint(1,10000))).upper())
                            purchased_grocery = PurchasedGrocery.objects.create(profile=profile,grocery=Grocery.objects.get(grocery_code=purchased_commodity[0]),ticket_id=tick_id,transaction_id=t_id)
                            purchased_commodit = PurchasedCommodity.objects.create(purchased_groc=purchased_grocery,commodityitemcode=purchased_commodity[2],commodityitemname=purchased_commodity[1])
                            total_comm = round(Decimal(purchased_commodity[3]*purchased_commodity[10]),2) + round(Decimal(purchased_commodity[4]*purchased_commodity[11]),2) + round(Decimal(purchased_commodity[5]*purchased_commodity[12]),2) + round(Decimal(purchased_commodity[6] * purchased_commodity[13]),2) + round(Decimal(purchased_commodity[7]*purchased_commodity[14]),2) + round(Decimal(purchased_commodity[8]*purchased_commodity[15]),2) + round(Decimal(purchased_commodity[9]*purchased_commodity[16]),2)
                            grocery_wall = Grocery.objects.get(grocery_code=purchased_grocery.grocery).grocery_wallet
                            tot = grocery_wall + total_comm
                            Grocery.objects.select_for_update().filter(grocery_code=purchased_grocery.grocery).update(grocery_wallet=tot)

                            purchased_content = PurchasedContent.objects.create(purchased_item=purchased_commodit,hundredgramqty=purchased_commodity[3],hundredgramtotprice=round(Decimal(purchased_commodity[3]*purchased_commodity[10]),2),
                                                                                twohundredgramqty=purchased_commodity[4],twohundredgramtotprice=round(Decimal(purchased_commodity[4]*purchased_commodity[11]),2),
                                                                                fivehundredgramqty=purchased_commodity[5],fivehundredgramtotprice=round(Decimal(purchased_commodity[5]*purchased_commodity[12]),2),
                                                                                onekgqty=purchased_commodity[6],onekgtotprice=round(Decimal(purchased_commodity[6]*purchased_commodity[13]),2),
                                                                                fivekgqty=purchased_commodity[7],fivekgtotprice=round(Decimal(purchased_commodity[7]*purchased_commodity[14]),2),
                                                                                twentyfivekgqty=purchased_commodity[8],twentyfivekgtotprice=round(Decimal(purchased_commodity[8]*purchased_commodity[15]),2),
                                                                                fiftykgqty=purchased_commodity[9],fiftykgtotprice=round(Decimal(purchased_commodity[9]*purchased_commodity[16]),2),
                                                                                totalcommamt=round(Decimal(total_comm),2),total_packets=total_qty)
                            purchased_content.save()
                    data = {'pk': pk, 'success': success, 't_id': t_id, 'tot_amt': total_amt}
                    return JsonResponse(data)
                else:
                    success=False
                    data = {'pk': pk, 'success': success, 't_id': t_id, 'tot_amt': total_amt}
                    return JsonResponse(data)
        else:
            pass
    return render(request,'groceries/grocery_list.html', {'profile': profile, 'wallet': wallet, 'pk': pk,
                                                           'groceries': groceries,'rang_groc':rang_groc,
                                                           'success': success,'commodityitems':commodityitems})
