from django import template
from accounts import models

def display_count():
    obj_count = models.Wallet.objects.filter(wallet_cash_req__gte=0).count() + models.Wallet.objects.filter(wallet_loan_req__gte=0).count() + models.Wallet.objects.filter(wallet_savings_req__gte=0).count()
    return { 'obj_count':obj_count }

template.Library().tag(display_count())
