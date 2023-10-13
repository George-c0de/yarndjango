from distutils.filelist import findall
from hashlib import new
from django.shortcuts import render, redirect
from httplib2 import Http
from pygame import math
from zmq import device
from .models import *
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
import requests
import uuid
from django.contrib.auth import login, authenticate
from django.contrib.auth import logout as django_logout
from django.core import serializers
from rest_framework import routers, serializers, viewsets, generics
from .serializersmain import *
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from yandex_geocoder import Client
from decimal import Decimal
import numpy
import math 
from datetime import datetime
import pytz
from django.conf import settings
import re
from requests_html import HTMLSession,AsyncHTMLSession
import pyppeteer
import asyncio
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import service 
from bs4 import BeautifulSoup
import time as tm
import random
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder

USER_PASSWORD='20012004Davidfe'
yandexkey = '94666ced-16f9-442e-a87d-75d9eb22ec6b'
client = Client(yandexkey)

async def load_page_helper(url: str):
    """Helper to parse obfuscated / JS-loaded profiles like Facebook.
    We need a separate function to handle requests-html's async nature
    in Django's event loop."""
    session = AsyncHTMLSession()
    browser = await pyppeteer.launch({
        'ignoreHTTPSErrors': True,
        'headless': True,
        'handleSIGINT': False,
        'handleSIGTERM': False,
        'handleSIGHUP': False
    })
    session._browser = browser
    resp = await session.get(url)
    await resp.html.arender()
    await session.close()
    return resp.html.raw_html

def pickup_choice(request):
    if request.method == 'GET':
        user = UserLoggined.objects.get(device=request.GET['device'])
        user.delivery_choice = False
        user.save()
        return HttpResponse(200)
    return HttpResponse(400)

def delivery_choise(request):
    if request.method == 'GET':
        user = UserLoggined.objects.get(device=request.GET['device'])
        user.delivery_choice = True
        user.save()
    return HttpResponse(40)

def pickup_change(request):
    if request.method == 'GET':
        user = UserLoggined.objects.get(device=request.GET['device'])
        user.pickup = request.GET['restoraunt']
        user.save()
        return HttpResponse(200)
    return HttpResponse(400)

def getpolicy(request):
    return HttpResponse(PolicyPage.objects.first().text)

def getabout(request):
    return HttpResponse(AboutPage.objects.first().text)

def savename(request):
    if request.method == 'GET':
        user = UserLoggined.objects.get(device=request.GET['device'])
        user.name = request.GET['name']
        user.save()
        return HttpResponse(200)
    return HttpResponse(400)
def saveemail(request):
    if request.method == 'GET':
        user = UserLoggined.objects.get(device=request.GET['device'])
        user.email = request.GET['email']
        user.save()
        return HttpResponse(200)
    return HttpResponse(400)
def savebirthday(request):
    if request.method == 'GET':
        user = UserLoggined.objects.get(device=request.GET['device'])
        user.birthday = request.GET['birthday']
        user.save()
        return HttpResponse(200)
    return HttpResponse(400)
def savepush(request):
    if request.method == 'GET':
        user = UserLoggined.objects.get(device=request.GET['device'])
        if request.GET['push'] == 'true':
            user.push = True
        else:
            user.push = False
        user.save()
        return HttpResponse(200)
    return HttpResponse(400)
