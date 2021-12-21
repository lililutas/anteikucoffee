"""
Definition of urls for DjangoWebProject1.
"""

from datetime import datetime
from django.urls import path, re_path
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView

from app import forms, views

from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings

urlpatterns = [
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('login/',
         LoginView.as_view
         (
             template_name='app/login.html',
             authentication_form=forms.BootstrapAuthenticationForm,
             extra_context=
             {
                 'title': 'Вход',
                 'year' : datetime.now().year,
             }
         ),
         name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('admin/', admin.site.urls),
    path('pool/', views.pool, name='pool'),
    path('registration', views.registration, name='registration'),
    path('blog/', views.blog, name='blog'),
    
    path('newpost/', views.newpost, name='newpost'),
    path('cart/', views.cart, name='cart'),
    path('shop/', views.shop, name='shop'),
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('delete_item/<int:item>/', views.delete_item, name='delete_item'),
    path('quantity_minus/', views.quantity_minus, name='quantity_minus'),
    path('quantity_plus/', views.quantity_plus, name='quantity_plus'),
    path('total_price/', views.total_price, name='total_price'),
    path('deal_order/', views.deal_order, name='deal_order'),
    path('delete_post/<int:parameter>/', views.delete_post, name='delete_post'),
    path('change_post/<int:parameter>/', views.change_post, name='change_post'),
    path('delete_order/<int:item>/', views.delete_order, name='delete_order'),
    path('delete_item_order/<int:item>/', views.delete_item_order, name='delete_item_order'),
    path('quantity_minus_order/', views.quantity_minus_order, name='quantity_minus_order'),
    path('quantity_plus_order/', views.quantity_plus_order, name='quantity_plus_order'),
    path('total_price_order/<int:order>/', views.total_price_order, name='total_price_order'),
    path('myOrders/', views.myOrders, name='myOrders'),
    path('AllOrders/', views.AllOrders, name='AllOrders'),
    path('orderDetails/<int:order>/', views.orderDetails, name='orderDetails'),
    
    path('shop/<str:parameter>/', views.shop, name='shop'),            
    re_path(r'^(?P<parameter>\d+)/$', views.blogpost, name='blogpost'),


    path('blogControls/', views.blogControls, name='blogControls'),
    path('shopControls/', views.shopControls, name='shopControls'),
    path('userControls/', views.userControls, name='userControls'),
    path('newproduct/', views.newproduct, name='newproduct'),
    path('delete_product/<int:parameter>/', views.delete_product, name='delete_product'),
    path('change_product/<int:parameter>/', views.change_product, name='change_product'),

    path('newuser/', views.newuser, name='newuser'),
    path('delete_user/<int:parameter>/', views.delete_user, name='delete_user'),
    path('change_user/<int:parameter>/', views.change_user, name='change_user'),
    path('changeStatus/', views.changeStatus, name='changeStatus'),
  
]


urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()