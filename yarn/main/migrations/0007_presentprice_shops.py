# Generated by Django 4.0.2 on 2022-04-20 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_presentprice'),
    ]

    operations = [
        migrations.AddField(
            model_name='presentprice',
            name='shops',
            field=models.ManyToManyField(to='main.Shop', verbose_name='Пиццерии'),
        ),
    ]