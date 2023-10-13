from email.policy import default
from fileinput import filename
from math import floor
from operator import mod
from pyexpat import model
from statistics import mode
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from numpy import size
import qrcode
import qrcode.image.svg
from io import BytesIO
from django.core.files import File
from PIL import Image,ImageDraw
# import yarn.settings
from django.conf import settings
from django.utils.timezone import now
from django.db.models.fields.files import ImageFieldFile, FileField
from django.conf import settings




class Shop(models.Model):
    street = models.CharField(max_length=500,verbose_name='улица',default='')
    # street_list = models.TextField()
    house = models.CharField(max_length=250,verbose_name='Дом',default='1')
    open = models.TimeField('Понедельник Открывается в:',default=now)
    close = models.TimeField('Понедельник Закрывается в:',default=now)
    open2 = models.TimeField('Вторник Открывается в:',default=now)
    close2 = models.TimeField('Вторник Закрывается в:',default=now)
    open3 = models.TimeField('Среда Открывается в:',default=now)
    close3 = models.TimeField('Среда Закрывается в:',default=now)
    open4 = models.TimeField('Четверг Открывается в:',default=now)
    close4 = models.TimeField('Четверг Закрывается в:',default=now)
    open5 = models.TimeField('Пятница Открывается в:',default=now)
    close5 = models.TimeField('Пятница Закрывается в:',default=now)
    open6 = models.TimeField('Суббота Открывается в:',default=now)
    close6 = models.TimeField('Суббота Закрывается в:',default=now)
    open7 = models.TimeField('Воскресенье Открывается в:',default=now)
    close7 = models.TimeField('Воскресенье Закрывается в:',default=now)
    minimalorder = models.IntegerField('Сумма миннимального заказа:',default=0)
    saleon = models.IntegerField('Скидка на вынос %:',default=0)
    mailsend = models.CharField('Почта для уведомлений :',max_length=255,default='')
    globalmail = models.CharField('Почта для дублирования уведомлений:',max_length=255,default='')
    zone = models.FileField(upload_to ='kml/',default='settings.MEDIA_ROOT/kml/default.kml',verbose_name='Зоны доставки(в формате KML)')

    def __str__(self):
        return self.street
    class Meta:
        verbose_name = u'Наcтройки пиццерии'
        verbose_name_plural = u'Наcтройки пиццерий'

# class UserLogginedManager(models.Manager):
#     def create(self, **obj_data):
#         # Do some extra stuff here on the submitted data before saving...
#         # For example...
#         # obj_data['phone'] = my_computed_value(obj_data['my_other_field'])
#         qrimage = qrcode.make('')
#         # Now call the super method which does the actual creation
#         return super().create(**obj_data) # Python 3 syntax!!


class UserLoggined(models.Model):
    device = models.CharField('Устройство',max_length=200)
    loggined = models.BooleanField('Авторизован',default=False)
    phone = models.CharField('Номер телефона',max_length=255,blank=True)
    name = models.CharField('Имя',max_length=255,blank=True,default='')
    birthday = models.CharField('День рождения',max_length=255,blank=True,default='')
    street = models.CharField('Улиц',max_length=255,blank=True,default='')
    house = models.CharField('Дом',max_length=255,blank=True,default='')
    apartament = models.CharField('Квартира',max_length=255,blank=True,default='')
    enter = models.CharField('Подъезд',max_length=255,blank=True,default='')
    floor = models.CharField('Этаж',max_length=255,blank=True,default='')
    code = models.CharField('Код',max_length=255,blank=True,default='')
    address_name=models.CharField('Название адреса',max_length=255,blank=True,default='')
    address_comment = models.TextField('Комментарий',blank=True,default='')
    pickup = models.CharField('Самовывоз',max_length=255,blank=True,default='')
    delivery_choice = models.BooleanField('Выбор доставки',default=True,blank=True)
    bonuses = models.IntegerField('Бонусы',default=0,blank=True)
    push = models.BooleanField(default=True,verbose_name='Push уведомления')
    email = models.CharField(default='',max_length=300,verbose_name='Email',blank=True)
    qr = models.ImageField('QR Code, данное поле не для заполнения ',upload_to='media/',blank=True)
    # objects = UserLogginedManager()
    def __str__(self):
        return self.device
    def save(self,*args,**kwargs):
        qrimage = qrcode.make(f'{settings.SITE_URL}/admin/main/userloggined/{self.pk}/change/')
        qroffset = Image.new('RGB',(410,410),'white')
        qroffset.paste(qrimage)
        filename = f'{self.name}-{self.pk}qr.png'
        stream = BytesIO()
        qroffset.save(stream,'PNG')
        self.qr.save(filename,File(stream),save=False)
        qroffset.close()
        super().save(*args,**kwargs)
    class Meta:
        verbose_name = u'Клиент'
        verbose_name_plural = u'Клиенты'

        