@csrf_exempt
def orderpostapp(request):
    if request.method == 'GET':
        cart = UserLoggined.objects.get(device=request.GET['device'])
        user = UserLoggined.objects.get(device=request.GET['device'])
        if request.GET['type'] == 'delivery':
            name = request.GET['name']
            street = request.GET['street']
            apartment = request.GET['apartment']
            house = request.GET['house']
            entrance = request.GET['entrance']
            code = request.GET['code']
            floor = request.GET['floor']
            com = request.GET['comment']
            time = request.GET['time']
            shop = request.GET['shop']
            paymethod = request.GET['paymethod']
            bonususe = request.GET['bonususe']
            commto = com+'   Время доставки'+time
            idd = random.randint(10000,99999)
            # ad = Address.objects.create(user=user,name=name,street=street,apartment=apartment,house=house,entrance=entrance,code=code,floor=floor)
            order = Order.objects.create(
                id = idd,
                street =street,
                apartment=apartment,
                house = house,
                entrance = entrance,
                code = code,
                floor = floor,
                user=user,
                price=request.GET['price'],
                comment=commto,
                pay_method = paymethod,
                phone = user.phone,
                shop = Shop.objects.get(street=shop),
                status='На доставку'
            )
            sum = 0
            a = ProductToCart.objects.filter(cart=cart)
            f = DefaultProductToCart.objects.filter(cart=cart)
            try:
                prom = PromocodeToCart.objects.filter(cart=cart).last()
                s = prom.promocode.sale
                order.promocodesale = s
                # sum = 0
                for i in a:
                    sumdops = 0
                    oredit = OrderProduct.objects.create(order=order,product=i.product,count=i.count)
                    dops = DopToProductCart.objects.filter(product=i)
                    for d in dops:
                        sumdops += d.dop.price
                        DopToProductOrder.objects.create(dop=d.dop,product=oredit)
                    sum += (i.product.price + sumdops) * i.count
                for i in f:
                    sumdops = 0
                    oredit = OrderProductDefault.objects.create(order=order,product=i.product,count=i.count)
                    dops = DopToProductCart.objects.filter(product=i)
                    for d in dops:
                        sumdops += d.dop.price
                        DopToProductDefaultOrder.objects.create(dop=d.dop,product=oredit)

                    sum += (i.product.price + sumdops) * i.count
                sum = sum - (sum * (s/100))
            except:
                for i in a:
                    sumdops = 0
                    oredit = OrderProduct.objects.create(order=order,product=i.product,count=i.count)
                    dops = DopToProductCart.objects.filter(product=i)
                    for d in dops:
                        sumdops += d.dop.price
                        DopToProductOrder.objects.create(dop=d.dop,product=oredit)
                    sum += (i.product.price + sumdops) * i.count
                for i in f:
                    sumdops = 0
                    oredit = OrderProductDefault.objects.create(order=order,product=i.product,count=i.count)
                    dops = DopToProductCart.objects.filter(product=i)
                    for d in dops:
                        sumdops += d.dop.price
                        DopToProductDefaultOrder.objects.create(dop=d.dop,product=oredit)
                    sum += (i.product.price + sumdops) * i.count
                # sum = sum - (sum * (s/100))
            order.price = sum
            order.save()
        else:
            # time = request.GET['time']
            # restoran = request.GET['restoran']
            # price = request.GET['price']
            # comment = request.GET['comment']
            # com = comment + ' Самовывоз - '+ restoran + ', Время - ' + time
            # order = Order.objects.create(user=user,price=request.GET['price'],comment=com,status='Обрабатывается',commented=False)

            com = request.GET['comment']
            time = request.GET['time']
            shop = request.GET['shop']
            paymethod = request.GET['paymethod']
            commto = com+'Время доставки'+time
            idd = random.randint(10000,99999)
            # ad = Address.objects.create(user=user,name=name,street=street,apartment=apartment,house=house,entrance=entrance,code=code,floor=floor)
            order = Order.objects.create(
                id = idd,
                user=user,
                price=request.GET['price'],
                comment=commto,
                shop = Shop.objects.get(street=shop),
                status='Обрабатывается'
            )
            sum = 0
            a = ProductToCart.objects.filter(cart=cart)
            f = DefaultProductToCart.objects.filter(cart=cart)
            try:
                prom = PromocodeToCart.objects.filter(cart=cart).last()
                s = prom.promocode.sale
                # sum = 0
                for i in a:
                    sumdops = 0
                    oredit = OrderProduct.objects.create(order=order,product=i.product,count=i.count)
                    dops = DopToProductCart.objects.filter(product=i)
                    for d in dops:
                        sumdops += d.dop.price
                        DopToProductOrder.objects.create(dop=d.dop,product=oredit)
                    sum += (i.product.price + sumdops) * i.count
                for i in f:
                    sumdops = 0
                    oredit = OrderProductDefault.objects.create(order=order,product=i.product,count=i.count)
                    dops = DopToProductCart.objects.filter(product=i)
                    for d in dops:
                        sumdops += d.dop.price
                        DopToProductDefaultOrder.objects.create(dop=d.dop,product=oredit)

                    sum += (i.product.price + sumdops) * i.count
                sum = sum - (sum * (s/100))
            except:
                for i in a:
                    sumdops = 0
                    oredit = OrderProduct.objects.create(order=order,product=i.product,count=i.count)
                    dops = DopToProductCart.objects.filter(product=i)
                    for d in dops:
                        sumdops += d.dop.price
                        DopToProductOrder.objects.create(dop=d.dop,product=oredit)
                    sum += (i.product.price + sumdops) * i.count
                for i in f:
                    sumdops = 0
                    oredit = OrderProductDefault.objects.create(order=order,product=i.product,count=i.count)
                    dops = DopToProductCart.objects.filter(product=i)
                    for d in dops:
                        sumdops += d.dop.price
                        DopToProductDefaultOrder.objects.create(dop=d.dop,product=oredit)

                    sum += (i.product.price + sumdops) * i.count
                # sum = sum - (sum * (s/100))
            order.price = sum
            order.save()

        # price = request.GET['price']
        # Configuration.account_id = "847744"
        # Configuration.secret_key = "live_Wj6HlCC7fGveqz3uX251RlIWxD3ZY66eJ7S_2YWnj-0"
        # idempotence_key = uuid.uuid4()
        # red = "https://toopizzabrothers.ru/confirmpay/?id="+str(idempotence_key)
        # payment = Payment.create({
        #     "amount": {
        #     "value": price,
        #     "currency": "RUB"
        #     },
        #     "payment_method_data": {
        #     "type": "bank_card"
        #     },
        #     "confirmation": {
        #     "type": "redirect",
        #     "return_url": red
        #     },
        #     "description": "Заказ №72"
        # }, idempotence_key)
        # order.idd = idempotence_key
        # order.save()
        # confirmation_url = payment.confirmation.confirmation_url
        print('400')
        return HttpResponse(400)

    return HttpResponse(200)


class LazyEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, DefaultProduct):
            return str(obj)
        return super().default(obj)

