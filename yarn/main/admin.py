from django.contrib import admin
from django.contrib.admin.options import ModelAdmin, TabularInline, StackedInline
from nested_inline.admin import NestedStackedInline, NestedModelAdmin
from .models import * 

# Register your models here.



class TabularInlineProduct(StackedInline):
    model= Product
    extra=1
    filter_horizontal = ('dops','dopscart','shops')


class AdminProductGroup(admin.ModelAdmin):
    inlines=[TabularInlineProduct, ]


class DefaultProductAdmin(admin.ModelAdmin):
    model = DefaultProduct
    filter_horizontal = ('dops','dopscart','shops')



class AdminPresentPrice(admin.ModelAdmin):
    model = PresentPrice
    filter_horizontal = ('dopscart','shops')


class TabularInlineDopsOrder(NestedStackedInline):
    model= DopToProductOrder
    extra=1


class TabularInlineProductOrder(NestedStackedInline):
    model = OrderProduct
    extra=1
    inlines=[TabularInlineDopsOrder, ]



class TabularInlineDopsOrdertDefault(NestedStackedInline):
    model= DopToProductDefaultOrder
    extra=1


class TabularInlineProductDefaultOrder(NestedStackedInline):
    model = OrderProductDefault
    extra=1
    inlines=[TabularInlineDopsOrdertDefault, ]


class AdminOrder(NestedModelAdmin):
    model = Order
    inlines=[TabularInlineProductOrder,TabularInlineProductDefaultOrder ]
   


admin.site.register(Dops)

# admin.site.register(Cart)
# admin.site.register(ProductToCart)
# admin.site.register(DefaultProduct)
# admin.site.register(News)

# admin.site.register(PromocodeToCart)

# admin.site.register(PromocodeToCart)
# admin.site.register(Masterclass)
# admin.site.register(Comment)

admin.site.register(UserLoggined)

admin.site.register(Promocode)

admin.site.register(News)
admin.site.register(Shop)

admin.site.register(Category)

admin.site.register(DefaultProduct,DefaultProductAdmin)
# admin.site.register(Product)
admin.site.register(ProductGroup,AdminProductGroup)

admin.site.register(Order,AdminOrder)
admin.site.register(PresentPrice,AdminPresentPrice)

admin.site.register(PolicyPage)
admin.site.register(AboutPage)


admin.site.site_header = 'Академия пиццерия'

