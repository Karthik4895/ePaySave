from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from accounts.models import Profile,Wallet,Transaction,PurchasedTicket,MerchantTicket
from .models import Merchant,MerchantItem
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
def buy_ticks(request,pk):
    # if pk==None:
    #     return HttpResponse("Sorry!")
    #
    success=False
    profile=Profile.objects.get(pk=pk)
    wallet=Wallet.objects.get(profile=profile)
    merchants=Merchant.objects.all()
    merchantitems=MerchantItem.objects.all()
    rang=range(0,len(merchantitems))
    tot_amt=0
    t_id=0
    if request.method=="POST":
        if "var_id" in request.POST:
            print(request.POST)
            id=int(list(request.POST.getlist('var_id'))[0])
            merchantcode=str(list(request.POST.getlist('merchantcode'))[0])
            merch_code=Merchant.objects.get(merchant_code=merchantcode)
            merch_purchased=list(Merchant.objects.all())[id]
            total_amt=float(list(request.POST.getlist('total_amt'))[0])
            adult_qty=float(list(request.POST.getlist('adult_quan'))[0])
            adult_qt=int(list(request.POST.getlist('adult_quan'))[0])

            child_qty=float(list(request.POST.getlist('child_quan'))[0])
            child_qt=int(list(request.POST.getlist('child_quan'))[0])

            ticket_id=(str('TICK'+str(merch_purchased)[1:4]+str(adult_qt)+str(child_qt)+str(random.randint(1,10000))).upper())
            profpk=int(list(request.POST.getlist('profile_pk'))[0])
            prof=Profile.objects.get(pk=profpk)
            wallet=Wallet.objects.get(profile=prof)
            b = wallet.cash_balance - Decimal.from_float(total_amt)
            if b<0:
                if request.user.groups.filter(name="Privileged Members").exists():
                    h = wallet.wallet_bal - Decimal.from_float(total_amt)
                    j = wallet.total_trans_sent + Decimal.from_float(total_amt)
                    merch_wall_bal= merch_code.merchant_wallet+Decimal.from_float(total_amt)
                    Wallet.objects.select_for_update().filter(profile=profile).update(cash_balance=b)
                    Wallet.objects.select_for_update().filter(profile=profile).update(wallet_bal=h)
                    Wallet.objects.select_for_update().filter(profile=profile).update(total_trans_sent=j)
                    Merchant.objects.select_for_update().filter(merchant_code=merchantcode).update(merchant_wallet=merch_wall_bal)
                    t_id = (str('TRTP' + str(wallet.wallet_id)[-1] + profile.first_name[2:3] + profile.mobile_no[2:4] + str(random.randint(1,10000))).upper())
                    wallet = Wallet.objects.get(profile=profile)
                    c = wallet.wallet_bal
                    Transaction.objects.create(transaction_amount=total_amt, sender_id=profile.pk, receiver_id=2, wallet_balance_sent=c,
                                               message="Purchased Merchant Tickets", transaction_id=t_id)

                    success = True
                    PurchasedTicket.objects.create(user_profile=prof,merchant_purchased=merch_purchased,ticket_amount=total_amt,
                                                   adult_qty=adult_qty,child_qty=child_qty,ticket_id= ticket_id,transaction_id=t_id,message="Purchased Tickets from "+merch_code.merchant_contact_name)
                    MerchantTicket.objects.create(user_profile=prof,merchant_purchased=merch_purchased,ticket_amount=total_amt,
                                                   adult_qty=adult_qty,child_qty=child_qty,ticket_id= ticket_id,transaction_id=t_id,message="Purchased Tickets from "+merch_code.merchant_contact_name)

                    data={'pk': pk, 'success': success, 't_id': t_id,'tot_amt': total_amt}
                    return JsonResponse(data)
                else:
                    success=False
                    data={'pk': pk, 'success': success, 't_id': t_id,'tot_amt': total_amt}
                    return JsonResponse(data)

        else:
            pass
    return render(request, 'merchants/buyticks.html', {'profile': profile, 'wallet': wallet, 'pk': pk, 'rang': rang,
                                                       'merchant': merchants, 'merchantitems': merchantitems,
                                                       'success': success, 't_id': t_id,'tot_amt': tot_amt})

# @permission_classes((IsAdminUser,))
# class MerchantView(viewsets.ViewSet):
#     queryset=Merchant.objects.all()
#     serializer_class=MerchantSerializer
#
# @permission_classes((IsAdminUser,))
# class MerchantItemView(viewsets.ViewSet):
#     queryset=MerchantItem.objects.all()
#     serializer_class=MerchantItemSerializer

