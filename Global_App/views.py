import json

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from .models import *

# Create your views here.
def index(request):
    product=Product.objects.all().order_by("-id")[:4]
    return render(request,"index.html",{"product":product})

def about(request):
    return render(request,"about.html")
def products(request):
    products = Product.objects.all()
    category = Category.objects.all()
    brand = Brand.objects.all()
    return render(request,"products.html",{"products":products,"category":category,"brand":brand})

def contact(request):
    return render(request,"contact.html")


def GMobile(request):
    return render(request,"GMobile.html")

def check_login(request):
    username=request.POST.get("username")
    password=request.POST.get("password")
    user=authenticate(request,username=username,password=password)
    if user is not None:
        login(request,user)
        return redirect("/dashboard/")
    else:
        return redirect("/GMobile/")

@login_required
def dashboard(request):
    return render(request,"dashboard.html")

def logout_admin(request):
    logout(request)
    return redirect("/GMobile/")

def create_category(request):
    return render(request,"create_category.html")

def save_category(request):
    if request.method == "POST":
        category_name = request.POST.get('categoryName')
        category_slug = request.POST.get('categorySlug')
        category_description = request.POST.get('categoryDescription')

        # Create a new Category object and save it to the database
        new_category = Category(
            name=category_name,
            slug=category_slug,
            description=category_description
        )
        new_category.save()

        return redirect('/manage_category/')


def manage_category(request):
    data=Category.objects.all()
    return render(request,"manage_category.html",{"data":data})
def create_brand(request):
    return render(request,"create_brand.html")
def create_product(request):
    category = Category.objects.all()
    brand = Brand.objects.all()
    return render(request,"create_product.html",{"category":category,"brand":brand})

def save_brand(request):
    if request.method == "POST":
        brand_name = request.POST.get('brandName')
        brand_slug = request.POST.get('brandSlug')
        brand_description = request.POST.get('brandDescription')

        # Create a new Brand object and save it to the database
        new_brand = Brand(
            name=brand_name,
            slug=brand_slug,
            description=brand_description
        )
        new_brand.save()

        # Redirect to a success page or brand list page
        return redirect('/manage_brand/')


def manage_brand(request):
    brands=Brand.objects.all()
    return render(request,"manage_brand.html",{"brands":brands})


def save_product(request):
    if request.method == 'POST':
        product_name = request.POST.get('productName')
        product_slug = request.POST.get('productSlug')
        product_description = request.POST.get('productDescription')
        product_category_id = request.POST.get('productCategory')
        product_brand_id = request.POST.get('productBrand')
        product_price = request.POST.get('productPrice')
        product_stock = request.POST.get('productStock')
        product_active = request.POST.get('productActive')
        product_image = request.FILES.get('productImage')
        keys = request.POST.getlist('keys[]')
        values = request.POST.getlist('values[]')



        try:
            category = Category.objects.get(id=product_category_id)
            brand = Brand.objects.get(id=product_brand_id)

            product = Product(
                name=product_name,
                slug=product_slug,
                description=product_description,
                category=category,
                brand=brand,
                price=product_price,
                stock=product_stock,
                is_active=(product_active == "true"),
                image=product_image,
            )
            product.save()
            for key, value in zip(keys, values):
                ProductAttribute.objects.create(product=product, key=key, value=value)
            messages.success(request, 'Product saved successfully!')
            return redirect('/manage_product/')  # Redirect to the product creation page or another view
        except Category.DoesNotExist:
            messages.error(request, 'Selected category does not exist.')
        except Brand.DoesNotExist:
            messages.error(request, 'Selected brand does not exist.')
        except Exception as e:
            messages.error(request, f'An error occurred: {e}')

    
def manage_product(request):
    products = Product.objects.all()  # Fetch all products from the database
    return render(request, 'manage_product.html', {'products': products})


