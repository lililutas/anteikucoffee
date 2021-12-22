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


    #Главная страница
    path('', views.home, name='home'),

    #Контакты
    path('contact/', views.contact, name='contact'),
    #Форма обратной связи
    path('pool/', views.pool, name='pool'),

    #О нас
    path('about/', views.about, name='about'),

    #Авторизация
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
    path('registration', views.registration, name='registration'),

    #Раздел администратора
    path('admin/', admin.site.urls),

    #Новости
    path('blog/', views.blog, name='blog'),
    #Страница поста 
    re_path(r'^(?P<parameter>\d+)/$', views.blogpost, name='blogpost'),
    #Управление новостями
    path('blogControls/', views.blogControls, name='blogControls'),
    #Новости API
    path('newpost/', views.newpost, name='newpost'),
    path('delete_post/<int:parameter>/', views.delete_post, name='delete_post'),
    path('change_post/<int:parameter>/', views.change_post, name='change_post'),

    #Магазин
    path('shop/', views.shop, name='shop'),
    path('shop/<str:parameter>/', views.shop, name='shop'),   
    #Управление товарами
    path('shopControls/', views.shopControls, name='shopControls'),
    #Магазин API
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('delete_product/<int:parameter>/', views.delete_product, name='delete_product'),
    path('change_product/<int:parameter>/', views.change_product, name='change_product'),
    path('newproduct/', views.newproduct, name='newproduct'),

    #Корзина
    path('cart/', views.cart, name='cart'),
    #Корзина API
    path('delete_item/<int:item>/', views.delete_item, name='delete_item'),
    path('quantity_minus/', views.quantity_minus, name='quantity_minus'),
    path('quantity_plus/', views.quantity_plus, name='quantity_plus'),
    path('total_price/', views.total_price, name='total_price'),
    path('deal_order/', views.deal_order, name='deal_order'),

    #Заказы
    path('AllOrders/', views.AllOrders, name='AllOrders'),
    #Мои заказы
    path('myOrders/', views.myOrders, name='myOrders'),
    #Детали заказа
    path('orderDetails/<int:order>/', views.orderDetails, name='orderDetails'),
    #Заказы API
    path('delete_order/<int:item>/', views.delete_order, name='delete_order'),
    path('delete_item_order/<int:item>/', views.delete_item_order, name='delete_item_order'),
    path('quantity_minus_order/', views.quantity_minus_order, name='quantity_minus_order'),
    path('quantity_plus_order/', views.quantity_plus_order, name='quantity_plus_order'),
    path('total_price_order/<int:order>/', views.total_price_order, name='total_price_order'),
    path('changeStatus/', views.changeStatus, name='changeStatus'),    
    
    #Управление пользователями
    path('userControls/', views.userControls, name='userControls'),
    #Управление пользователями API
    path('newuser/', views.newuser, name='newuser'),
    path('delete_user/<int:parameter>/', views.delete_user, name='delete_user'),
    path('change_user/<int:parameter>/', views.change_user, name='change_user'),

  
]


urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()