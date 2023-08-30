
from shop.apps import ShopConfig
from django.urls import path

from shop.views import contacts, FlowersListView, FlowersDetailView, BlogCreateView, BlogListView, BlogDetailView, \
    BlogUpdateView, BlogDeleteView, toggle_activity

app_name = ShopConfig.name

urlpatterns = [
    # path("", home, name='flowers_list.html'),
    path("", FlowersListView.as_view(), name='flowers_list'),
    path("contacts/", contacts, name='contacts.html'),
    path("<int:pk>/detail/", FlowersDetailView.as_view(), name='flowers_detail/'),

    path("blog/create", BlogCreateView.as_view(), name='blog_create/'),
    path("blog/list/", BlogListView.as_view(), name='blog_list/'),
    path("<int:pk>/blog/detail/", BlogDetailView.as_view(), name='blog_detail/'),
    path("<int:pk>/blog/update/", BlogUpdateView.as_view(), name='blog_update/'),
    path("<int:pk>/blog/delete/", BlogDeleteView.as_view(), name='blog_delete/'),
    path("<int:pk>/blog/activiti/", toggle_activity , name='toggle_activity/'),

]
