# from attr import field
from django.contrib.auth.models import User, Group
from numpy import source
from rest_framework import serializers
from .models import *

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']

class UserLogginedSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserLoggined
        fields = ['name', 'phone', 'device', 'loggined','birthday','street','house','apartament','enter','floor','code','address_name','address_comment','pickup','delivery_choice','bonuses','qr','push','email']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class NewsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = News
        fields = ['img', 'description', 'title', 'created','text','pk']


class DopsItemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Dops
        fields = ['img','title','price']


class CategoryForDefaultProductasDopsSerializes(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ['title']


class DefaultProductasDops(serializers.HyperlinkedModelSerializer):
    # category = CategoryForDefaultProductasDopsSerializes(many=True,read_only=True)
    category_name = serializers.CharField(source='category.title')
    class Meta:
        model = DefaultProduct
        fields = ['title','description','weight','img','price','category_name']


class ProductItemSerializer(serializers.HyperlinkedModelSerializer):
    dops = DopsItemSerializer(many=True,read_only=True)
    dopscart = DefaultProductasDops(many=True,read_only=True)
    class Meta:
        model = Product
        fields = ['size', 'weight','composition', 'price','img','dops','dopscart']


# Serializers define the API representation.
class ProductSerializer(serializers.HyperlinkedModelSerializer):
    types = ProductItemSerializer(many=True,read_only=True)

    class Meta:
        model = ProductGroup
        fields = ['pk','title', 'description', 'hit', 'new','types']


class DopsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Dops
        fields = ['title', 'img', 'price']


class DopsToCartSerializer(serializers.HyperlinkedModelSerializer):
    # category = CategoryForDefaultProductasDopsSerializes(many=True,read_only=True)
    price = serializers.CharField(source='dop.price')
    title = serializers.CharField(source='dop.title')
    class Meta:
        model = DefaultProduct
        fields = ['title','price']

class ProductToCartSerializer(serializers.HyperlinkedModelSerializer):
    img = serializers.CharField(source='product.img')
    title = serializers.CharField(source='product.group.title')
    # dops = serializers.CharField(source='')
    price = serializers.CharField(source='product.price')
    size = serializers.CharField(source='product.size')

    # dops = serializers.StringRelatedField(many=True)
    dops = DopsToCartSerializer(many=True,read_only=True)

    class Meta:
        model = ProductToCart
        fields = ['price','size','count','img','title','pk','dops']


class ProductToCartDefaultSerializer(serializers.HyperlinkedModelSerializer):
    img = serializers.CharField(source='product.img')
    title = serializers.CharField(source='product.title')
    weight = serializers.CharField(source='product.weight')
    price = serializers.CharField(source='product.price')

    dops = DopsToCartSerializer(many=True,read_only=True)

    class Meta:
        model = DefaultProductToCart
        fields = ['price', 'count','img','title','pk','dops','weight']



class OrderProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProduct
        fields = ['product']
        


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['commentation','raiting_one','raiting_two','raiting_three','raiting_four']


class OrderItemSerializer(serializers.HyperlinkedModelSerializer):
    img = serializers.CharField(source='product.img')

    class Meta:
        model = OrderProduct
        fields = ['img']

class OrderItemDefaultSerializer(serializers.HyperlinkedModelSerializer):
    img = serializers.CharField(source='product.img')

    class Meta:
        model = OrderProductDefault
        fields = ['img']



class OrderSerializer(serializers.HyperlinkedModelSerializer):
    # name = serializers.CharField(source='address.name')
    # street = serializers.CharField(source='address.street')
    # apartment = serializers.CharField(source='address.apartment')
    # house = serializers.CharField(source='address.house')
    address = serializers.CharField(source='getaddress')
    products =OrderItemSerializer(many=True,read_only=True)
    productsdefault = OrderItemDefaultSerializer(many=True,read_only=True)

    # productss = OrderProductSerializer(source='products', many=True)
    # productsdefault = OrderProductSerializer(source='products', many=True)
    # comment = CommentSerializer(source='commentation',many=True)
    class Meta:
        model = Order
        fields = ['idd','address','products','productsdefault','created_at','price','status',]
        
class DopsForCategories(serializers.ModelSerializer):
    # products = serializers.PrimaryKeyRelatedField(queryset=DefaultProduct.objects.all(), many=True)
    class Meta:
        model = Dops
        fields = ('title','price','img')

class DefaultProductSerializer(serializers.ModelSerializer):
    dops = DopsForCategories(many=True, read_only=True)
    class Meta:
        model = DefaultProduct
        fields = ['title','description','weight','img','price','pk','dops']


class CategoriesSerializer(serializers.HyperlinkedModelSerializer):
    productss = DefaultProductSerializer(source='products', many=True)
    class Meta:
        model = Category
        fields = ['title','productss','pk']


class ShopsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Shop
        fields = ['street']