def cart_products(request):
    if request.method == 'GET':
        try:
            user = UserLoggined.objects.get(device=request.GET['device'])
            empt = ProductToCart.objects.filter(cart = user)
            qs = []
            for i in empt:
                for b in i.product.dopscart.all():
                    if b not in qs:
                        qs.append(b)
            qs_json = serializers.serialize('json', qs,indent = 4,use_natural_foreign_keys=True, # this or the one below makes django include the natural_key() within a model. Not sure.
                                            use_natural_primary_keys=True, )

            return HttpResponse(qs_json, content_type='application/json')
        except:
            return HttpResponse(400)
    else:
        return HttpResponse(400)

def createorderpickup(request):
    if request.method == 'GET':
        cart = UserLoggined.objects.get(device=request.GET['device'])
        user = UserLoggined.objects.get(device=request.GET['device'])


        if request.GET['type'] == 'pickup':
            pickup = request.GET['pickup']
            cart.pickup = pickup
            cart.delivery_choice = False
            cart.save()
            shop = Shop.objects.get(street=pickup)
            try:
                time = request.GET['time']
            except:
                time = ''
            try:
                if request.GET['paymethod'] == 'SingingCharacter.online':
                    paymethod = 'Онлайн оплата'
                else:
                    paymethod = 'Наличные'
            except:
                paymethod = 'Онлайн оплата'
            try:
                if request.GET['bonususe'] == 'true':
                    bonusesused = user.bonuses
                    user.bonuses = 0
                    user.save()
                else:
                    bonusesused = 0
            except:
                bonusesused = 0
            commto = 'Время доставки '+time
            idd = random.randint(10000,99999)
                        # ad = Address.objects.create(user=user,name=name,street=street,apartment=apartment,house=house,entrance=entrance,code=code,floor=floor)
            try:
                order = Order.objects.create(
                                idd = str(idd),
                                user=user,
                                price=0,
                                comment=commto,
                                pay_method = paymethod,
                                phone = user.phone,
                                shop = shop,
                                status='Самовывоз',
                                bonusesused = bonusesused,
                                delivery_choice = False
                )
            except:
                return HttpResponse('400. Ошибка в создании заказа')
            sum = 0
            a = ProductToCart.objects.filter(cart=cart)
            f = DefaultProductToCart.objects.filter(cart=cart)
            try:
                prom = PromocodeToCart.objects.filter(cart=cart).last()
                s = prom.promocode.sale
                order.promocodesale = s
                            # sum = 0
                for i in a:
                    sumdops = 0
                    oredit = OrderProduct.objects.create(order=order,product=i.product,count=i.count)
                    dops = DopToProductCart.objects.filter(product=i)
                    for d in dops:
                        sumdops += d.dop.price
                        DopToProductOrder.objects.create(dop=d.dop,product=oredit)
                    sum += (i.product.price + sumdops) * i.count
                    i.delete()
                for i in f:
                    sumdops = 0
                    oredit = OrderProductDefault.objects.create(order=order,product=i.product,count=i.count)
                    dops = DopToDefaultProductToCart.objects.filter(product=i)
                    for d in dops:
                        sumdops += d.dop.price
                        DopToProductDefaultOrder.objects.create(dop=d.dop,product=oredit)

                    sum += (i.product.price + sumdops) * i.count
                    i.delete()
                sum = sum - (sum * (s/100))
            except:                
                for i in a:
                    sumdops = 0
                    oredit = OrderProduct.objects.create(order=order,product=i.product,count=i.count)
                    dops = DopToProductCart.objects.filter(product=i)
                    for d in dops:
                        sumdops += d.dop.price
                        DopToProductOrder.objects.create(dop=d.dop,product=oredit)
                    sum += (i.product.price + sumdops) * i.count
                    i.delete()
                for i in f:
                    sumdops = 0
                    oredit = OrderProductDefault.objects.create(order=order,product=i.product,count=i.count)
                    dops = DopToDefaultProductToCart.objects.filter(product=i)
                    for d in dops:
                        sumdops += d.dop.price
                        DopToProductDefaultOrder.objects.create(dop=d.dop,product=oredit)
                    sum += (i.product.price + sumdops) * i.count
                    i.delete()
                            # sum = sum - (sum * (s/100))
            sum -= bonusesused
            if shop.saleon != 0:
                sum = sum - (sum * (sum/shop.saleon))
            order.price = sum
            order.save()



    return HttpResponse(200)

