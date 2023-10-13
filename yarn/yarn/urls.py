from django.contrib import admin
from django.urls import path,include,re_path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.models import User
from main.models import *
from rest_framework import routers, serializers, viewsets, generics
from main.views import *
from main.serializersmain import *


router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
router = routers.DefaultRouter()
router.register(r'products', ProductViewSet)
# router.register(r'masterclass', MasterclassViewSet)
router.register(r'news', NewsViewSet)
router.register(r'dops', DopsViewSet)
router.register(r'defaultproducts', CategoriesViewSet)
# router.register(r'shops', ShopsViewSet,basename='Shop')

# router.register(r'createdopsapp/(?P<category>.+)/$', CreateDopViewSet.as_view(),basename='createdops')
# router.register(r'createtocartapp/(?P<device>.+)/$', CreateToCartViewSet.as_view(),basename='createtocartapp')
router.register(r'productstocartapp/(?P<device>.+)/$', ProductToCartViewSet.as_view(),basename='productstocartapp')
router.register(r'productstocartdefaultapp/(?P<device>.+)/$', ProductToCartDefaultViewSet.as_view(),basename='productstocartdefaultapp')
router.register(r'ordersapp/(?P<phone>.+)/$', OrderViewSet.as_view(),basename='orderstapp')
router.register(r'userorders/(?P<device>.+)/$', OrderViewSetOne.as_view(),basename='orderstdoneapp')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('main.urls')),
    path('api/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/products/', ProductViewSet.as_view()),
    path('api/defaultproducts/', CategoriesViewSet.as_view()),
    # path('api/masterclass/', MasterclassViewSet.as_view()),
    path('api/news/', NewsViewSet.as_view()),
    path('api/dops/', DopsViewSet.as_view()),
    path('api/shops/', ShopsViewSet.as_view()),

    # path(r'api/createdopsapp/<str:category>/', CreateDopViewSet.as_view()),
    # path(r'api/createtocartapp/<str:device>/', CreateToCartViewSet.as_view()),
    path(r'api/productstocartapp/<str:device>/', ProductToCartViewSet.as_view()),
    path(r'api/user/<str:device>/',UserLogginedViewSet.as_view()),
    path(r'api/productstocartdefaultapp/<str:device>/', ProductToCartDefaultViewSet.as_view()),
    path(r'api/ordersapp/<str:phone>/', OrderViewSet.as_view()),
    path(r'api/userorders/<str:device>/', OrderViewSetOne.as_view()),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# urlpatterns = [
#     path('', include(router.urls)),
#     path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
# ]