class UserStart(models.Model):
    session = models.CharField(max_length=200)
    def __str__(self):
        return self.title

class Category(models.Model):
    title = models.CharField('Название',max_length=150)
    def __str__(self):
        return self.title
    class Meta:
        verbose_name = u'Категория'
        verbose_name_plural = u'Категории'


class Cart(models.Model):
    session = models.CharField(max_length=250)
    def __str__(self):
        return self.session

def django_sub_dict(obj):
    allowed_fields = obj.allowed_fields() # pick the list containing the requested fields
    sub_dict = {}
    for field in obj._meta.fields: # go through all the fields of the model (obj)
        if field.name in allowed_fields: # be sure to only pick fields requested
            if field.is_relation: # will result in true if it's a foreign key
                sub_dict[field.name] = django_sub_dict(
                    getattr(obj, field.name)) # call this function, with a new object, the model which is being referred to by the foreign key.
            # elif field.is_file:
            #     sub_dict[field.name] = getattr(obj, field.image_url.url)
            else: # not a foreign key? Just include the value (e.g., float, integer, string)
                sub_dict[field.name] = getattr(obj, field.name)
    sub_dict['img'] = settings.SITE_URL+ obj.img.url

    return sub_dict # returns the dict generated


class Dops(models.Model):
    title = models.CharField('Название',max_length=150)
    price = models.IntegerField('Цена',)
    img = models.ImageField('Изображение',upload_to='media/')
    def natural_key(self):
        return django_sub_dict(self)

    def allowed_fields(self):
        return [
                'title',
                'price',
                'img.path',
                ]
    def __str__(self):
        return self.title
    class Meta:
        verbose_name = u'Дополнение'
        verbose_name_plural = u'Допы'

class DefaultProduct(models.Model):
    active = models.BooleanField(default=True,verbose_name='Опубликовать')
    title = models.CharField('Название',max_length=260)
    description = models.CharField('Описание',max_length=1200,default='')
    composition = models.TextField('Состав/Выход',default='')
    weight = models.IntegerField('Вес',blank=True)
    img = models.ImageField('Изображение',upload_to='media/')
    category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name='products',verbose_name='Категория')
    price = models.IntegerField('Цена',)
    dops = models.ManyToManyField(Dops,blank=True,verbose_name='Допы в карточке товара')
    dopscart = models.ManyToManyField('self',blank=True,verbose_name='Допы для корзины, если там этот товар')
    shops = models.ManyToManyField(Shop,blank=True,verbose_name='Пиццерии')
    hit = models.BooleanField(default=False,verbose_name='Хит')
    new = models.BooleanField(default=False,verbose_name='Новинка')
    MARKER_CHOICE = (
        (' ',' '),
        ('Острая','Острая'),
        ('Сладкая','Сладкая'),
    )
    marker = models.CharField('Острая и Сладкая:',max_length=255,choices=MARKER_CHOICE,default='Сладкая',blank=True)

    

    def __str__(self):
        return self.title
    class Meta:
        verbose_name = u'Товар'
        verbose_name_plural = u'Список товаров'
        # unique_together = ['dops']

class ProductGroup(models.Model):
    active = models.BooleanField(default=True,verbose_name='Опубликовать')
    title = models.CharField('Название',max_length=250)
    description = models.TextField('Описание')
    hit = models.BooleanField(default=False,verbose_name='Хит')
    new = models.BooleanField(default=False,verbose_name='Новинка')
    MARKER_CHOICE = (
        (' ',' '),
        ('Острая','Острая'),
        ('Сладкая','Сладкая'),
    )
    marker = models.CharField('Острая и Сладкая:',max_length=255,choices=MARKER_CHOICE,default='Сладкая',blank=True)

    def __str__(self):
        return self.title
    class Meta:
        verbose_name = u'Пицца'
        verbose_name_plural = u'Список Пиццы'



class Product(models.Model):
    active = models.BooleanField(default=True,verbose_name='Опубликовать')
    group = models.ForeignKey(ProductGroup,on_delete=models.CASCADE,related_name='types',verbose_name='Группа товаров',default=1)
    # title = models.CharField('Название',max_length=260,default)
    # dough = models.CharField('Тесто',max_length=260)
    composition = models.TextField('Состав/Выход',)
    size = models.CharField('Размер', max_length=100,default='25')
    weight = models.IntegerField('Вес',blank=True,default=0)
    # weight_per_30 = models.IntegerField('Вес 38см',blank=True)
    price = models.IntegerField('Цена',blank=True,default=0)
    # price_per_30 = models.IntegerField('Цена 38см',blank=True)
    img = models.ImageField('Изображение',upload_to='media/')
    dops = models.ManyToManyField(Dops,verbose_name='Допы в карточке товара')
    dopscart = models.ManyToManyField(DefaultProduct,verbose_name='Допы для корзины, если там этот товар')
    shops = models.ManyToManyField(Shop,verbose_name='Пиццерии')
    def __str__(self):
        return 'Название: ' + self.group.title +' Размер: '+ str(self.size) +' Цена: '+ str(self.price)
    class Meta:
        verbose_name = u'Вариация'
        verbose_name_plural = u'Вариации'


