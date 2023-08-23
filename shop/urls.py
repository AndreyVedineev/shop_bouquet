
from shop.apps import ShopConfig
from django.urls import path

from shop.views import home, contacts

app_name = ShopConfig.name

urlpatterns = [
    path('', home, name='home.html'),
    path('contacts/', contacts, name='contacts.html')

]
