from django.urls import path, include
from . import views

app_name='accounts'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    # path('', views.index, name='index'),
    path('<int:pk>/',views.index_with_pk, name='index_with_pk'),
    path('profile/<int:pk>/',views.profile_detail,name='profile_detail'),
    path('profile/<int:pk>/edit/',views.profile_edit,name='profile_edit'),
    path('profile/<int:pk>/wallet/',views.wallet_view,name='wallet_view'),
    path('profile/<int:pk>/wallet/transac',views.history_transac,name='history_transac'),
    path('news/all/', views.news_all, name='news_all'),
    path('profile/<int:pk>/maps/',views.map_view,name='map_view'),
    path('newsdesc/',views.news_desc,name='newsdesc'),
]
