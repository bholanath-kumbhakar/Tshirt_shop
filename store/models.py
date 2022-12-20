from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class TshirtProperty(models.Model):
    title=models.CharField(max_length=30,null=False)
    slug=models.CharField(max_length=30,null=True,unique=True)
    def __str__(self):
        return self.title
    class Meta:
        abstract=True

class Occasion(TshirtProperty):
    pass
class IdealFor(TshirtProperty):
    pass
class NeckType(TshirtProperty):
    pass
class Sleeve(TshirtProperty):
    pass
class Brand(TshirtProperty):
    pass
class Color(TshirtProperty):
    pass

class Tshirt(models.Model):
    name=models.CharField(max_length=50,null=True)
    slug=models.CharField(max_length=200,null=False,unique=True)
    description=models.CharField(max_length=500,null=True)
    discount=models.IntegerField(default=0)
    image=models.ImageField(upload_to='images/',null=False)
    occasion=models.ForeignKey(Occasion,on_delete=models.CASCADE)
    brand=models.ForeignKey(Brand,on_delete=models.CASCADE)
    sleeve=models.ForeignKey(Sleeve,on_delete=models.CASCADE)
    neck_type=models.ForeignKey(NeckType,on_delete=models.CASCADE)
    color=models.ForeignKey(Color,on_delete=models.CASCADE)
    idealfor=models.ForeignKey(IdealFor,on_delete=models.CASCADE ,null=True,blank=True)
    def __str__(self) -> str:
        return self.name

class SizeVarient(models.Model):
    SIZES=(
        ('S','small'),
        ('M','medium'),
        ('L','large'),
        ('XL','extra large'),
        ('XXL','extra extra large'),
    )
    price=models.IntegerField(null=False)
    tshirt=models.ForeignKey(Tshirt,on_delete=models.CASCADE)
    size=models.CharField(choices=SIZES,max_length=5)

    def __str__(self):
        return f'{self.size}- {self.tshirt.name}'

class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    sizevarient=models.ForeignKey(SizeVarient,on_delete=models.CASCADE)
    quantity=models.IntegerField(default=1)


class Order(models.Model):
    orderstatus=( 
        ('PENDING',"pending"),
        ('PLACED',"placed"),
        ('CANCELED',"canceled"),
        ('COMPLETED',"completed"),
    )
    paymentmethod=(
        ('COD',"cod"),
        ('ONLINE',"online"),
    )
    order_status=models.CharField(max_length=15,choices=orderstatus)
    payment_method=models.CharField(max_length=15,choices=paymentmethod)
    shipping_address=models.CharField(max_length=100,null=False)
    phone=models.IntegerField(null=False)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    total=models.IntegerField(null=False)
    date=models.DateTimeField(null=False,auto_now_add=True)

class OrderItem(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE)
    tshirt=models.ForeignKey(Tshirt,on_delete=models.CASCADE)
    size=models.ForeignKey(SizeVarient,on_delete=models.CASCADE)
    quantity=models.IntegerField(null=False)
    price=models.IntegerField(null=False)
    date=models.DateTimeField(null=False,auto_now_add=True)

class Payment(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE)
    payment_status=models.CharField(max_length=15,default='FAILED')
    date=models.DateTimeField(null=False,auto_now_add=True)
    payment_id=models.CharField(max_length=60)
    payment_request_id=models.CharField(max_length=60, unique=True,null=False)