def check_address_answer(request):
    if request.method == 'GET':
        url = settings.SITE_URL + '/checkaddressin/?street='+request.GET['street']+'&house='+request.GET['house']
        op = webdriver.ChromeOptions()
        op.add_argument('headless')
        driver = webdriver.Chrome("/Users/davidbabayan/Downloads/chromedriver",options=op)
        driver.get(url)
        tm.sleep(1)
        answer = driver.page_source.split('<div id="info">')[1].split('</div>')[0]

        cart = UserLoggined.objects.get(device=request.GET['device'])

        a = ProductToCart.objects.filter(cart=cart)
        f = DefaultProductToCart.objects.filter(cart=cart)
        try:
            prom = PromocodeToCart.objects.filter(cart=cart).last()
            s = prom.promocode.sale
            sum = 0
            for i in a:
                # sum += i.product.price * i.count
                sumdops = 0
                dops = DopToProductCart.objects.filter(product=i)
                for d in dops:
                    sumdops += d.dop.price
                sum += (i.product.price + sumdops) * i.count
            for i in f:
                sum += i.product.price * i.count
            sum = sum - (sum * (s/100))
            # return HttpResponse(int(sum))
        except:
            sum = 0
            for i in a:
                sumdops = 0
                dops = DopToProductCart.objects.filter(product=i)
                for d in dops:
                    sumdops += d.dop.price
                sum += (i.product.price + sumdops) * i.count
            for i in f:
                sum += i.product.price * i.count
            
            # return HttpResponse(int(sum))
        print(a)
        if answer == 'Пиццерия закрыта':
            return HttpResponse('400. Пиццерия закрыта')
        else:
            i = answer.split('.')[0]
            if i == 'Входит в область доставки':
                mini = int(answer.split('.')[1].split('-')[1].replace(' ', ''))
                if sum > mini:
                    # Good
                    cart = UserLoggined.objects.get(device=request.GET['device'])
                    user = UserLoggined.objects.get(device=request.GET['device'])
                    if request.GET['type'] == 'delivery':
                        street = request.GET['street']
                        cart.street = street
                        house = str(request.GET['house'])
                        cart.house = house
                        try:
                            name = request.GET['name']
                        except:
                            name = ''
                        try:
                            apartment = str(request.GET['apartment'])
                        except:
                            apartment = ''
                        try:
                            entrance = str(request.GET['entrance'])
                        except:
                            entrance = ''
                        try:    
                            code = str(request.GET['code'])
                        except:
                            code = ''
                        try:
                            floor = str(request.GET['floor'])
                        except:
                            floor = ''
                        try:
                            com = request.GET['comment']
                        except:
                            com = ''
                        try:
                            time = request.GET['time']
                        except:
                            time = ''
                        try:
                            shop = answer.split('.')[2]
                        except:
                            shop = ''
                        try:
                            if request.GET['paymethod'] == 0:
                                paymethod = 'Онлайн оплата'
                            else:
                                paymethod = 'Наличные'
                        except:
                            paymethod = 'Онлайн оплата'
                        try:
                            if request.GET['bonususe'] == 'true':
                                bonusesused = user.bonuses
                                user.bonuses = 0
                                user.save()
                            else:
                                bonusesused = 0
                        except:
                            bonusesused = 0
                        commto = com+'   Время доставки'+time
                        idd = random.randint(10000,99999)
                        # ad = Address.objects.create(user=user,name=name,street=street,apartment=apartment,house=house,entrance=entrance,code=code,floor=floor)
                        try:
                            order = Order.objects.create(
                                idd = str(idd),
                                street =street,
                                apartament=apartment,
                                house = house,
                                enter = entrance,
                                code = code,
                                floor = floor,
                                user=user,
                                price=0,
                                comment=commto,
                                pay_method = paymethod,
                                phone = user.phone,
                                shop = Shop.objects.get(street=shop),
                                status='На доставку',
                                bonusesused = bonusesused
                            )
                        except:
                            return HttpResponse('400. Ошибка в создании заказа')
                        sum = 0
                        a = ProductToCart.objects.filter(cart=cart)
                        f = DefaultProductToCart.objects.filter(cart=cart)
                        try:
                            prom = PromocodeToCart.objects.filter(cart=cart).last()
                            s = prom.promocode.sale
                            order.promocodesale = s
                            # sum = 0
                            for i in a:
                                sumdops = 0
                                oredit = OrderProduct.objects.create(order=order,product=i.product,count=i.count)
                                dops = DopToProductCart.objects.filter(product=i)
                                for d in dops:
                                    sumdops += d.dop.price
                                    DopToProductOrder.objects.create(dop=d.dop,product=oredit)
                                sum += (i.product.price + sumdops) * i.count
                                i.delete()
                            for i in f:
                                sumdops = 0
                                oredit = OrderProductDefault.objects.create(order=order,product=i.product,count=i.count)
                                dops = DopToDefaultProductToCart.objects.filter(product=i)
                                for d in dops:
                                    sumdops += d.dop.price
                                    DopToProductDefaultOrder.objects.create(dop=d.dop,product=oredit)

                                sum += (i.product.price + sumdops) * i.count
                                i.delete()
                            sum = sum - (sum * (s/100))
                        except:
                            for i in a:
                                sumdops = 0
                                oredit = OrderProduct.objects.create(order=order,product=i.product,count=i.count)
                                dops = DopToProductCart.objects.filter(product=i)
                                for d in dops:
                                    sumdops += d.dop.price
                                    DopToProductOrder.objects.create(dop=d.dop,product=oredit)
                                sum += (i.product.price + sumdops) * i.count
                                i.delete()
                            for i in f:
                                sumdops = 0
                                oredit = OrderProductDefault.objects.create(order=order,product=i.product,count=i.count)
                                dops = DopToDefaultProductToCart.objects.filter(product=i)
                                for d in dops:
                                    sumdops += d.dop.price
                                    DopToProductDefaultOrder.objects.create(dop=d.dop,product=oredit)
                                
                                sum += (i.product.price + sumdops) * i.count
                                i.delete()
                            # sum = sum - (sum * (s/100))
                        sum -= bonusesused
                        order.price = sum
                        order.save()
                    else:
                        # time = request.GET['time']
                        # restoran = request.GET['restoran']
                        # price = request.GET['price']
                        # comment = request.GET['comment']
                        # com = comment + ' Самовывоз - '+ restoran + ', Время - ' + time
                        # order = Order.objects.create(user=user,price=request.GET['price'],comment=com,status='Обрабатывается',commented=False)
                        com = request.GET['comment']
                        time = request.GET['time']
                        shop = request.GET['shop']
                        paymethod = request.GET['paymethod']
                        commto = com+'Время доставки'+time
                        idd = random.randint(10000,99999)
                        # ad = Address.objects.create(user=user,name=name,street=street,apartment=apartment,house=house,entrance=entrance,code=code,floor=floor)
                        order = Order.objects.create(
                            id = idd,
                            user=user,
                            price=request.GET['price'],
                            comment=commto,
                            shop = Shop.objects.get(street=shop),
                            status='Обрабатывается'
                        )
                        sum = 0
                        a = ProductToCart.objects.filter(cart=cart)
                        f = DefaultProductToCart.objects.filter(cart=cart)
                        try:
                            prom = PromocodeToCart.objects.filter(cart=cart).last()
                            s = prom.promocode.sale
                            # sum = 0
                            for i in a:
                                sumdops = 0
                                oredit = OrderProduct.objects.create(order=order,product=i.product,count=i.count)
                                dops = DopToProductCart.objects.filter(product=i)
                                for d in dops:
                                    sumdops += d.dop.price
                                    DopToProductOrder.objects.create(dop=d.dop,product=oredit)
                                sum += (i.product.price + sumdops) * i.count
                            for i in f:
                                sumdops = 0
                                oredit = OrderProductDefault.objects.create(order=order,product=i.product,count=i.count)
                                dops = DopToProductCart.objects.filter(product=i)
                                for d in dops:
                                    sumdops += d.dop.price
                                    DopToProductDefaultOrder.objects.create(dop=d.dop,product=oredit)

                                sum += (i.product.price + sumdops) * i.count
                            sum = sum - (sum * (s/100))
                        except:
                            for i in a:
                                sumdops = 0
                                oredit = OrderProduct.objects.create(order=order,product=i.product,count=i.count)
                                dops = DopToProductCart.objects.filter(product=i)
                                for d in dops:
                                    sumdops += d.dop.price
                                    DopToProductOrder.objects.create(dop=d.dop,product=oredit)
                                sum += (i.product.price + sumdops) * i.count
                            for i in f:
                                sumdops = 0
                                oredit = OrderProductDefault.objects.create(order=order,product=i.product,count=i.count)
                                dops = DopToProductCart.objects.filter(product=i)
                                for d in dops:
                                    sumdops += d.dop.price
                                    DopToProductDefaultOrder.objects.create(dop=d.dop,product=oredit)

                                sum += (i.product.price + sumdops) * i.count
                            # sum = sum - (sum * (s/100))
                        order.price = sum
                        order.save()

                    # price = request.GET['price']
                    # Configuration.account_id = "847744"
                    # Configuration.secret_key = "live_Wj6HlCC7fGveqz3uX251RlIWxD3ZY66eJ7S_2YWnj-0"
                    # idempotence_key = uuid.uuid4()
                    # red = "https://toopizzabrothers.ru/confirmpay/?id="+str(idempotence_key)
                    # payment = Payment.create({
                    #     "amount": {
                    #     "value": price,
                    #     "currency": "RUB"
                    #     },
                    #     "payment_method_data": {
                    #     "type": "bank_card"
                    #     },
                    #     "confirmation": {
                    #     "type": "redirect",
                    #     "return_url": red
                    #     },
                    #     "description": "Заказ №72"
                    # }, idempotence_key)
                    # order.idd = idempotence_key
                    # order.save()
                    # confirmation_url = payment.confirmation.confirmation_url
                    print('400')
                    return HttpResponse('200')
                else:
                    return HttpResponse('400. Сумма меньше чем у области доставки')
            else:
                return HttpResponse('400. '+i)
        return HttpResponse(a)
    else:
        return HttpResponse('400. Ошибка запроса')



