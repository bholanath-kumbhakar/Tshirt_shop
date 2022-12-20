from math import floor
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.sessions.models import Session
from django.shortcuts import HttpResponse, HttpResponseRedirect, render, redirect
from django.views import View
from store.forms import CheckoutForm, LoginForm, Userform
from .models import Cart, SizeVarient, Tshirt, Order, OrderItem,Payment,Occasion,IdealFor,NeckType,Brand,Color,Sleeve
from instamojo_wrapper import Instamojo
from django.core.paginator import Paginator
from urllib.parse import urlencode

API_KEY="test_bd12ee81e21968b13d9b606f6b0"
AUTH_TOKEN="test_07720fd6b90dc5cb8f67fca285b"
api = Instamojo(api_key=API_KEY, auth_token=AUTH_TOKEN, endpoint='https://test.instamojo.com/api/1.1/')

# Home view...................................................................

class HomeView(View):
    def get(self, request):

        tshirts=Tshirt.objects.all()
        
        brand=request.GET.get('brand')
        necktype=request.GET.get('necktype')
        color=request.GET.get('color')
        idealfor=request.GET.get('idealfor')
        sleeve=request.GET.get('sleeve')        

        if brand:
            tshirts=tshirts.filter(brand__slug = brand)
        if necktype :
            tshirts=tshirts.filter(neck_type__slug=necktype)
        if color:
            tshirts=tshirts.filter(color__slug=color)
        if idealfor:
            tshirts=tshirts.filter(idealfor__slug=idealfor)
        if sleeve:
            tshirts=tshirts.filter(sleeve__slug=sleeve)
        else:
            tshirts=tshirts.all()

        brands=Brand.objects.all()
        occasions=Occasion.objects.all()
        sleeve=Sleeve.objects.all()
        idealfor=IdealFor.objects.all()
        colors=Color.objects.all()
        necktypes=NeckType.objects.all()
        #pagination.................................
        page=request.GET.get('page')
        if page is None or page == '':
            page=1
        paginator=Paginator(tshirts,6)
        page_obj=paginator.get_page(page)
        
        query=request.GET.copy()
        query['page']=''
        pageurl=urlencode(query)
        
        context={'pageurl':pageurl,'page_obj':page_obj,'brands':brands,'occasions':occasions,'sleeves':sleeve,'idealfor':idealfor,'colors':colors,'necktypes':necktypes,'tshirts':tshirts}
        return render(request, 'store/home.html',context)

# Signp view.............................................................................................


class SignupView(View):

    def get(self, request):
        fm = Userform()
        return render(request, 'store/signup.html', {'form': fm})

    def post(self, request):
        fm = Userform(request.POST)
        if fm.is_valid():
            user = fm.save()
            user.email = user.username
            user.save()
            return HttpResponseRedirect('/login/')
        return render(request, 'store/signup.html', {'form': fm})

# Login view...................................................................................


class LoginView(View):

    def get(self, request):
        fm = LoginForm()
        next_page = request.GET.get('next')
        if next_page is not None:
            request.session['next_page'] = next_page

        return render(request, 'store/login.html', {'form': fm})

    def post(self, request):
        fm = LoginForm(data=request.POST)
        if fm.is_valid():
            un = fm.cleaned_data.get('username')
            ps = fm.cleaned_data.get('password')
            user = authenticate(username=un, password=ps)
            if user:
                login(request, user)
# merging cart to databa........................................
                session_cart = request.session.get('cart')
                if session_cart is None:
                    session_cart = []
                else:
                    for c in session_cart:
                        size = c.get('size')
                        tshirt_id = c.get('tshirt')
                        quantiy = c.get('quantity')
                        cart_obj = Cart()
                        cart_obj.sizevarient = SizeVarient.objects.get(
                            tshirt=tshirt_id, size=size)
                        cart_obj.quantity = quantiy
                        cart_obj.user = user
                        cart_obj.save()
# fetch all cart products ..............................
                session_cart = []
                cart = Cart.objects.filter(user=user)
                for c in cart:
                    obj = {
                        'tshirt': c.sizevarient.tshirt.id,
                        'size': c.sizevarient.size,
                        'quantity': c.quantity
                    }
                    session_cart.append(obj)
                request.session['cart'] = session_cart
                next_page = request.session.get('next_page')
                if next_page is None:
                    next_page = '/'
                return HttpResponseRedirect(next_page)
        return render(request, 'store/login.html', {'form': fm})


# Logout view...........................................................
class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect('/')


# ProductView.............................................................
class ProductView(View):
    def get(self, request, slug):
        tshirt = Tshirt.objects.get(slug=slug)
        size = request.GET.get('size')
        if size is None:
            size_obj = tshirt.sizevarient_set.all().order_by('price').first()
        else:
            size_obj = tshirt.sizevarient_set.get(size=size)
        price = size_obj.price
        sale_price = price-(price * (tshirt.discount/100))
        sale_price = floor(sale_price)
        return render(request, 'store/product_details.html', {'tshirt': tshirt, 'price': price, 'sale_price': sale_price, 'active_size': size_obj})

# Cart view......................................................
class Addto_Cart(View):

    def get(self, request, slug, size):
        user = None
        if request.user.is_authenticated:
            user = request.user
        tshirt = Tshirt.objects.get(slug=slug)
        size_obj = SizeVarient.objects.get(size=size, tshirt=tshirt)

# add tshirt in session user may login or logout
        cart = request.session.get('cart')
        if cart is None:
            cart = []
        flag = True
        for cart_obj in cart:
            t_id = cart_obj.get('tshirt')
            size_temp = cart_obj.get('size')
            if t_id == tshirt.id and size == size_temp:
                flag = False
                cart_obj['quantity'] = cart_obj['quantity']+1
        if flag:
            cart_obj = {
                'tshirt': tshirt.id,
                'size': size,
                'quantity': 1
            }
            cart.append(cart_obj)

