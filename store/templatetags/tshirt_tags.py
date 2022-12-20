from django import template
from math import floor
register = template.Library()


@register.simple_tag
def cart_sale_price(price,discount):
    return floor(price-(price * discount/100))   

@register.filter
def cart_total_price(cart):
    total=0
    for c in cart:
        price=c.get('size').price
        discount=c.get('tshirt').discount
        sale_price=cart_sale_price(price,discount)
        total_of_single_tshirt=sale_price * c.get('quantity')
        total=total+total_of_single_tshirt
    return total

@register.simple_tag
def min_price(tshirt):
    size=tshirt.sizevarient_set.all().order_by('price').first()
    return size.price

@register.simple_tag
def sale_price(tshirt):
    price=min_price(tshirt)
    discount=tshirt.discount
    return floor(price-(price * discount/100))    


@register.simple_tag
def multiply(a,b):
    return a*b

@register.simple_tag
def cal_sale_price(price,discount):
    return floor(price-(price * discount/100))    