def check_address_in(request):
    if request.method == 'GET':
        street = request.GET['street']
        house = request.GET['house']
        coordinates = client.coordinates("Ярославль "+street+" "+house)
        listshops = []
        closest = 0
        minn = -1
        for i in Shop.objects.all():
            itemc = client.coordinates("Ярославль "+ i.street +" "+ i.house)
            # print(coordinates,itemc)
            f1 = itemc[0]
            f2 = coordinates[0]
            l1 = itemc[1]
            # print(type(l1))
            l2 = coordinates[1]
            form = ((1-math.cos(2*(f2-f1)))/2)/2
            form1 = ((1-math.cos(2*(l2-l1)))/2)/2
            d = 2*6371 * numpy.arcsin(math.sqrt(form + math.cos(f1) * math.cos(f2) * form1))
            print(d,i.street)
            if minn == -1:
                minn = d
                closest = i.pk
            elif d < minn:
                minn = d
                closest = i.pk
            listshops.append([d,i.pk])
        shop = Shop.objects.get(pk = closest)
        print(shop.street)
        checktime = False
        moscow_time = datetime.now(pytz.timezone('Europe/Moscow')).time()
        day = datetime.weekday(datetime.now(pytz.timezone('Europe/Moscow')))
        if day == 0:
            shopopen = shop.open
            shopclose = shop.close
        if day == 1:
            shopopen = shop.open2
            shopclose = shop.close2
        if day == 2:
            shopopen = shop.open3
            shopclose = shop.close3
        if day == 3:
            shopopen = shop.open4
            shopclose = shop.close4
        if day == 4:
            shopopen = shop.open5
            shopclose = shop.close5
        if day == 5:
            shopopen = shop.open6
            shopclose = shop.close6
        if day == 6:
            shopopen = shop.open7
            shopclose = shop.close7


        print(moscow_time,shopopen,shopclose)
        if shopopen < moscow_time and (moscow_time < shopclose and moscow_time < datetime(2000,1,1,23,59).time()):
            checktime = True
            print('Пиццерия  открыта')
            f = requests.get(settings.SITE_URL+shop.zone.url)
            # print(f.text)
            totalarr = {}
            a = re.findall('<Placemark>(.*?)</Placemark>',f.text,re.DOTALL)
            for i in a:
                total = int(i.split('<![CDATA[')[1].split(']]></description>')[0])
                # print(total)
                coordinatesarr = re.findall('<coordinates>(.*?)</coordinates>',i,re.DOTALL)[0].split(',')
                coordinatesarr.insert(0,'%s %s'%(coordinatesarr[-1],coordinatesarr[0]))
                coordinatesarr.pop(1)
                coordinatesarr.pop(-1)
                coordinatesarr.append(coordinatesarr[0])
                newarr = []
                for b in coordinatesarr:
                    a = b.split(' ')
                    newarr.append([float(a[0]),float(a[1])])
                totalarr.update({str(total):newarr})
                # a = is_point_in_path(coordinates[0],coordinates[1],newarr)
            # print(totalarr)
            return render(request,'main/addressresponse.html',context={'shop':shop,'yandexkey':yandexkey,'totalarr':'%s'%totalarr,'x':coordinates[1],'y':coordinates[0]})
        else:
            checktime = False
            print('Пиццерия закрыта')
            return render(request,'main/addressresponseerr.html',context={'message':'Пиццерия закрыта'})
        print(moscow_time,shopclose,shopopen)
        print(checktime)
        # print(listshops)
    return HttpResponse(True)


