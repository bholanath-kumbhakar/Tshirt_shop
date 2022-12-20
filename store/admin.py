from django.contrib import admin
from store.models import *
from django.utils.html import format_html
# Register your models here.


class sizevarientconfig(admin.TabularInline):
    model=SizeVarient

class Tshirtconfig(admin.ModelAdmin):
    inlines=[sizevarientconfig]
    list_display=['get_image','name','discount']
    list_editable=['discount']
    list_display_links=['name']
    list_per_page=5
    
    def get_image(self,obj):
        return format_html(f"""<a href="{obj.image.url}" target="_blank"> <img height=50px src="{obj.image.url}" /> </a>""")


class Cartconfig(admin.ModelAdmin):

    fieldsets=(
        ("cart info",{"fields" : ('user','tshirt','size','quantity')}),
    )
    list_display=['quantity','size','tshirt','user']

    readonly_fields=['quantity','size','user','tshirt']

    def size(self,obj):
        return obj.sizevarient.size
        
    def tshirt(self,obj):
        tshirt_id=obj.sizevarient.tshirt.id
        return format_html(f'<a href=/admin/store/tshirt/{tshirt_id}/change/>{obj.sizevarient.tshirt.name}</a>')


class Orderconfig(admin.ModelAdmin):

    list_display=['user','shipping_address','phone','date','order_status']
    readonly_fields=['user','shipping_address','phone','date','payment_method','total','payment']

    def payment(sef,obj):
        payment_id=obj.payment_set.all()[0].id
        return format_html(f'<a href=/admin/store/payment/{payment_id}/change/>Click For Payment Info</a>')


admin.site.register(Tshirt,Tshirtconfig)
admin.site.register(Brand)
admin.site.register(NeckType)
admin.site.register(Color)
admin.site.register(IdealFor)
admin.site.register(Occasion)
admin.site.register(Sleeve)
admin.site.register(Cart,Cartconfig)
admin.site.register(Payment)
admin.site.register(Order,Orderconfig)
admin.site.register(OrderItem)




