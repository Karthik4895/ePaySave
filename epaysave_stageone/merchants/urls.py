from django.urls import path, include

from . import views

app_name='merchants'

urlpatterns = [
    path('profiles/<int:pk>/buytickets/', views.buy_ticks, name='buyticks'),
]