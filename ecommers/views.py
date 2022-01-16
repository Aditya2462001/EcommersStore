from django.shortcuts import redirect, render
from django.http.response import HttpResponse, JsonResponse,HttpResponseBadRequest
from collections import namedtuple
import razorpay
from django.contrib import messages
from django.conf import settings
from .models import Cart, Category, Customer, ProductBooking, ProductRequest, Products
from .form import ProductForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login ,logout
from django.views.decorators.csrf import csrf_exempt
from rest_framework import routers, serializers, viewsets
from django.template.loader import render_to_string

from django.db.models import Q
import pdfkit
import os
from django.template.loader import get_template 



# payment authorization 

razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))


def Home(request):
    customer = None
    carts = None
    cart_count =None
    prod = []
    category = Category.objects.get(name = 'Programming')
    programming_product = Products.objects.filter(category = category.id)
    products = Products.objects.all()
    category = Category.objects.get(name = 'Love')
    love_books = Products.objects.filter(category = category.id)
    category = Category.objects.get(name = 'Biography')
    biography_books = Products.objects.filter(category = category.id)
    categories = Category.objects.all()
    if request.user.is_active:
        if Customer.objects.filter(user = request.user).exists():
            customer = Customer.objects.get(user = request.user)
            carts = Cart.objects.filter(customer = customer,booked = False)
            cart_count = len(carts)
            if cart_count == 0:
                carts = None
    
    for c in categories:
        if Products.objects.filter(category = c.id).exists():
            prod.append(Products.objects.filter(category = c.id).first())

    
    print(customer)

    context = {
        'products':products,
        'customer':customer,
        'categorires':categories,
        'love_books':love_books,
        'programming_books':programming_product,
        'carts':carts,
        'cart_count':cart_count,
        'best_seller':prod,
        'biography_books':biography_books
    }
    return render(request,'index.html',context)

# =========================== search product ==============================
def Search(request):
    search = request.GET.get('search')
    print(search)
    customer = None
    carts = None
    cart_count = None
    if request.user.is_active:
        if Customer.objects.filter(user = request.user).exists():
            customer = Customer.objects.get(user = request.user)
            carts = Cart.objects.filter(customer = customer,booked = False)
            cart_count = len(carts)
            if cart_count == 0:
                carts = None
    products = Products.objects.filter(Q(product_name__icontains = search) | Q(product_desc__icontains = search) | Q(category__name__icontains = search))

    categories = Category.objects.filter(Q(name__icontains = search))
    

    print(products)
    
    context = {
        'products':products,
        'customer':customer,
        'carts':carts,
        'cart_count':cart_count,
        'categories':categories,
        'search':search
    }
    return render(request,'search-result.html',context)


# ============================ filters ===================================
@csrf_exempt
def Filters(request):
    if request.method == 'POST':
        id_list = []
        options = request.POST.get('options')
        print(options)
        if options == 'No':
            products = Products.objects.all()
        else:
            options = options.split(',')
            categories = Category.objects.filter(name__in = list(options))
            for cat in categories:
                id_list.append(cat.id)

            products = Products.objects.filter(category__in= list(id_list))
        
        context = {
            'products':products
        }

        product_string = render_to_string('filter.html',context)

        return JsonResponse({'data':product_string})

    

# ============================ categories product =========================

def GetProductByCategory(request,category):
    customer = None
    carts = None
    cart_count = None
    categories = Category.objects.all()
    category = Category.objects.get(name = category)
    products = Products.objects.filter(category = category)
    if request.user.is_active:
        if Customer.objects.filter(user = request.user).exists():
            customer = Customer.objects.get(user = request.user)
            carts = Cart.objects.filter(customer = customer,booked = False)
            cart_count = len(carts)
            if cart_count == 0:
                carts = None

    context = {
        'products':products,
        'customer':customer,
        'carts':carts,
        'cart_count':cart_count,
        'category':category,
        'categories':categories
    }
    return render(request,'category-product.html',context)


# ============================ all categories =============================

