"""
Definition of models.
"""

from django.db import models
# Create your models here.
from datetime import datetime
from django.contrib import admin
from django.contrib.auth.models import User
from django.urls import reverse

class Roles(models.Model):
	ROLES = (
		('admin', 'Администратор'),
		('moderator', 'Модератор'),
		('client', 'Клиент')
	)
	user = models.ForeignKey(User, on_delete = models.CASCADE, verbose_name = 'Пользователь')
	role = models.CharField(verbose_name = 'Роль', choices = ROLES, max_length=300, default = 'client')


	def __str__(self):
		return 'Роли'

	class Meta:
		db_table = 'Roles'
		ordering = ['user']
		verbose_name = 'Роли'
		verbose_name_plural = 'Роли'





class Blog(models.Model):
	title = models.CharField(max_length = 100, unique_for_date = 'posted', verbose_name = 'Заголовок')
	description = models.TextField(verbose_name = 'Краткое содержание')
	content = models.TextField(verbose_name = 'Полное содержание')
	posted = models.DateTimeField(default = datetime.now(), db_index = True, verbose_name = 'Опубликовано')
	author = models.ForeignKey(User, null=True, blank=True, on_delete = models.SET_NULL, verbose_name = "Автор")
	image = models.FileField(default = 'temp.jpg', verbose_name = 'Путь к картинке')

	def get_absolute_url(self):
		return reverse('blogpost', args=[str(self.id)])

	def __str__(self):
		return self.title

	class Meta:
		db_table = 'Posts'
		ordering = ['posted']
		verbose_name = 'Статья блога'
		verbose_name_plural = 'Статьи блога'



class Comment(models.Model):
	text = models.TextField(verbose_name = 'Комментарий')
	date = models.DateTimeField(default = datetime.now(), db_index = True, verbose_name = 'Дата')
	author = models.ForeignKey(User, on_delete = models.CASCADE, verbose_name = "Автор")
	post = models.ForeignKey(Blog, on_delete = models.CASCADE, verbose_name = "Статья")


	def __str__(self):
		return 'Комментарий %s к %s' % (self.author, self.post)

	class Meta:
		db_table = 'Comments'
		ordering = ['-date']
		verbose_name = 'Комментарий'
		verbose_name_plural = 'Комментарии к статьям блога'



class Shop(models.Model):
	name = models.TextField(verbose_name = 'Название товара')
	short = models.TextField(verbose_name = 'Краткое описание', max_length = 200)
	text = models.TextField(verbose_name = 'Описание товара')
	price = models.IntegerField(verbose_name = 'Цена')
	category = models.CharField(verbose_name = 'Категория',max_length = 300, choices = (
		('cat_1', 'Фигурки'),
		('cat_2', 'Значки'),
		('cat_3', 'Постеры')
		))
	image = models.FileField(default = 'temp.jpg', verbose_name = 'Путь к картинке')


	def __str__(self):
		return 'Товар %s: %s' % (self.id, self.name)

	class Meta:
		db_table = 'Goods'
		ordering = ['id']
		verbose_name = 'Товары'
		verbose_name_plural = 'Товары'

class Orders(models.Model):
	STATUS = (
		('incart', 'В корзине'),
		('intransit', 'Доставляется'),
		('delivered', 'Доставлен')
	)
	holder = models.ForeignKey(User, on_delete = models.CASCADE, verbose_name = 'Покупатель')
	status = models.CharField(verbose_name = 'Статус', choices = STATUS, max_length=300)
	total_price = models.IntegerField(default = 0, verbose_name = 'Итоговая стоимость')


	def __str__(self):
		return 'Заказ %s' % (self.id)

	class Meta:
		db_table = 'Orders'
		ordering = ['holder']
		verbose_name = 'Заказы'
		verbose_name_plural = 'Заказы'

class SubOrders(models.Model):
	order = models.ForeignKey(Orders, on_delete = models.CASCADE, verbose_name = 'Заказ')
	product = models.ForeignKey(Shop, on_delete = models.CASCADE, verbose_name = 'Товар')
	quantity = models.IntegerField(default = 1, verbose_name = 'Количество')
	price = models.IntegerField(default = 0, verbose_name = 'Стоимость товаров')
	


	def __str__(self):
		return 'Товар %s к заказу %s' % (self.product, self.order)

	class Meta:
		db_table = 'SubOrders'
		ordering = ['order']
		verbose_name = 'Товары'
		verbose_name_plural = 'Товары заказа'


admin.site.register(Blog)
admin.site.register(Comment)
admin.site.register(Shop)
admin.site.register(Orders)
admin.site.register(SubOrders)
admin.site.register(Roles)
