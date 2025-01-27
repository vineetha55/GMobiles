from django.db import models

# Create your models here.
class Registration(models.Model):
    name=models.CharField(max_length=50,null=True)
    email=models.EmailField(null=True)
    mobile=models.IntegerField(null=True)
    password=models.CharField(max_length=200,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=255, unique=True)
    logo = models.ImageField(upload_to="brands/logos/", blank=True, null=True)
    slug = models.SlugField(unique=True,null=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True, related_name="products")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    image = models.ImageField(upload_to="products/images/")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Cart(models.Model):
    session_key = models.CharField(max_length=255, null=True, blank=True)  # For guest users
    user = models.ForeignKey(Registration, on_delete=models.CASCADE, null=True, blank=True)  # For logged-in users
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def total_price(self):
        return self.product.price * self.quantity
class User_Ship_Address(models.Model):
    user = models.ForeignKey(Registration, on_delete=models.CASCADE, null=True, blank=True)
    firstname = models.CharField(max_length=100, null=True)
    lastname = models.CharField(max_length=100, null=True)
    country = models.CharField(max_length=100, null=True)
    street_address = models.CharField(max_length=500, null=True)
    apartment = models.CharField(max_length=300, null=True)
    city = models.CharField(max_length=100, null=True)
    zip = models.CharField(max_length=100, null=True)
    phone = models.IntegerField(null=True)
    email = models.EmailField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
class Bookings(models.Model):
    ship_add=models.ForeignKey(User_Ship_Address,on_delete=models.CASCADE,null=True)
    user = models.ForeignKey(Registration, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,null=True)
    total_price=models.FloatField(null=True)
    quantity=models.IntegerField(null=True)
    delivery =models.FloatField(null=True)
    sub_total = models.FloatField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)
    status=models.CharField(max_length=100,null=True)


class Multi_Bookings(models.Model):
    ship_add = models.ForeignKey(User_Ship_Address, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(Registration, on_delete=models.CASCADE, null=True, blank=True)
    total_price = models.FloatField(null=True)
    delivery = models.FloatField(null=True)
    sub_total = models.FloatField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=100, null=True)

class Order_Item(models.Model):
    book=models.ForeignKey(Multi_Bookings,on_delete=models.CASCADE,null=True)
    user = models.ForeignKey(Registration, on_delete=models.CASCADE, null=True, blank=True)  # For logged-in users
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)
    
class Contact(models.Model):
    name=models.CharField(max_length=100,null=True)
    email=models.EmailField(null=True)
    subject=models.CharField(max_length=100,null=True)
    message=models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



class ProductAttribute(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="attributes")
    key = models.CharField(max_length=255,null=True)
    value = models.CharField(max_length=255,null=True)


class Services(models.Model):
    service_name=models.CharField(max_length=100,null=True)
    service_slug=models.CharField(max_length=100,null=True)
    service_image=models.ImageField(upload_to="Service/",null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Service_Booking(models.Model):
    service=models.ForeignKey(Services,on_delete=models.CASCADE,null=True)
    name=models.CharField(max_length=100,null=True)
    email=models.EmailField(null=True)
    phone=models.IntegerField(null=True)
    date=models.DateField(null=True)
    time=models.TimeField(null=True)
    comments=models.CharField(max_length=700,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

