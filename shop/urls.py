
from shop.apps import ShopConfig
from django.urls import path

from shop.views import home, contacts, detail_info

app_name = ShopConfig.name

urlpatterns = [
    path("", home, name='home.html'),
    path("contacts/", contacts, name='contacts.html'),
    path("<int:pk>/bouquet/", detail_info, name='detail_info/' )

]