def AllCategories(request):
    customer = None
    carts = None
    cart_count =None
    categories = Category.objects.all()
    if request.user.is_active:
        if Customer.objects.filter(user = request.user).exists():
            customer = Customer.objects.get(user = request.user)
            carts = Cart.objects.filter(customer = customer,booked= False)
            cart_count = len(carts)
            if cart_count == 0:
                carts = None

    context = {
        'categories':categories,
        'customer':customer,
        'carts':carts,
        'cart_count':cart_count
    }

    return render(request,'all-categories.html',context)

# ============================== all Product ==============================
def AllProducts(request):
    customer = None
    carts = None
    cart_count =None
    products = Products.objects.all()
    categories = Category.objects.all()
    if request.user.is_active:
        if Customer.objects.filter(user = request.user).exists():
            customer = Customer.objects.get(user = request.user)
            carts = Cart.objects.filter(customer = customer,booked = False)
            cart_count = len(carts)
            if cart_count == 0:
                carts = None

    context = {
        'products':products,
        'customer':customer,
        'categories':categories,
        'cart':carts,
        'cart_count':cart_count
    }
    return render(request,'all-products.html',context)



# =============================== view Products ===========================

def ViewProduct(request,slug):
    cart_count = 0
    carts = None
    customer = None
    product = Products.objects.get(product_slug = slug)
    if request.user.is_active:
        if Customer.objects.filter(user = request.user).exists():
            customer = Customer.objects.get(user = request.user)
            carts = Cart.objects.filter(customer = customer,booked = False)
            cart_count = len(carts)
            if cart_count == 0:
                carts = None

    products = Products.objects.filter(category = product.category)[:5]

    context = {
        'product':product,
        'carts':carts,
        'cart_count':cart_count,
        'products':products
    }
    return render(request,'product.html',context)

# ========================== view Cart =====================================

def ViewCart(request):
    customer = None
    carts = None
    total_pay = 0
    if request.user.is_active:
        if Customer.objects.filter(user = request.user).exists():
            customer = Customer.objects.get(user = request.user)
            carts = Cart.objects.filter(customer = customer,booked = False)
            cart_count = len(carts)
            if cart_count == 0:
                return redirect('/')
            for c in carts:
                pro = Products.objects.get(id = c.product.id)
                total_pay += (c.quantity * pro.selling_rate)
            print(total_pay)
    
        context = {
            'customer':customer,
            'carts':carts,
            'cart_count':cart_count,
            'total_pay':total_pay
        }
        return render(request,'cart.html',context)
    else:
        return redirect('/login')

# ========================= Add to cart ==================================
@csrf_exempt
def AddToCart(request):
    if request.user.is_active:
        if Customer.objects.filter(user = request.user).exists():
            customer = Customer.objects.get(user = request.user)
            if request.method == 'POST':
                product_id = request.POST.get('productId')
                customerId = request.POST.get('customerId')

                product = Products.objects.get(id = product_id)


                if int(customer.id) != int(customerId):
                    return JsonResponse({'message':'Your Request is Not Valid.','tag':'fail'})
                
                if Cart.objects.filter(customer = customer,product = product).exists():
                    return JsonResponse({'message':'product is already added.','tag':'fail'})

                cart = Cart(customer = customer,product = product,quantity=1,total_cost = product.selling_rate)
                cart.save()
                cart_list = [cart.product.product_name,cart.product.product_image1.url,cart.product.selling_rate,1,cart.product.product_slug,cart.product.id]
                cart_len = Cart.objects.filter(customer = customer,booked = False)

                return JsonResponse({'message':'product added To Cart.','count':len(cart_len),'cart_list':cart_list,'tag':'success'})
    else:
        return JsonResponse({'message':'You are Not LogIn.','tag':'fail'})

