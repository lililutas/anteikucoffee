# Generated by Django 2.2.19 on 2021-11-27 11:05

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_auto_20211124_1418'),
    ]

    operations = [
        migrations.AddField(
            model_name='shop',
            name='image',
            field=models.FileField(default='temp.jpg', upload_to='', verbose_name='Путь к картинке'),
        ),
        migrations.AlterField(
            model_name='blog',
            name='posted',
            field=models.DateTimeField(db_index=True, default=datetime.datetime(2021, 11, 27, 14, 5, 8, 132316), verbose_name='Опубликовано'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='date',
            field=models.DateTimeField(db_index=True, default=datetime.datetime(2021, 11, 27, 14, 5, 8, 133315), verbose_name='Дата'),
        ),
    ]