def add_to_cart_product_app(request):
    if request.method == 'GET':
        try:
            cart =UserLoggined.objects.get(device=request.GET['device'])
        except:
            cart =UserLoggined.objects.create(device=request.GET['device'])
        size = request.GET['size']
        idd = int(request.GET['id'])
        count = request.GET['count']
        price = request.GET['price']
        p = ProductToCart.objects.create(product=Product.objects.get(pk=idd), count=count, cart=cart)
        if request.GET['dops'] != '':
            dops = request.GET['dops'].split(';')
            for i in dops:
                if i != ' ' or i!='':
                    print(i.strip())
                    DopToProductCart.objects.create(dop=Dops.objects.get(title = i.strip()),product=p)
        return HttpResponse(str(p.pk))
    else:
        return HttpResponse(400)



def add_to_cart_default_app(request):
    if request.method == 'GET':
        try:
            cart =UserLoggined.objects.get(device=request.GET['device'])
        except:
            cart =UserLoggined.objects.create(device=request.GET['device'])
        count = 1
        product = DefaultProduct.objects.get(pk=request.GET['id'])
        p = DefaultProductToCart.objects.create(cart=cart,product=product,count=count)
        if request.GET['dops'] != '':
            dops = request.GET['dops'].split(';')
            for i in dops:
                if i != ' ' or i!='':
                    print(i.strip())
                    DopToDefaultProductToCart.objects.create(dop=Dops.objects.get(title = i.strip()),product=p)

        return HttpResponse(str(p.pk))
    else:
        return HttpResponse(400)


def saveaddress(request):
    if request.method == 'GET':
        street = request.GET['street']
        house = request.GET['house']
        apartament = request.GET['apartament']
        enter = request.GET['enter']
        floor = request.GET['floor']
        code = request.GET['code']
        name = request.GET['name']
        comment = request.GET['comment']
        user = UserLoggined.objects.get(device=request.GET['device'])
        user.street = street
        user.house = house
        user.apartament = apartament
        user.enter = enter
        user.code = code
        user.floor = floor
        user.address_name = name
        user.address_comment = comment
        user.delivery_choice = True
        user.save()
    return HttpResponse(200)

def logout(request):
    if request.method == 'GET':
        a = request.GET['device']
        user = UserLoggined.objects.get(device=a)
        user.loggined = False
        user.save()
    return HttpResponse(200)

def promocode_to_cart(request):
    if request.method == 'GET':
        try:
            device = request.GET['device']
            promocode = Promocode.objects.get(title = request.GET['promocode'])
            user = UserLoggined.objects.get(device = device)
            try:
                a = PromocodeToCart.objects.get(cart=user)
                a.promocode = promocode
                a.save()
            except:
                a = PromocodeToCart.objects.create(cart = user,promocode=promocode)
            return HttpResponse(200)
        except:
            return HttpResponse(400)
    return HttpResponse(200)

def checkpromocade(request):
    if request.method == 'GET':
        device = request.GET['device']
        user = UserLoggined.objects.get(device = device)
        try:
            a = PromocodeToCart.objects.get(cart=user)
            return HttpResponse(a.promocode.sale)
        except:
            return HttpResponse(400)
    return HttpResponse(200)

