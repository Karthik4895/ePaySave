from django.urls import path, include

from . import views

app_name='groceries'

urlpatterns = [
    path('profiles/<int:pk>/grocery_list/', views.grocery_list, name='grocery_list'),
    path('profiles/<int:pk>/grocery_page/<int:comm>/', views.grocery_page, name='grocery_page'),
]