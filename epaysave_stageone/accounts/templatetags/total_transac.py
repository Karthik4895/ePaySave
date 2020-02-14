from accounts.models import Transaction, Wallet, Profile
from django import template
from django.db.models import Sum

register=template.Library()

@register.simple_tag(name='transac')
def transac():
    # obj_count = Wallet.objects.aggregate(Sum('wallet_id'))['wallet_id__sum']
    # print(str(obj_count))
    obj_count = Transaction.objects.all().count()
    if obj_count:
        return "%s" % obj_count
    else:
        return 'nil'


@register.simple_tag(name='wallet_tot')
def wallet_tot():
    # obj_count = Wallet.objects.aggregate(Sum('wallet_id'))['wallet_id__sum']
    # print(str(obj_count))
    total=0
    prof_count=Profile.objects.all()
    for prof in prof_count:
        try:
            # prof_i=Profile.objects.get(pk=i)
            wall= Wallet.objects.get(profile=prof)
            total= total+wall.wallet_bal
    # obj_count = Wallet.objects.aggregate(Sum('wallet_bal'))
        except:
            continue
    if total:
        return "%s" % total
    else:
        return '0'

@register.simple_tag(name='cash_tot')
def cash_tot():
    # obj_count = Wallet.objects.aggregate(Sum('wallet_id'))['wallet_id__sum']
    # print(str(obj_count))
    total=0
    prof_count=Profile.objects.all()
    for prof in prof_count:
        try:
            # prof_i=Profile.objects.get(pk=i)
            wall= Wallet.objects.get(profile=prof)
            total= total+wall.cash_balance
    # obj_count = Wallet.objects.aggregate(Sum('wallet_bal'))
        except:
            continue
    if total:
        return "%s" % total
    else:
        return '0'

@register.simple_tag(name='savings_tot')
def savings_tot():
    # obj_count = Wallet.objects.aggregate(Sum('wallet_id'))['wallet_id__sum']
    # print(str(obj_count))
    total=0
    prof_count=Profile.objects.all()
    for prof in prof_count:
        try:
            # prof_i=Profile.objects.get(pk=i)
            wall= Wallet.objects.get(profile=prof)
            total= total+wall.savings
    # obj_count = Wallet.objects.aggregate(Sum('wallet_bal'))
        except:
            continue
    if total:
        return "%s" % total
    else:
        return '0'