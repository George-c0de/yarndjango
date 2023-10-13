# Generated by Django 4.0.2 on 2022-04-20 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_alter_doptoproductorder_options_product_shops_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='defaultproduct',
            name='dops',
            field=models.ManyToManyField(to='main.Dops', verbose_name='Допы в карточке товара'),
        ),
        migrations.AddField(
            model_name='defaultproduct',
            name='dopscart',
            field=models.ManyToManyField(to='main.DefaultProduct', verbose_name='Допы для корзины, если там этот товар'),
        ),
        migrations.AddField(
            model_name='defaultproduct',
            name='shops',
            field=models.ManyToManyField(to='main.Shop', verbose_name='Пиццерии'),
        ),
        migrations.AddField(
            model_name='product',
            name='active',
            field=models.BooleanField(default=True, verbose_name='Опубликовать'),
        ),
        migrations.AddField(
            model_name='productgroup',
            name='active',
            field=models.BooleanField(default=True, verbose_name='Опубликовать'),
        ),
        migrations.AlterField(
            model_name='productgroup',
            name='hit',
            field=models.BooleanField(default=False, verbose_name='Хит'),
        ),
        migrations.AlterField(
            model_name='productgroup',
            name='new',
            field=models.BooleanField(default=False, verbose_name='Новинка'),
        ),
    ]