# ========================= increase quantity cart ==================================
@csrf_exempt
def IncreaseQuantityCart(request):
    if request.user.is_active:
        if Customer.objects.filter(user = request.user).exists():
            customer = Customer.objects.get(user = request.user)
            if request.method == 'POST':
                product_id = request.POST.get('productId')
                customerId = request.POST.get('customerId')
                quantity = request.POST.get('quantity')

                product = Products.objects.get(id = product_id)


                if int(customer.id) != int(customerId):
                    return JsonResponse({'message':'Your Request is Not Valid.','tag':'fail'})
                
                if Cart.objects.filter(customer = customer,product = product,booked = False).exists():
                   cart = Cart.objects.get(product = product , customer = customer,booked = False)
                   cart.quantity = quantity
                   cart.total_cost = int(quantity)*int(cart.product.selling_rate)
                   cart.save()

                total_payment = 0
                all_cart = Cart.objects.filter(customer = customer,booked = False)
                for a in all_cart:
                    total_payment += int(a.quantity)*int(a.product.selling_rate)

                return JsonResponse({'message':'product added To Cart.','product_total':cart.total_cost,'total_payment':total_payment,'tag':'success'})
    else:
        return JsonResponse({'message':'You are Not LogIn.','tag':'fail'})


# ========================== remove cart ================================
@csrf_exempt
def RemoveFromCart(request):
    if request.user.is_active:
        if Customer.objects.filter(user = request.user).exists():
            customer = Customer.objects.get(user = request.user)
            if request.method == 'POST':
                product_id = request.POST.get('productId')
                customerId = request.POST.get('customerId')

                product = Products.objects.get(id = product_id)

                if int(customer.id) != int(customerId):
                    return JsonResponse({'message':'Your Request is Not Valid.','tag':'fail'})
                
                if Cart.objects.filter(customer = customer,product = product,booked=False).exists():
                    cart = Cart.objects.get(customer = customer,product = product,booked = False)
                    cart.delete()
                
                else:
                    return JsonResponse({'message':'product is not present.','tag':'fail'})

            
                cart_len = Cart.objects.filter(customer = customer,booked = False)

                return JsonResponse({'message':'Remove from cart.','count':len(cart_len),'tag':'success'})
    else:
        return JsonResponse({'message':'You are Not LogIn.','tag':'fail'})


# ============================= checkout =====================================

def Checkout(request):
    customer = None
    carts = 0
    total_pay = 0
    product_booking = None
    if request.user.is_active:
        if Customer.objects.filter(user = request.user).exists():
            customer = Customer.objects.get(user = request.user)
            carts = Cart.objects.filter(customer = customer,booked = False)
            cart_count = len(carts)
            if cart_count == 0:
                return redirect('/')
            for c in carts:
                pro = Products.objects.get(id = c.product.id)
                total_pay += (c.quantity * pro.selling_rate)
            print(total_pay)

            if request.method == 'POST':
                name = request.POST.get('name')
                number = request.POST.get('number')
                email = request.POST.get('email')
                address = request.POST.get('address')
                country = request.POST.get('country')
                state = request.POST.get('state')
                city = request.POST.get('city')
                pincode = request.POST.get('pincode')
                payment_type = request.POST.get('payment-type')
                total_payment = request.POST.get('total_payment')

                if total_pay == int(total_payment):
                    product_booking = ProductBooking(customer = customer, name = name,email = email,number = number,
                    address=address,country= country,state=state,city = city,pincode = pincode,total_amount = total_pay,
                    payment_type = payment_type)
                    product_booking.save()


                    if payment_type == 'cash-on-delivary':
                        product_booking.payment_status = 'PANDING'
                        product_booking.booking_status = True
                        product_booking.delivary_status = 'PANDING'
                        product_booking.save()


                        for cart in carts:
                            product_booking.cart.add(cart.id)
                            cart.booked = True
                            cart.save()

                        product_booking.save()

                        return redirect('/dashboard')
                    else:
                        for cart in carts:
                            product_booking.cart.add(cart.id)
                        product_booking.save()

                        currency = 'INR'
                        razorpay_order = razorpay_client.order.create(dict(amount=total_pay*100,currency=currency, payment_capture='0'))
                        print(razorpay_order['id'])

                        product_booking.razorpay_orderId = razorpay_order['id']
                        product_booking.save()  
 

                        call_back_url = '/handlerequest/'             
                        
                        context = {
                            'name':name,
                            'number':number,
                            'email':email,
                            'product_booking':product_booking,
                            'order_id':product_booking.razorpay_orderId,
                            'total_amount':product_booking.total_ammount * 100,
                            'razor_payment_id':settings.RAZOR_KEY_ID,
                            'callback_url':call_back_url,
                            'currency':currency
                        }

                        return render(request,'makepayment.html',context)


        context = {
            'customer':customer,
            'carts':carts,
            'cart_count':cart_count,
            'total_pay':total_pay
        }
        return render(request,'checkout.html',context)
    else:
        return redirect('/login')