def add_to_cart(request,slug):
    try:
        uid=request.session['userid']
        pdt=Product.objects.get(slug=slug)
        c,created=Cart.objects.get_or_create(product_id=pdt.id,user_id=uid)
        if not created:
            c.quantity+=1
            c.save()
        else:
            c.quantity=1
            c.save()
        return redirect("/cart/")
    except KeyError:
        pdt = Product.objects.get(slug=slug)
        session_key = request.session.session_key
        if not session_key:
            session_key = request.session.create()
        c, created = Cart.objects.get_or_create(product_id=pdt.id, session_key=session_key)
        if not created:
            c.quantity += 1
            c.save()
        else:
            c.quantity = 1
            c.save()
        return redirect("/cart/")

def cart(request):
    try:
        uid=request.session['userid']
        cart_items=Cart.objects.filter(user=uid)
        cart_total=sum(i.total_price() for i in cart_items)
        quantity_range = range(1, 7)
        return render(request,"cart.html",{"cart_items":cart_items,"cart_total":cart_total,"quantity_range":quantity_range})
    except:
        cart_items=Cart.objects.filter(session_key=request.session.session_key)
        cart_total = sum(i.total_price() for i in cart_items)
        quantity_range = range(1, 7)
        return render(request, "cart.html", {"cart_items": cart_items,"cart_total":cart_total,"quantity_range":quantity_range})

def remove_cart(request,id):
    d=Cart.objects.get(id=id)
    d.delete()
    return redirect("/cart/")


def buy_now(request,slug):
    try:
        f=request.session['userid']
        pdt=Product.objects.get(slug=slug)
        d=User_Ship_Address.objects.filter(user=f)
        if d:
            return render(request,"buy_now.html",{"pdt":pdt,"d":d})
        else:
            return render(request, "buy_now.html", {"pdt": pdt})


    except KeyError:
        print(slug,"buy")
        return render(request,"Login.html",{"slug":slug})

def save_booking(request,slug):
    pdt=Product.objects.get(slug=slug)
    j=User_Ship_Address.objects.filter(user=request.session['userid'])
    if not j.exists():
        v=User_Ship_Address()
        v.user_id=request.session['userid']
        v.firstname=request.POST.get("first_name")
        v.lastname = request.POST.get("last_name")
        v.street_address = request.POST.get("streetaddress")
        v.country=request.POST.get("country")
        v.apartment=request.POST.get("apartment")
        v.city=request.POST.get("city")
        v.zip=request.POST.get("zip")
        v.phone=request.POST.get("phone")
        v.email=request.POST.get("email")
        v.save()
        v1 = Bookings()
        v1.ship_add_id = v.id
        v1.user_id = request.session['userid']
        v1.product_id = pdt.id
        v1.quantity = request.POST.get("quantity")
        v1.total_price = float(request.POST.get("total_price"))
        v1.sub_total = float(request.POST.get("sub_total"))
        v1.status = "Pending"
        v1.save()
    else:
        v1=Bookings()
        v1.ship_add_id=request.POST.get("address")
        v1.user_id=request.session['userid']
        v1.product_id=pdt.id
        v1.quantity=request.POST.get("quantity")
        v1.total_price=float(request.POST.get("total_price"))
        v1.sub_total=float(request.POST.get("sub_total"))
        v1.status="Pending"
        v1.save()
    return redirect("/")


def save_reg(request):
    reg=Registration()
    reg.name=request.POST.get("username")
    reg.mobile=request.POST.get("mobile")
    reg.email=request.POST.get("email")
    reg.password=request.POST.get("password")

    reg.save()
    slug=request.POST.get("slug")
    return render(request,"Login.html",{"slug":slug})

def Login(request):
    return render(request,"Login.html")