class ProductToCart(models.Model):
    cart = models.ForeignKey(UserLoggined,on_delete=models.CASCADE,related_name='products')
    product = models.ForeignKey(Product,on_delete=models.CASCADE,default=1,verbose_name='Продукт в корзине',related_name='tocart')
    count = models.IntegerField(default=1)
    # size = models.IntegerField(default=1)
    # price = models.IntegerField(default=1)



class DopToProductCart(models.Model):
    dop = models.ForeignKey(Dops,on_delete=models.CASCADE)
    product = models.ForeignKey(ProductToCart,on_delete=models.CASCADE,related_name='dops')
    def __str__(self):
        return self.dop.title



class DefaultProductToCart(models.Model):
    cart = models.ForeignKey(UserLoggined,on_delete=models.CASCADE,related_name='default_prod')
    product = models.ForeignKey(DefaultProduct,on_delete=models.CASCADE)
    count = models.IntegerField()

class DopToDefaultProductToCart(models.Model):
    dop = models.ForeignKey(Dops,on_delete=models.CASCADE)
    product = models.ForeignKey(DefaultProductToCart,on_delete=models.CASCADE,related_name='dops')
    def __str__(self):
        return self.dop.title




class News(models.Model):
    title= models.CharField('Название',max_length=200)
    img =models.ImageField('Изображение',upload_to='media/',blank=True,default='')
    description = models.CharField('Описание',max_length=1024)
    text = models.TextField(verbose_name='Текст')
    created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title
    class Meta:
        verbose_name = u'Акция'
        verbose_name_plural = u'Акции'


