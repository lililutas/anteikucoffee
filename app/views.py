"""
Definition of views.
"""

from datetime import datetime
from django.shortcuts import render, redirect
from django.http import HttpRequest
from .forms import MyRequestForm
from django.contrib.auth.forms import UserCreationForm
from django.core.paginator import Paginator
from django.urls import reverse
from django.db import models
from .models import Blog
from .models import Comment
from .models import Shop
from .models import Orders
from .models import SubOrders
from .forms import CommentForm
from .forms import BlogForm


def home(request):
    """Renders the home page."""
    posts = Blog.objects.all().reverse()[:6]
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Главная страница',
            'posts' : posts,
            'year':datetime.now().year,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Контакты',
            'message':'Свяжитесь с нами',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'О нас',
            'message':'Здесь вы найдете!',
            'year':datetime.now().year,
        }
    )

def pool(request):
    """Renders the request page."""
    assert isinstance(request, HttpRequest)
    data = None

    if request.method == 'POST':
        form = MyRequestForm(request.POST)
        if form.is_valid():
            data = dict()
            data['theme'] = form.cleaned_data['requestTheme']
            data['text'] = form.cleaned_data['requestText']
            data['choice'] = form.cleaned_data['requestChoice']
            data['radio'] = form.cleaned_data['requestRadio']
            data['email'] = form.cleaned_data['requestMail']
            form = None
    else:
        form = MyRequestForm()

    return render(
        request,
        'app/pool.html',
        {
            'form' : form,
            'data' : data,
            'title':'Обратная связь',
            'message' : 'Оставьте сообщение об ошибке.',
            'year':datetime.now().year,
        }
    )

def registration(request):
        if request.method == "POST":
            regform = UserCreationForm(request.POST)
            if regform.is_valid():
                reg_f = regform.save(commit=False)
                reg_f.is_staff = False
                reg_f.is_active = True
                reg_f.is_superuser = False
                reg_f.date_joined = datetime.now()
                reg_f.last_login = datetime.now()
                regform.save()
                return redirect('home')
        else:
           regform =  UserCreationForm()
           
        assert isinstance(request, HttpRequest)
        return render(
            request,
            'app/registration.html',
            {
                'title': 'Регистрация',
                'regform' : regform,
                'year':datetime.now().year,
                }
            )
def blog(request):
    """Renders the blog page."""
    posts = Blog.objects.all()
   
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/blog.html',
        {
            'title':'Блог',
            'posts': posts,
            'year':datetime.now().year,
        }
    )
def blogpost(request, parameter):
    """Renders the blog page."""
    post = Blog.objects.get(id=parameter)
    comments = Comment.objects.filter(post=parameter)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment_f = form.save(commit=False)
            comment_f.author = request.user
            comment_f.date = datetime.now()
            comment_f.post = Blog.objects.get(id=parameter)
            comment_f.save()
            return redirect('blogpost', parameter=post.id)
                
    else:
        form = CommentForm()
        


    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/blogpost.html',
        {
            'title': post.title,
            'post': post,
            'comments': comments,
            'form': form,
            'year':datetime.now().year,
        }
    )
def newpost(request):

    if request.method == 'POST':
        blogform = BlogForm(request.POST, request.FILES)
        if blogform.is_valid():
            blog_f = blogform.save(commit=False)
            blog_f.author = request.user
            blog_f.posted = datetime.now()
            blog_f.save()
            return redirect('blog')
                
    else:
        blogform = BlogForm()
        


    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/newpost.html',
        {
            'title': 'Новый пост',
            'blogform': blogform,
            'year':datetime.now().year,
        }
    )
def shop(request, parameter = 'all'):
    """Renders the shop page."""
    search = request.GET.get('search')
    if parameter == 'all': 
        if search == None:
            products = Shop.objects.all()
        else:
            products = Shop.objects.filter(name__contains=search)
    else:
        if search == None:
            products = Shop.objects.filter(category=parameter)
        else:
            products = Shop.objects.filter(category=parameter, name__contains=search)
    
    if search == None:
        paginator = Paginator(products, 6)
    else:
        paginator = Paginator(products, 100)
    page = request.GET.get('page')
    products = paginator.get_page(page)
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/shop.html',
        {
            'title':'Магазин',
            'products': products,
            'year':datetime.now().year,
        }
    )       


def total_price(request):
    current_order, status = Orders.objects.get_or_create(holder=request.user, status='incart')
    order_list = SubOrders.objects.filter(order=current_order)
    current_order.total_price = 0
    for item in order_list:
        current_order.total_price += item.price

    current_order.save()
    return redirect(reverse('cart'))

def add_to_cart(request):

    current_product = Shop.objects.filter(id = request.GET.get('product')).first()
    current_order, status = Orders.objects.get_or_create(holder=request.user, status='incart')
    if status:
        current_order.save()
    suborder, status = SubOrders.objects.get_or_create(order=current_order, product=current_product)
    if status: 
        suborder.price = suborder.product.price * suborder.quantity
        suborder.save()
    else:
        suborder.quantity += 1
        suborder.price = suborder.product.price * suborder.quantity
        suborder.save()
    order_list = SubOrders.objects.filter(order=current_order)
    current_order.total_price = 0
    for item in order_list:
        current_order.total_price += item.price

    current_order.save()
    assert isinstance(request, HttpRequest)
    return redirect(reverse('shop'))

def cart(request):
    """Renders the cart page."""
    current_order = Orders.objects.filter(holder=request.user, status='incart').first()
    if current_order == None:
        items = None
    else:
        items = SubOrders.objects.filter(order=current_order)
        
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/cart.html',
        {
            'title':'Корзина',
            'order': current_order,
            'items': items,  
            'year':datetime.now().year,
        }
    ) 

def delete_item(request, item):
    current_item = SubOrders.objects.get(id = item).delete()
    return redirect(reverse('total_price'))

def quantity_minus(request):
    current_item = SubOrders.objects.filter(id = request.GET.get('item')).first()
 
    current_item.quantity -= 1
    if current_item.quantity == 0:
        return redirect(reverse('delete_item', kwargs={'item': current_item.id}))
    else:

        current_item.price = current_item.product.price * current_item.quantity
        current_item.save()
    
        return redirect(reverse('total_price'))

def quantity_plus(request):
    current_item = SubOrders.objects.filter(id = request.GET.get('item')).first()
 
    current_item.quantity += 1
    current_item.price = current_item.product.price * current_item.quantity
    current_item.save()
    
    return redirect(reverse('total_price'))

def deal_order(request):
    current_order = Orders.objects.filter(holder=request.user, status='incart').first()
    current_order.status = 'intransit'
    current_order.save()
    
    return redirect(reverse('shop'))