def login_check(request):
    slug = request.POST.get("slug")
    print(slug,"slug")
    email=request.POST.get("email")
    password=request.POST.get("password")
    if Registration.objects.filter(email=email,password=password).exists():
        sess_id=Registration.objects.get(email=email,password=password)
        request.session['userid']=sess_id.id
        next_url = request.POST.get("next") or request.GET.get("next")
        print(next_url,"hh")
        cart=Cart.objects.filter(session_key=request.session.session_key)
        cart.update(user_id=request.session['userid'])
        
        if next_url:
            return HttpResponseRedirect(next_url)
        else:
            return redirect("buy_now",slug=slug)
    else:
        return render(request, "login.html", {"error": "Invalid email or password"})

def logout_user(request):
    del request.session['userid']
    return redirect("/")



@csrf_exempt
def update_cart_quantity(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        cart_id = data.get('cart_id')
        quantity = data.get('quantity')

        try:
            cart_item = Cart.objects.get(id=cart_id)
            cart_item.quantity = quantity
            cart_item.save()
            return JsonResponse({'success': True}, status=200)
        except Cart.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Cart item not found.'}, status=404)
    return JsonResponse({'success': False, 'error': 'Invalid request method.'}, status=400)

def edit_category(request,id):
    f=Category.objects.get(id=id)
    return render(request,"edit_category.html",{"f":f})


def update_category(request,id):
    k=Category.objects.get(id=id)
    k.name=request.POST.get("categoryName")
    k.slug=request.POST.get("categorySlug")
    k.description=request.POST.get("categoryDescription")
    k.save()
    return redirect("/manage_category/")

def delete_category(request,id):
    k=Category.objects.get(id=id)
    k.delete()
    return redirect("/manage_category/")

def edit_brand(request,id):
    h=Brand.objects.get(id=id)
    return render(request,"edit_brand.html",{"h":h})
def update_brand(request,id):
    f=Brand.objects.get(id=id)
    try:
        f.logo=request.FILES.get('brandLogo')
        f.name=request.POST.get("brandName")
        f.slug=request.POST.get("brandSlug")
        f.description=request.POST.get("brandDescription")
        f.save()
        return redirect("/manage_brand/")
    except:
        f.name = request.POST.get("brandName")
        f.slug = request.POST.get("brandSlug")
        f.description = request.POST.get("brandDescription")
        f.save()
        return redirect("/manage_brand/")


def edit_product(request,id):
    b=Product.objects.get(id=id)
    attr=ProductAttribute.objects.filter(product=id)
    categories=Category.objects.all()
    brands=Brand.objects.all()
    return render(request,"edit_product.html",{"b":b,"attr":attr,"categories":categories,"brands":brands})


def update_product(request,id):
    k=Product.objects.get(id=id)
    product_name = request.POST.get('productName')
    product_slug = request.POST.get('productSlug')
    product_description = request.POST.get('productDescription')
    product_category_id = request.POST.get('productCategory')
    product_brand_id = request.POST.get('productBrand')
    product_price = request.POST.get('productPrice')
    product_stock = request.POST.get('productStock')
    product_active = request.POST.get('productActive')
    product_image = request.FILES.get('productImage')

    try:

        category = Category.objects.get(id=product_category_id)
        brand = Brand.objects.get(id=product_brand_id)
        if product_image:
            k.name=product_name
            k.slug=product_slug
            k.description=product_description
            k.category=category
            k.brand=brand
            k.price=product_price
            k.stock=product_stock
            k.is_active=(product_active == "true")
            k.image=product_image
            k.save()
            ProductAttribute.objects.filter(product=k).delete()  # Clear existing attributes
            keys = request.POST.getlist('keys[]')
            values = request.POST.getlist('values[]')
            for key, value in zip(keys, values):
                ProductAttribute.objects.create(product=k, key=key, value=value)
            messages.success(request, 'Product saved successfully!')
            return redirect('/manage_product/')
        else:
            k.name = product_name
            k.slug = product_slug
            k.description = product_description
            k.category = category
            k.brand = brand
            k.price = product_price
            k.stock = product_stock
            k.is_active = (product_active == "true")
            k.save()
            messages.success(request, 'Product saved successfully!')
            ProductAttribute.objects.filter(product=k).delete()  # Clear existing attributes
            keys = request.POST.getlist('keys[]')
            values = request.POST.getlist('values[]')
            for key, value in zip(keys, values):
                ProductAttribute.objects.create(product=k, key=key, value=value)

            return redirect('/manage_product/')
    except Category.DoesNotExist:
        messages.error(request, 'Selected category does not exist.')
    except Brand.DoesNotExist:
        messages.error(request, 'Selected brand does not exist.')

def delete_product(request,id):
    g=Product.objects.get(id=id)
    g.delete()
    return redirect("/manage_product/")

def delete_brand(request,id):
    k=Brand.objects.get(id=id)
    k.delete()
    return redirect("/manage_brand/")

def pending_orders(request):
    k=Bookings.objects.filter(status="Pending")
    k1=Multi_Bookings.objects.filter(status="Pending")
    return render(request,"pending_orders.html",{"k":k,"k1":k1})

def status_booking(request,id):
    data=Bookings.objects.get(id=id)
    return render(request,"status_booking.html",{"data":data})

def save_status(request,id):
    f=Bookings.objects.get(id=id)
    f.status=request.POST.get("status")
    f.save()
    return redirect("/pending_orders/")

def cancelled_orders(request):
    k = Bookings.objects.filter(status="Cancel")
    k1 = Multi_Bookings.objects.filter(status="Cancel")
    return render(request, "cancelled_orders.html", {"k": k,"k1":k1})


def completed_orders(request):
    k = Bookings.objects.filter(status="Completed")
    k1 = Multi_Bookings.objects.filter(status="Completed")
    return render(request, "completed_orders.html", {"k": k,"k1":k1})

def enquiries(request):
    return render(request,"enquiries.html")

def save_contact(request):
    g=Contact()
    g.name=request.POST.get("name")
    g.email=request.POST.get("email")
    g.subject=request.POST.get("subject")
    g.message=request.POST.get("message")
    g.save()
    return redirect("/")

def get_product_attributes(request, product_id):
    # Fetch product attributes based on the product ID
    attributes = ProductAttribute.objects.filter(product_id=product_id).values('key', 'value')
    return JsonResponse(list(attributes), safe=False)

def product_single(request,slug):
    pdt=Product.objects.get(slug=slug)
    attributes=ProductAttribute.objects.filter(product=pdt.id)
    related=Product.objects.filter(category=pdt.category.id)
    return render(request,"product_single.html",{"pdt":pdt,"attributes":attributes,"related":related})


def checkout(request):
    try:
        request.session['userid']
        pdt=Cart.objects.filter(session_key=request.session.session_key)
        d = User_Ship_Address.objects.filter(user=request.session['userid'])
        sub_total=sum(i.total_price() for i in pdt)
        return render(request,"checkout.html",{"pdt":pdt,"d":d,"sub_total":sub_total})
    except:
        next_url = "/checkout/"
        return redirect(f"/Login/?next={next_url}")

def save_checkout(request):
    j = User_Ship_Address.objects.filter(user=request.session['userid'])
    if not j.exists():
        v = User_Ship_Address()
        v.user_id = request.session['userid']
        v.firstname = request.POST.get("first_name")
        v.lastname = request.POST.get("last_name")
        v.street_address = request.POST.get("streetaddress")
        v.country = request.POST.get("country")
        v.apartment = request.POST.get("apartment")
        v.city = request.POST.get("city")
        v.zip = request.POST.get("zip")
        v.phone = request.POST.get("phone")
        v.email = request.POST.get("email")
        v.save()
        v1 = Multi_Bookings()
        v1.ship_add_id = v.id
        v1.user_id = request.session['userid']
        v1.total_price = float(request.POST.get("total_price"))
        v1.sub_total = float(request.POST.get("sub_total"))
        v1.status = "Pending"
        v1.save()
        cart=Cart.objects.filter(user=request.session['userid'])
        for i in cart:
            f=Order_Item()
            f.user_id=request.session['userid']
            f.product_id=i.product.id
            f.quantity=i.quantity
            f.book_id=v1.id
            f.save()
        cart.delete()
    else:
        v1 = Multi_Bookings()
        v1.ship_add_id = request.POST.get("address")
        v1.user_id = request.session['userid']
        v1.total_price = float(request.POST.get("total_price"))
        v1.sub_total = float(request.POST.get("sub_total"))
        v1.status = "Pending"
        v1.save()
        cart = Cart.objects.filter(user=request.session['userid'])
        for i in cart:
            f = Order_Item()
            f.user_id = request.session['userid']
            f.product_id = i.product.id
            f.quantity = i.quantity
            f.book_id = v1.id
            f.save()
        cart.delete()
    return redirect("/")

def cancel_m_booking(request,id):
    data=Multi_Bookings.objects.get(id=id)
    data.status="Cancel"
    data.save()
    return redirect("/cancelled_orders/")

def cancel_booking(request,id):
    data=Bookings.objects.get(id=id)
    data.status="Cancel"
    data.save()
    return redirect("/cancelled_orders/")
def status_m_booking(request,id):
    data=Multi_Bookings.objects.get(id=id)
    return render(request,"status_m_booking.html",{"data":data})

def save_m_status(request,id):
    f=Multi_Bookings.objects.get(id=id)
    f.status=request.POST.get("status")
    f.save()
    return redirect("/pending_orders/")

def my_profile(request):
    return render(request,"my_profile.html")

def products_category(request,slug):
    pdt_cat=Product.objects.filter(category__slug=slug)
    category=Category.objects.all()
    brand=Brand.objects.all()
    return render(request,"products_category.html",{"pdt_cat":pdt_cat,"brand":brand,"category":category})

def product_brand(request,slug):
    pdt_brand=Product.objects.filter(brand__slug=slug)
    category=Category.objects.all()
    brand=Brand.objects.all()
    return render(request,"product_brand.html",{"pdt_brand":pdt_brand,"category":category,"brand":brand})


def services(request):
    services = Services.objects.all()
    return render(request,"services.html",{"services":services})

def create_service(request):
    return render(request,"create_service.html")

def save_service(request):
    data=Services()
    data.service_name=request.POST.get("serviceName")
    data.service_slug=request.POST.get("serviceSlug")
    data.service_image=request.FILES.get("serviceImage")
    data.save()
    return redirect("/create_service/")

def manage_service(request):
    service=Services.objects.all()
    return render(request,"manage_service.html",{"service":service})

def edit_service(request,id):
    d=Services.objects.get(id=id)
    return render(request,"edit_service.html",{"d":d})

def delete_service(request,id):
    d = Services.objects.get(id=id)
    d.delete()
    return redirect("/manage_service/")

def update_service(request,id):
    data = Services.objects.get(id=id)
    service_image = request.FILES.get("serviceImage")
    if service_image:
        data.service_name = request.POST.get("serviceName")
        data.service_slug = request.POST.get("serviceSlug")
        data.service_image = request.FILES.get("serviceImage")
        data.save()
    else:
        data.service_name = request.POST.get("serviceName")
        data.service_slug = request.POST.get("serviceSlug")
        data.save()
    return redirect("/manage_service/")

def book_now(request,slug):
    ser=Services.objects.get(service_slug=slug)
    return render(request,"book_now.html",{"ser":ser})

def submit_booking(request):
    data=Service_Booking()
    data.name=request.POST.get("name")
    data.email=request.POST.get("email")
    data.phone=request.POST.get("phone")
    data.service_id=request.POST.get("service_id")
    data.date=request.POST.get("date")
    data.time=request.POST.get("time")
    data.comments=request.POST.get("comments")
    data.save()
    return redirect("/")


def bookings(request):
    data=Service_Booking.objects.all()
    return render(request,"bookings.html",{"data":data})
