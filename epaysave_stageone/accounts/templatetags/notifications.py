from accounts.models import Wallet,Profile
from django.contrib.auth.models import User
from django import template

register=template.Library()

@register.simple_tag(name='notification')
def notification():
    obj_count = Wallet.objects.filter(wallet_cash_req__gt=0).count() + Wallet.objects.filter(wallet_loan_req__gt=0).count() + Wallet.objects.filter(wallet_savings_req__gt=0).count() + Wallet.objects.filter(wallet_crowd_req__gt=0).count()
    if obj_count:
        return "%s" % (obj_count)
    else:
        return 'nil'


@register.simple_tag(name='total_users')
def total_users():
    user_count = User.objects.all().count()
    return "%s" % (user_count)


@register.simple_tag(name='wallet_counts')
def wallet_counts():
    wallet_count = Wallet.objects.filter(wallet_bal__gt=1000).count()
    return "%s" % (wallet_count)