# if user logged in cart save to model..............................................

        if user is not None:
            existing = Cart.objects.filter(user=user, sizevarient=size_obj)
            if len(existing) > 0:
                obj = existing[0]
                obj.quantity = obj.quantity+1
                obj.save()
            else:
                c = Cart(user=user, sizevarient=size_obj, quantity=1)
                c.save()

        request.session['cart'] = cart
        return_url = request.GET.get('return_url')
        return redirect(return_url)

# cartview.............................................................................................


class CartView(View):
    def get(self, request):
        cart = request.session.get('cart')
        if cart is None:
            cart = []

        for c in cart:
            tshirt_id = c.get('tshirt')
            tshirt = Tshirt.objects.get(id=tshirt_id)
            size = SizeVarient.objects.get(tshirt=tshirt_id, size=c['size'])
            c['tshirt'] = tshirt
            c['size'] = size

        context = {'cart': cart}
        return render(request, 'store/cart.html', context)
# ....Remove  from session ..........
    def post(self,request):
        cart=request.session.get('cart')
        tshirt_id=request.POST.get('tshirt_id')
        lst=[]
        for i in cart:
            t_id=i.get('tshirt')
            lst.append(t_id)
        delete_index=lst.index(int(tshirt_id))
        del cart[delete_index]
        request.session['cart']=cart
 #.......#remove from base...........................
        user = None
        if request.user.is_authenticated:
            user = request.user
        tshirt=Tshirt.objects.get(id=tshirt_id)
        size=tshirt.sizevarient_set.all()        
        cart_obj=Cart.objects.filter(user=user,sizevarient__in=size)
        cart_obj.delete()
        return HttpResponseRedirect('/cart/')

# orderview......................................................................................

class OrdersView(View):
    def get(self, request):
        orders=Order.objects.filter(user=request.user).order_by('-date').exclude(order_status="PENDING")
        return render(request, 'store/orders.html',{'orders':orders})


# Checkoutview........................................................
class CheckoutView(View):
    def get(self, request):    
        form = CheckoutForm()
        cart = request.session.get('cart')
        if cart is None:
            cart = []
            return HttpResponse('SORRY NO ITEM IN CART')
        for c in cart:
            size_str = c.get('size')
            tshirt_id = c.get('tshirt')
            size_obj = SizeVarient.objects.get(tshirt=tshirt_id, size=size_str)
            c['size'] = size_obj
            c['tshirt'] = size_obj.tshirt
        return render(request, 'store/checkout.html', {'form': form, 'cart': cart})

    def post(self, request):
        user = None
        if request.user.is_authenticated:
            user = request.user
        form = CheckoutForm(request.POST)
        if form.is_valid():
            cart = request.session.get('cart')
            if cart is None:
                cart = []
            for c in cart:
                size_str = c.get('size')
                tshirt_id = c.get('tshirt')
                size_obj = SizeVarient.objects.get(tshirt=tshirt_id, size=size_str)
                c['size'] = size_obj
                c['tshirt'] = size_obj.tshirt
            shipping_address = form.cleaned_data.get('shipping_address')
            phone = form.cleaned_data.get('phone')
            pay_method = form.cleaned_data.get('payment_method')
            total_amount = cart_total_price(cart)
            print(shipping_address, phone, pay_method, total_amount)
            #Saving order..............
            order = Order()
            order.shipping_address = shipping_address
            order.phone = phone
            order.payment_method = pay_method
            order.total = total_amount
            order.order_status = "PENDING"
            order.user = user
            order.save()
            # saving order items
            for c in cart:
                orderitem=OrderItem()
                orderitem.order=order
                size=c.get('size')
                tshirt=c.get('tshirt')
                orderitem.price=floor(size.price-(size.price * tshirt.discount/100))
                orderitem.quantity=c.get('quantity')
                orderitem.tshirt=size.tshirt
                orderitem.size=size
                orderitem.save()
            #creating payment...........

            response = api.payment_request_create(
            amount=order.total,
            purpose='Tshirt Payment',
            send_email=True,
            email="alok92442@gmail.com",
            redirect_url="http://localhost:8000/validate_payment"
            ) 
            payment_request_id=response['payment_request']['id']
            url=response['payment_request']['longurl']
        #    save to payment model..........
            payment=Payment()
            payment.order=order
            payment.payment_request_id=payment_request_id
            payment.save()
            return redirect(url)
        else:
            return redirect('/checkout/')


# utility function...................
def cart_total_price(cart):
    total = 0
    for c in cart:
        price = c.get('size').price
        discount = c.get('tshirt').discount
        sale_price = floor(price-(price * discount/100))
        total_of_single_tshirt = sale_price * c.get('quantity')
        total = total+total_of_single_tshirt
    return total


class Validate_Payment_View(View):
    def get(self,request):
        user = None
        if request.user.is_authenticated:
            user = request.user
        payment_request_id=request.GET.get('payment_request_id')
        payment_id=request.GET.get('payment_id')
        response = api.payment_request_payment_status(payment_request_id, payment_id)
        status=response.get('payment_request').get('payment').get('status')

        if status != "Failed":
            try:
                payment=Payment.objects.get(payment_request_id=payment_request_id)
                payment.payment_id=payment_id
                payment.payment_status=status
                payment.save()

                order=payment.order
                order.order_status='PLACED'
                order.save()

                cart=[]
                request.session['cart']=cart
                Cart.objects.filter(user=user).delete()
                # return HttpResponse('order page')
                return redirect('orders')
            except:
                return render(request, "store/payment_failed.html")
        else:
            return render(request, "store/payment_failed.html")