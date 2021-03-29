from django.db import models
from django.contrib.auth.models import User
from django.core.files import File
from django.conf import settings
from .managers import ProductManager

CURRENCY = settings.CURRENCY


class Category(models.Model):
    title = models.CharField(max_length=150, unique=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.title

class CustomerAddress(models.Model):
	name = models.CharField(default="Address 1", max_length=200, null=True)
	addressline1 = models.CharField(max_length=200, null=True)
	county = models.CharField(max_length=30, null=True)
	postcode = models.CharField(max_length=10, null=True)
	date_created = models.DateTimeField(auto_now_add=True, null=True)

	def __str__(self):
		return self.name

class Customer(models.Model):
	name = models.CharField(max_length=200, null=True)
	customeraddress = models.ManyToManyField(CustomerAddress, blank=True)
	phone = models.CharField(max_length=200, null=True)
	email = models.EmailField(max_length=200, null=True)
	profile_pic = models.ImageField(default="profile1.png", null=True, blank=True)
	date_created = models.DateTimeField(auto_now_add=True, null=True)

	def __str__(self):
		return self.name


class Tag(models.Model):
	name = models.CharField(max_length=200, null=True)
	def __str__(self):
		return self.name

class ProductImage(models.Model):
	name = models.CharField(max_length=200, null=True)
	product_Main_Img = models.ImageField(default="product1.png", null=True, blank=True)	
	def __str__(self):
		return self.name

class Product(models.Model):
	CATEGORY = (
			('Indoor', 'Indoor'),
			('Out Door', 'Out Door'),
			) 

	name = models.CharField(max_length=200, null=True)
	price = models.FloatField(null=True)
	category = models.CharField(max_length=200, null=True, choices=CATEGORY)
	description = models.CharField(max_length=200, null=True, blank=True)
	date_created = models.DateTimeField(auto_now_add=True, null=True)
	tags = models.ManyToManyField(Tag, blank=True)
	product_note = models.CharField(max_length=1000, null=True, blank=True)
	productimage = models.ForeignKey(ProductImage, null=True, blank=True, on_delete= models.SET_NULL)
	value = models.DecimalField(default=0.00, decimal_places=2, max_digits=10, null=True, blank=True)
	discount_value = models.DecimalField(default=0.00, decimal_places=2, max_digits=10, null=True, blank=True)
	final_value = models.DecimalField(default=0.00, decimal_places=2, max_digits=10, null=True, blank=True)
	qty = models.PositiveIntegerField(default=0)

	objects = models.Manager()
	broswer = ProductManager()

	class Meta:
		verbose_name_plural = 'Products'

	def save(self, *args, **kwargs):
		self.final_value = self.discount_value if self.discount_value > 0 else self.value
		super().save(*args, **kwargs)

	def __str__(self):
		return self.name

	def tag_final_value(self):
		return f'{self.final_value} {CURRENCY}'
		tag_final_value.short_description = 'Value'

class Order(models.Model):
	STATUS = (
			('Pending', 'Pending'),
			('Out for delivery', 'Out for delivery'),
			('Delivered', 'Delivered'),
			)

	customer = models.ForeignKey(Customer, null=True, on_delete= models.SET_NULL)
	product = models.ManyToManyField(Product, blank=True)
	date_created = models.DateTimeField(auto_now_add=True, null=True)
	status = models.CharField(max_length=200, null=True, choices=STATUS)
	note = models.CharField(max_length=1000, null=True)
	note2 = models.CharField(max_length=1000, null=True)


def __str__(self):
    return str(self.Orderid)



	
