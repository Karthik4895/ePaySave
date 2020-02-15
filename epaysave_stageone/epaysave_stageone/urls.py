"""epaysave_stageone URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from rest_framework import routers
import accounts.views as views
import merchants.views as Views
import groceries.views as View
from django.conf import settings
from django.conf.urls.static import static
from django.views.decorators.csrf import csrf_exempt
router=routers.DefaultRouter()

router.register('profiles',views.ProfileView)
router.register('requests',views.RequestsView)
router.register('transactions',views.TransactionView)
router.register('login', views.LoginView)
router.register('wallets',views.WalletView)
router.register('purchasedtickets',views.PurchasedTicketView)
router.register('grocerycontents',views.PurchasedContentView)
router.register('merchants',views.MerchantView)
router.register('merchantitems',views.MerchantItemView)
router.register('groceries',views.GroceryView)
router.register('commodityitems',views.CommodityItemView)
router.register('transview',views.TransactionsView,basename='Transactions_view')
router.register('tokenidview',views.TokenIDView,basename='Token_view')
router.register('barcodetransfer',views.BarCodeView)
router.register('apptransfer',views.AppTransferView)



admin.autodiscover()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/',include(router.urls)),
    path('', views.index, name='index'),
    path('accounts/',include('accounts.urls'),name='accounts'),
    path('merchants/',include('merchants.urls'),name='merchants'),
    path('groceries/', include('groceries.urls'), name='groceries'),
    path('home/rest-auth/', include('rest_auth.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

