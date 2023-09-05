from django.urls import path
from django.views.decorators.cache import cache_page

from shop.apps import ShopConfig
from shop.views import contacts, FlowersListView, FlowersDetailView, BlogCreateView, BlogListView, BlogDetailView, \
    BlogUpdateView, BlogDeleteView, toggle_activity, FlowersCreateView, FlowersUpdateView, FlowersDeleteView, \
    toggle_activity_fl, CategoryListView

app_name = ShopConfig.name

urlpatterns = [
    # path("", home, name='flowers_list.html'),
    path("", FlowersListView.as_view(), name='flowers_list/'),
    path("flowers/create", FlowersCreateView.as_view(), name='flowers_create/'),
    path("flowers/<int:pk>/detail/", FlowersDetailView.as_view(), name='flowers_detail/'),
    path("flowers/<int:pk>/update/", FlowersUpdateView.as_view(), name='flowers_update/'),
    path("flowers/<int:pk>/delete/", cache_page(60) (FlowersDeleteView.as_view()), name='flowers_delete/'),
    path("flowers/<int:pk>/activiti_fl/", toggle_activity_fl, name='toggle_activity_fl/'),

    path("flowers/category,", CategoryListView.as_view(), name='flowers_category/'),

    path("blog/create", BlogCreateView.as_view(), name='blog_create/'),
    path("blog/list/", BlogListView.as_view(), name='blog_list/'),
    path("blog/<int:pk>/detail/", BlogDetailView.as_view(), name='blog_detail/'),
    path("blog/<int:pk>/update/", BlogUpdateView.as_view(), name='blog_update/'),
    path("blog/<int:pk>/delete/", BlogDeleteView.as_view(), name='blog_delete/'),
    path("blog/<int:pk>/activiti/", toggle_activity, name='toggle_activity/'),



    path("contacts/", contacts, name='contacts.html'),

]
