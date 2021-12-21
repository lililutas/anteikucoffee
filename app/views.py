"""
Definition of views.
"""

from datetime import datetime
from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.http import JsonResponse
from .forms import MyRequestForm
from django.contrib.auth.forms import UserCreationForm
from django.core.paginator import Paginator
from django.urls import reverse
from django.db import models
from django.contrib.auth.models import User
from .models import Blog
from .models import Comment
from .models import Shop
from .models import Orders
from .models import Roles
from .models import SubOrders
from .forms import CommentForm
from .forms import BlogForm
from .forms import ProductForm
from .forms import AddUserForm


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
            return redirect('blogControl')
                
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

    if request.is_ajax and request.method == "GET":
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
        return JsonResponse({'isAdded': True}, status = 200)

    return JsonResponse({}, status = 400)

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

def myOrders(request):
    """Renders the cart page."""
    current_orders = Orders.objects.filter(holder=request.user).exclude(status='incart')
        
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/myOrders.html',
        {
            'title':'Мои заказы',
            'items': current_orders, 
            'year':datetime.now().year,
        }
    ) 

def orderDetails(request, order):
    """Renders the order page."""
    current_order = Orders.objects.get(id = order)
    items = SubOrders.objects.filter(order=current_order)
        
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/orderDetails.html',
        {
            'title':'Заказ',
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

def delete_order(request, item):
    current_order = Orders.objects.get(id = item).delete()
    return redirect(reverse('myOrders'))





def total_price_order(request, order):
    order_list = SubOrders.objects.filter(order=order)
    current_order = Orders.objects.get(id=order)
    current_order.total_price = 0
    for item in order_list:
        current_order.total_price += item.price

    current_order.save()
    return redirect(reverse('orderDetails', kwargs={'order': order}))


def delete_item_order(request, item):
    current_item = SubOrders.objects.get(id = item).delete()
    current_order = request.GET.get('order')
    return redirect(reverse('total_price_order', kwargs={'order': current_order}))

def quantity_minus_order(request):
    current_item = SubOrders.objects.filter(id = request.GET.get('item')).first()
    current_order = request.GET.get('order')
    current_item.quantity -= 1
    current_item.price = current_item.product.price * current_item.quantity
    current_item.save()
    
    return redirect(reverse('total_price_order', kwargs={'order': current_order}))

def quantity_plus_order(request):
    current_item = SubOrders.objects.filter(id = request.GET.get('item')).first()
    current_order = request.GET.get('order')
    current_item.quantity += 1
    current_item.price = current_item.product.price * current_item.quantity
    current_item.save()
    
    return redirect(reverse('total_price_order', kwargs={'order': current_order}))
def blogControls(request):
    """Renders the blog page."""
    posts = Blog.objects.all()
   
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/blogControls.html',
        {
            'title':'Управление блогом',
            'posts': posts,
            'year':datetime.now().year,
        }
    )


def delete_post(request, parameter):
    current_item = Blog.objects.get(id = parameter).delete()
    return redirect(reverse('blogControls'))

def change_post(request, parameter):

    current_post = Blog.objects.get(id = parameter)
    if request.method == 'POST':
        blogform = BlogForm(request.POST, request.FILES)
        if blogform.is_valid():
            
            
            current_post.title = blogform.cleaned_data['title']
            current_post.description = blogform.cleaned_data['description']
            current_post.content = blogform.cleaned_data['content']
            current_post.posted = datetime.now()
            current_post.save()


            return redirect(reverse('blogControls'))
                
    else:
        blogform = BlogForm()


    return render(
        request,
        'app/changePost.html',
        {
            'title': 'Изменить пост',
            'post': current_post,
            'blogform': blogform,
            'year':datetime.now().year,
        }
    )
        
def AllOrders(request):
    """Renders the cart page."""
    current_orders = Orders.objects.all().exclude(status='incart')
        
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/orders.html',
        {
            'title':'Заказы',
            'items': current_orders, 
            'year':datetime.now().year,
        }
    ) 



def changeStatus(request):
    current_order = Orders.objects.get(id = request.GET.get('order'))
    current_order.status = request.GET.get('status')
    current_order.save()
    return redirect(reverse('AllOrders'))
    


def shopControls(request):
    """Renders the blog page."""
    products = Shop.objects.all()
   
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/shopControls.html',
        {
            'title':'Управление товарами',
            'products': products,
            'year':datetime.now().year,
        }
    )


def newproduct(request):

    if request.method == 'POST':
        productform = ProductForm(request.POST, request.FILES)
        if productform.is_valid():
            product_f = productform.save(commit=False)
            product_f.save()
            return redirect(reverse('shopControls'))
                
    else:
        productform = ProductForm()
        


    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/newproduct.html',
        {
            'title': 'Новый товар',
            'productform': productform,
            'year':datetime.now().year,
        }
    )
def delete_product(request, parameter):
    current_item = Shop.objects.get(id = parameter).delete()
    return redirect(reverse('shopControls'))

def change_product(request, parameter):

    current_product = Shop.objects.get(id = parameter)
    if request.method == 'POST':
        productform = ProductForm(request.POST, request.FILES)
        if productform.is_valid():
            
            
            current_product.name = productform.cleaned_data['name']
            current_product.short = productform.cleaned_data['short']
            current_product.text = productform.cleaned_data['text']
            current_product.price =  productform.cleaned_data['price']
            current_product.category =  productform.cleaned_data['category']
            current_product.save()


            return redirect(reverse('shopControls'))
                
    else:
        productform = ProductForm()


    return render(
        request,
        'app/changeProduct.html',
        {
            'title': 'Изменить товар',
            'product': current_product,
            'productform': productform,
            'year':datetime.now().year,
        }
    )

def userControls(request):
    """Renders the blog page."""
    users = User.objects.all()
    roles = Roles.objects.all()
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/userControls.html',
        {
            'title':'Управление пользователями',
            'roles': roles,
            'users': users,
            'year':datetime.now().year,
        }
    )

def delete_user(request, parameter):
    User.objects.get(id = parameter).delete()
    return redirect(reverse('userControls'))

def change_user(request, parameter):

    current_user = User.objects.get(id = parameter)
    current_role, status = Roles.objects.get_or_create(user = current_user)
    if request.method == 'POST':
        userform = AddUserForm(request.POST, request.FILES)
        if userform.is_valid():
            
            
            current_user.username = userform.cleaned_data['username']
            current_user.password = userform.cleaned_data['password']
            current_user.mail = userform.cleaned_data['mail']
            current_user.role =  userform.cleaned_data['role']
            current_user.save()


            return redirect(reverse('userControls'))
                
    else:
        userform = AddUserForm()


    return render(
        request,
        'app/changeUser.html',
        {
            'title': 'Изменить пользователя',
            'user': current_user,
            'userform': userform,
            'role': current_role.role,
            'year':datetime.now().year,
        }
    )

def newuser(request):

    if request.method == 'POST':

        userform = AddUserForm(request.POST, request.FILES)
        if productform.is_valid():
            current_user = User.objects.create_user(userform.cleaned_data['username'])
            current_user.password = userform.cleaned_data['password']
            current_user.mail = userform.cleaned_data['mail']
            role, status = Roles.objects.get_or_create(user = current_user)
            role.role =  userform.cleaned_data['role']
            current_user.save()
            return redirect(reverse('userControls'))
                
    else:
        userform = AddUserForm()
        


    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/newuser.html',
        {
            'title': 'Новый пользователь',
            'userform': userform,
            'year':datetime.now().year,
        }
    )