@csrf_exempt
def HandleRequest(request):
    if request.method == 'POST':
        try:
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }

            product_booking = ProductBooking.objects.get(razorpay_orderId = razorpay_order_id)
            product_booking.razorpay_signature = signature
            product_booking.booking_status = True
            product_booking.save()

            for booking in product_booking.cart.all():
                cart = Cart.objects.get(id = booking.id)
                cart.booked = True
                cart.save()

            result = razorpay_client.utility.verify_payment_signature(params_dict)
            if result is None:
                amount = product_booking.total_ammount*100  # Rs. 200
                try:
                    razorpay_client.payment.capture(payment_id, amount)
                    product_booking.payment_status = 'SUCCESS'
                    product_booking.save()

                    messages.success(request,'Your Payment is Successful.')
                    return redirect('/dashboard')
                except:
                    product_booking.payment_status = 'FAIL'
                    product_booking.save()
                    messages.success(request,'Your Payment is FAIL.')
                    return redirect('/dashboard')
            else:
                product_booking.payment_status = 'FAIL'
                product_booking.save()
                messages.success(request,'Your Payment is FAIL.')
                return redirect('/dashboard')
        except:
            return redirect('/checkout')
    else:
        return redirect('/checkout')



# ========================== Login Customer =====================================

def LoginView(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(username = email,password = password)
        if user is not None:
            if user.is_active:
                login(request,user)
                return redirect('/')
        else:
            messages.info(request,'Cradentials is wrong Try Again !')
            return redirect('/login')

    return render(request,'auth.html',{})


# ============================= Register Customer =================================

def Register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        number = request.POST.get('number')
        password = request.POST.get('password')
        vpassword = request.POST.get('vpassword')

        if password != vpassword:
            messages.info(request,'password Not Matching !')
            print('password not match')
            return render(request,'auth.html',{'name':name,'email':email,'number':number})

        if User.objects.filter(email = email).exists():
            messages.info(request,'User is already exists,try to login !')
            print('username is exist.')
            return redirect('/login')

        user = User(first_name = name,username = email,email= email)
        user.set_password(password)
        user.save()

        customer = Customer(user = user ,name = name,email = email,number = number)
        customer.save()
        print('user is register successfully')

        messages.success(request,'You account is created')
        return redirect('/login')

# ======================= Customer userpanal =================================

def DashBoard(request):
    customer = None
    carts = None
    cart_count = None
    product_booking = None
    prod_count = []
    if request.user.is_active:
        if Customer.objects.filter(user = request.user).exists():
            customer = Customer.objects.get(user = request.user)
            carts = Cart.objects.filter(customer = customer,booked = False)
            cart_count = len(carts)
            if cart_count == 0:
                carts = None
            
            product_booking = ProductBooking.objects.filter(customer = customer,booking_status = True)
            for p_b in product_booking:
                prod_count.append({'id':p_b.id,'product_count':len(p_b.cart.all())})

            recent_booking = ProductBooking.objects.filter(customer = customer,booking_status = True).last()
            recent_booking_product = recent_booking.cart.all()
            

            return_requests = ProductRequest.objects.filter(customer = customer)

        
        context = {
            'customer':customer,
            'carts':carts,
            'cart_count':cart_count,
            'product_booking':product_booking,
            'recent_booking':recent_booking,
            'recent_booking_products':recent_booking_product,
            'prod_count':prod_count,
            'return_request':return_requests
        }
        return render(request,'dashboard.html',context)

    else:
        return redirect('/login')

# ================================ return request ============================
def ReturnReuqest(request):
    customer = None
    product_id = ''
    if request.user.is_active:
        if Customer.objects.filter(user = request.user).exists():
            customer = Customer.objects.get(user = request.user)
            if request.method == 'POST':
                booking_id = request.POST.get('booking_id')
                product_name = request.POST.get('product_name')
                defect_info = request.POST.get('defect_info')


                if not ProductBooking.objects.filter(customer = customer,booking_id = booking_id).exists():
                    messages.info(request,'this booking id does Not exist')
                    return redirect('/dashborad/#return-tab')
                
                p_name = product_name.split(',')
                for p in p_name:
                    if Cart.objects.filter(product__product_name =p, booked = True).exists():
                        cart = Cart.objects.get(product__product_name =p, booked = True)
                        product_id += str(cart.product.id)+","

                return_request = ProductRequest(customer = customer,booking_id = booking_id,product_name = product_name,
                                product_id = product_id,defect_info = defect_info,request_action = 'PANDING',return_payment = 'PANDING',
                                accept_message = 'Your request is panding. Wait for specific action.')

                return_request.save()

                messages.info(request,'your request is sended to us. Wait for result.')


                
    
        return redirect('/dashboard')

    else:
        return redirect('/login')




def EditProfile(request):
    if request.user.is_active:
        if request.method == 'POST':
            name = request.POST.get('name')
            number = request.POST.get('number')
            state = request.POST.get('state')
            city = request.POST.get('city')
            pincode = request.POST.get('pincode')
            address = request.POST.get('address')
            image = request.FILES.get('image')

            customer = Customer.objects.get(user = request.user)
            customer.name = name
            customer.number = number
            customer.state = state
            customer.city = city
            customer.pincode = pincode
            customer.address =  address
            if image is not None:
                customer.image = image
            customer.save()

            messages.success(request,'Your Profile is updated!')

        return redirect('/dashboard/')
    else:
        return redirect('/login')

# ========================= view each booking Details ===========
def EachBookingDetails(request,id):
    customer = None
    carts = None
    product_booking = None
    if request.user.is_active:
        if Customer.objects.filter(user = request.user).exists():
            customer = Customer.objects.get(user = request.user)
            if not ProductBooking.objects.filter(id = id,customer = customer).exists():
                return redirect('/dashboard')
            product_booking = ProductBooking.objects.get(id = id,customer = customer)
            carts = product_booking.cart.all()
            
            
        context = {
            'customer':customer,
            'product_booking':product_booking,
            'carts':carts
        }
        return render(request,'booked-order.html',context)

    else:
        return redirect('/login')


# ============ generate pdf ==================================
def GeneratePdf(request,id):
    if not ProductBooking.objects.filter(id = id).exists():
        return redirect('/dashboard')
    product_booking = ProductBooking.objects.get(id = id)
    carts = product_booking.cart.all()

    context={
        'product_booking':product_booking,
        'carts':carts
    }

    return render(request,'invoice.html',context)




# ===================== logout view ==========================
def LogoutView(request):
    if request.user.is_active:
        logout(request)
    return redirect('/')



# ======================= admin panal ========================
def ProductList(request):
    if request.user.is_active and request.user.is_superuser:
        products = Products.objects.all()

        context = {
            'products':products
        }
        return render(request,'product-list.html',context)
    else:
        return redirect('/')

# add Product View
def AddProduct(request):
    categories = None
    if request.user.is_active:
        if request.user.is_superuser:
            categories = Category.objects.all()
            form = ProductForm()
            if request.method == 'POST':
                form = ProductForm(request.POST or None,request.FILES or None)
                print(form)
                print(form.errors)
                if form.is_valid():
                    prod = form.save(commit = False)
                    prod.save()
                    form.save_m2m()
                    messages.success(request,'Product Added Successfully')
            context = {
                'form':form,
                'categories':categories
            }

            return render(request,'upload-product.html',context)
    
    return redirect('/')



# =============================== contact Us ===========================
def ContactUs(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        number = request.POST.get('number')
        message = request.POST.get('message')

        contact = ContactUs(name = name,email = email,number = number , message = message)
        contact.save()
        messages.success(request,'Your Message is Updated successfully. We Contact You sortly.')

        return redirect('/')

    return render(request,'contact.html',{})


# ================================ About Us =================================
def AboutUs(request):
    return render(request,'about.html',{})