class Address(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    street = models.CharField(max_length=250)
    apartment = models.CharField(max_length=100,blank=True)
    house = models.CharField(max_length=100,blank=True)
    entrance = models.CharField(max_length=100,blank=True)
    code = models.CharField(max_length=100,blank=True)

    floor = models.CharField(max_length=100,blank=True)
    def __str__(self):
        return self.name + self.street


class Order(models.Model):
    idd = models.CharField('ID',max_length=250,blank=True,default='')
    user = models.ForeignKey(UserLoggined,on_delete=models.CASCADE,related_name='orders',verbose_name="Пользователь")
    comment = models.TextField('Комментарий',blank=True)
    # address = models.CharField('Адрес',max_length=500,blank=True,default='')
    street = models.CharField('Улиц',max_length=255,blank=True,default='')
    house = models.CharField('Дом',max_length=255,blank=True,default='')
    apartament = models.CharField('Квартира',max_length=255,blank=True,default='')
    enter = models.CharField('Подъезд',max_length=255,blank=True,default='')
    floor = models.CharField('Этаж',max_length=255,blank=True,default='')
    code = models.CharField('Код',max_length=255,blank=True,default='')
    address_name=models.CharField('Название адреса',max_length=255,blank=True,default='')
    address_comment = models.TextField('Комментарий',blank=True,default='')
    pickup = models.CharField('Самовывоз',max_length=255,blank=True,default='')
    delivery_choice = models.BooleanField('Выбор доставки',default=True,blank=True)
    price = models.IntegerField('Сумма')
    bonusesused = models.IntegerField('Бонусов использовано',default=0,blank=True)
    bonusesadded = models.IntegerField('Бонусов начислено',default=0,blank=True)
    
    promocodesale = models.IntegerField('Скидка %',default=0,blank=True)
    shop = models.ForeignKey(Shop,on_delete=models.CASCADE,related_name='orders',blank=True,default='',verbose_name="Заказ отправлен в ресторан")
    phone = models.CharField('Номер телефона клиента:',max_length=255,default='')
    created = models.DateTimeField('Заказ был создан в:',default=now)

    PAY_CHOICE = (
        ('Онлайн оплата','Онлайн оплата'),
        ('Наличные','Наличные'),
    )
    pay_method = models.CharField('Способ оплаты:',max_length=255,choices=PAY_CHOICE,default='Наличные')
    STATUS_CHOICE = (
        ('На доставку','На доставку'),
        ('Самовывоз','Самовывоз'),
    )
    created_at = models.DateTimeField('Дата и время заказа',auto_now_add=True)
    status = models.CharField('Доставка/Самовывоз',max_length=100,choices=STATUS_CHOICE,default='На доставку')

    def getaddress(self):
        return 'Ярославль, ул. '+ self.street +', д. ' +self.house


    def __str__(self):
        return self.user.device
    class Meta:
        verbose_name = u'Заказ'
        verbose_name_plural = u'Заказы'


class OrderProduct(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE,related_name='products')
    product = models.ForeignKey(Product,on_delete=models.CASCADE,default=0,verbose_name='Товар в заказе')
    count = models.IntegerField('Количество',default=0)
    def __str__(self):
        return self.product.group.title + str(self.product.size) + str(self.product.price)
    class Meta:
        verbose_name = u'Товары'
        verbose_name_plural = u'Товары'

class DopToProductOrder(models.Model):
    dop = models.ForeignKey(Dops,on_delete=models.CASCADE,verbose_name='Дополнение')
    product = models.ForeignKey(OrderProduct,on_delete=models.CASCADE,related_name='dops')
    def __str__(self):
        return self.dop.title
    class Meta:
        verbose_name = u'Допы к товару в заказе'
        verbose_name_plural = u'Допы к товару в заказе'



class OrderProductDefault(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE,related_name='productsdefault')
    product = models.ForeignKey(DefaultProduct,on_delete=models.CASCADE,default=0,verbose_name='Товар в заказе')
    count = models.IntegerField('Количество',default=0)
    def __str__(self):
        return self.product.group.title + str(self.product.size) + str(self.product.price)
    class Meta:
        verbose_name = u'Товары'
        verbose_name_plural = u'Товары'

class DopToProductDefaultOrder(models.Model):
    dop = models.ForeignKey(Dops,on_delete=models.CASCADE,verbose_name='Дополнение')
    product = models.ForeignKey(OrderProductDefault,on_delete=models.CASCADE,related_name='dops')
    def __str__(self):
        return self.dop.title
    class Meta:
        verbose_name = u'Допы к товару в заказе'
        verbose_name_plural = u'Допы к товару в заказе'


class Comment(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE,related_name='commentation')
    commentation = models.TextField()
    raiting_one = models.IntegerField(blank=True,default=5)
    raiting_two = models.IntegerField(blank=True,default=5)
    raiting_three = models.IntegerField(blank=True,default=5)
    raiting_four = models.IntegerField(blank=True,default=5)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    class Meta:
        verbose_name = u'Комментарий'
        verbose_name_plural = u'Комментарии'


class Promocode(models.Model):
    title = models.CharField('Промокод',max_length=150)
    sale = models.IntegerField('Скидка %')
    def __str__(self):
        return self.title
    class Meta:
        verbose_name = u'Промокод'
        verbose_name_plural = u'Промокоды'



class PromocodeToCart(models.Model):
    promocode = models.ForeignKey(Promocode,on_delete=models.CASCADE)
    cart = models.ForeignKey(UserLoggined,on_delete=models.CASCADE,related_name='promocode')


class PresentPrice(models.Model):
    price = models.IntegerField('Сумма')
    dopscart = models.ManyToManyField(DefaultProduct,verbose_name='Подарок')
    shops = models.ManyToManyField(Shop,verbose_name='Пиццерии')
    class Meta:
        verbose_name = u'Подарок от суммы заказа'
        verbose_name_plural = u'Подарки от суммы заказа'


class Masterclass(models.Model):
    img = models.ImageField(upload_to='media/')
    title = models.CharField(max_length=150)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    date = models.DateTimeField()
    price = models.IntegerField()
    STATUS_CHOICE = (
        ('Открыт для записи','Открыт для записи'),
        ('Завершенный','Завершенный'),
    )
    status = models.CharField(max_length=150,choices=STATUS_CHOICE)
    def __str__(self):
        return self.title

class MasterclassOrder(models.Model):
    masterclass = models.ForeignKey(Masterclass,on_delete=models.CASCADE,blank=True,null=True)
    phone = models.CharField(max_length=150)
    comment = models.TextField(blank=True)
    def __str__(self):
        return '%s - %s'%(self.phone,self.masterclass.title)


class PolicyPage(models.Model):
    text = models.TextField('Текст')
    def __str__(self):
        return self.text
    class Meta:
        verbose_name = u'Страница "Правовые документы"'
        verbose_name_plural = u'Страница "Правовые документы"'


class AboutPage(models.Model):
    text = models.TextField('Текст')
    def __str__(self):
        return self.text
    class Meta:
        verbose_name = u'Страница "О приложении"'
        verbose_name_plural = u'Страница "О приложении"'