def del_from_cart_app(request):
    if request.method == 'GET':
        # try:
        #     cart =UserLoggined.objects.get(device=request.GET['device'])
        # except:
        #     cart =UserLoggined.objects.create(device=request.GET['device'])

        idd = request.GET['id']
        ProductToCart.objects.get(pk=idd).delete()
        return HttpResponse(200)
    else:
        return HttpResponse(400)

def del_from_cart_default_app(request):
    if request.method == 'GET':
        # try:
        #     cart =UserLoggined.objects.get(device=request.GET['device'])
        # except:
        #     cart =Cart.objects.create(device=request.GET['device'])

        idd = request.GET['id']
        DefaultProductToCart.objects.get(pk=idd).delete()
        return HttpResponse(200)
    else:
        return HttpResponse(400)


def change_item_cart_app(request):
    if request.method == 'GET':
        idd = request.GET['id']
        pm = request.GET['pm']
        print(request.GET)
        print(idd)
        if pm == '+':
            a = ProductToCart.objects.get(pk=idd)
            a.count += 1
            a.save()
        elif pm =='-':
            a = ProductToCart.objects.get(pk=idd)
            a.count -= 1
            a.save()
        return HttpResponse(200)
    else:
        return HttpResponse(400)


def change_item_cart_default_app(request):
    if request.method == 'GET':
        idd = request.GET['id']
        pm = request.GET['pm']
        if pm == '+':
            a = DefaultProductToCart.objects.get(pk=idd)
            a.count += 1
            a.save()
        elif pm =='-':
            a = DefaultProductToCart.objects.get(pk=idd)
            a.count -= 1
            a.save()
        return HttpResponse(200)
    else:
        return HttpResponse(400)

def confirmpromocode_app(request):
    
    if request.method == 'GET':
        try:
            cart =UserLoggined.objects.get(device=request.GET['device'])
        except:
            cart =UserLoggined.objects.create(device=request.GET['device'])
        promocode = request.GET['promocode']
        try:
            PromocodeToCart.objects.create(cart=cart,promocode=Promocode.objects.get(title=promocode))
            return HttpResponse(200)
        except:
            return HttpResponse(400)
    else:
        return HttpResponse(400)


def send_code_app(request):
    # account_sid = 'AC7664421d899b8eb956b069c50f74ac4f' 
    # auth_token = '1b23b7b7353bb2b24fdfd9fae8bbbd1a' 
    # client = Client(account_sid, auth_token) 
    mes = request.GET['code'] + ' - code'
    ph = request.GET['phone'].replace(' ','').replace(')','').replace('(','').replace('-','')
    # message = client.messages.create(  
    #                             messaging_service_sid='MG2fda281b210ddb7b41e0319fa199e40f', 
    #                             body=mes,      
    #                             to=ph 
    #                         ) 
    ur = 'https://smsc.ru/sys/send.php?login=David1234&psw=20012004David&phones='+ ph +'&mes='+ mes
    requests.get(ur)






def commentorderapp(request):
    if request.method == 'GET':
        try:
            cart =UserLoggined.objects.get(device=request.GET['device'])
        except:
            cart =UserLoggined.objects.create(device=request.GET['device'])
        # a = User.objects.get(userame = UserLoggined.objects.get(device=request.GET['device']).phone)
        commentation = request.GET['commentation']
        raiting_one = request.GET['raiting_one']
        raiting_two = request.GET['raiting_two']
        raiting_three = request.GET['raiting_three']
        raiting_four = request.GET['raiting_four']
        Comment.objects.create(order=Order.objects.get(pk=int(request.GET['id'])),commentation=commentation,raiting_one=raiting_one,raiting_two=raiting_two,raiting_three=raiting_three,raiting_four=raiting_four,user=User.objects.get(username = UserLoggined.objects.get(device=request.GET['device']).phone))
        z = Order.objects.get(pk=int(request.GET['id']))
        z.commented = True
        z.save()
        return HttpResponse(200)
    else:
        return HttpResponse(400)

def get_user_phone(request):
    if request.method == 'GET':
        a = UserLoggined.objects.get(device=request.GET['device'])
        return HttpResponse(a.phone.replace(' ','').replace(')','').replace('(','').replace('-',''))

def get_user_order_active(request):
    if request.method == 'GET':
        b = User.objects.get(username=request.GET['phone'].replace('%2B','+').replace(' ','').replace(')','').replace('(','').replace('-',''))
        c = Order.objects.filter(user=b,status='Активный')
        qs_json = serializers.serialize('json', c)
        return HttpResponse(qs_json, content_type='application/json')



def get_total_cart(request):
    if request.method == 'GET':
        try:
            cart =UserLoggined.objects.get(device=request.GET['device'])
        except:
            cart =UserLoggined.objects.create(device=request.GET['device'])
        a = ProductToCart.objects.filter(cart=cart)
        f = DefaultProductToCart.objects.filter(cart=cart)
        try:
            prom = PromocodeToCart.objects.filter(cart=cart).last()
            s = prom.promocode.sale
            sum = 0
            for i in a:
                # sum += i.product.price * i.count
                sumdops = 0
                dops = DopToProductCart.objects.filter(product=i)
                for d in dops:
                    sumdops += d.dop.price
                sum += (i.product.price + sumdops) * i.count
            for i in f:
                sum += i.product.price * i.count
            sum = sum - (sum * (s/100))
            return HttpResponse(int(sum))
        except:
            sum = 0
            for i in a:
                sumdops = 0
                dops = DopToProductCart.objects.filter(product=i)
                for d in dops:
                    sumdops += d.dop.price
                sum += (i.product.price + sumdops) * i.count
            for i in f:
                sum += i.product.price * i.count
            return HttpResponse(int(sum))


def check_loggined(request):
    if request.method == 'GET':
        try:
            a = UserLoggined.objects.get(device=request.GET['device'])
        except:
            a = UserLoggined.objects.create(device=request.GET['device'])
        return JsonResponse({'loggined':str(a.loggined),'phone':a.phone,'name':a.name,'deviverchoice':a.delivery_choice})
    return HttpResponse(200)
def check_loggined_cart(request):
    if request.method == 'GET':
        try:
            a = UserLoggined.objects.get(device=request.GET['device'])
        except:
            a = UserLoggined.objects.create(device=request.GET['device'])
        if ProductToCart.objects.filter(cart=a).first() or DefaultProductToCart.objects.filter(cart=a).first():
            return JsonResponse({'loggined':str(a.loggined),'phone':a.phone,'name':a.name})
        else:
            return JsonResponse({'loggined':'false','phone':a.phone,'name':a.name})

    return HttpResponse(200)

def check_user(request):
    try:
        a = UserLoggined.objects.get(phone=request.GET['phone'].replace('+',''))
        return HttpResponse(200)
    except:
        return HttpResponse(400)
def get_loggin(request):
    if request.method == 'GET':
        # try:
        #     b = User.objects.get(username=request.GET['phone'].replace(' ','').replace(')','').replace('(','').replace('-',''))
        # except:
        #     b = User.objects.create_user(username='+'+request.GET['phone'].replace(' ','').replace(')','').replace('(','').replace('-',''),password=USER_PASSWORD)

        try:
            a = UserLoggined.objects.get(phone=request.GET['phone'])
            a.loggined = True
            a.device = request.GET['device']
            a.save()
            return request.GET['phone']
        except:
            # a = UserLoggined.objects.create(device=request.GET['device'],phone=request.GET['phone'].replace(' ','').replace(')','').replace('(','').replace('-',''))
            return HttpResponse(400)
        # a.loggined = True
        # a.phone = request.GET['phone'].replace(' ','').replace(')','').replace('(','').replace('-','')
        # a.save()
        # return HttpResponse(200)
    return HttpResponse(400)

def register_user(request):
    if request.method == 'GET':
        try:
            a = UserLoggined.objects.create(name=request.GET['name'],phone=request.GET['phone'],device=request.GET['device'],birthday=request.GET['birthday'],loggined=True)
            return HttpResponse(200)
        except:
            return HttpResponse(400)
    else:
        return HttpResponse(400)


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]
















# ViewSets define the view behavior.
class NewsViewSet(generics.ListAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer


# ViewSets define the view behavior.
class ProductViewSet(generics.ListAPIView):
    queryset = ProductGroup.objects.all()
    serializer_class = ProductSerializer


class ShopsViewSet(generics.ListAPIView):
    queryset = Shop.objects.all()
    serializer_class = ShopsSerializer


# ViewSets define the view behavior.
class DopsViewSet(generics.ListAPIView):
    queryset = Dops.objects.all()
    serializer_class = DopsSerializer



# ViewSets define the view behavior.
class ProductToCartViewSet(generics.ListAPIView):
    # queryset = Product.objects.all()
    serializer_class = ProductToCartSerializer

    def get_queryset(self):
        """
        This view should return a list of all the purchases for
        the user as determined by the username portion of the URL.
        """
        device = self.kwargs['device']
        return ProductToCart.objects.filter(cart__device = device)


# ViewSets define the view behavior.
class ProductToCartDefaultViewSet(generics.ListAPIView):
    # queryset = Product.objects.all()
    serializer_class = ProductToCartDefaultSerializer

    def get_queryset(self):
        """
        This view should return a list of all the purchases for
        the user as determined by the username portion of the URL.
        """
        device = self.kwargs['device']
        return DefaultProductToCart.objects.filter(cart__device = device)

class UserLogginedViewSet(generics.ListAPIView):
    # queryset = Product.objects.all()
    serializer_class = UserLogginedSerializer

    def get_queryset(self):
        """
        This view should return a list of all the purchases for
        the user as determined by the username portion of the URL.
        """
        device = self.kwargs['device']
        return UserLoggined.objects.filter(device = device)



class OrderViewSet(generics.ListAPIView):
    # queryset = Product.objects.all()
    serializer_class = OrderSerializer

    def get_queryset(self):
        device = self.kwargs['phone']
        return Order.objects.filter(Q(status='Активный',user__username = device) | Q(status='Обрабатывается',user__username = device))




# class OrderViewSetOne(generics.ListAPIView):
#     # queryset = Product.objects.all()
#     serializer_class = OrderSerializer

#     def get_queryset(self):
#         device = self.kwargs['phone']
#         return Order.objects.filter(user__username = device,status='Завершенный')


class OrderViewSetOne(generics.ListAPIView):
    # queryset = Product.objects.all()
    serializer_class = OrderSerializer

    def get_queryset(self):
        device = self.kwargs['device']
        return Order.objects.filter(user__device = device)


class CategoriesViewSet(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoriesSerializer



