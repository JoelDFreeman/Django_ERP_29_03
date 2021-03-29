import csv
from django.shortcuts import render, redirect 
from django.http import HttpResponse
from django.forms import *
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User

from .models import *
from .forms import *
from .filters import *
from .decorators import unauthenticated_user, allowed_users, admin_only
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

@login_required(login_url='login')
@admin_only
def upload(request):
	form = ProductImageForm(request.POST or None)
	if form.is_valid():
		form.save()
	
	context = {
		'form': form
	} 	
	return render(request,"accounts/upload.html", context)

@login_required(login_url='login')
@admin_only
def tag_create(request):
	form = TagCreateForm(request.POST or None)
	if form.is_valid():
		form.save()
	
	context = {
		'form': form
	} 	
	return render(request,"accounts/product_tag.html", context)

@login_required(login_url='login')
@admin_only
def product_create(request):
	form = ProductForm(request.POST or None)
	if form.is_valid():
		form.save()
	
	context = {
		'form': form
	} 	
	return render(request,"accounts/product_create.html", context)

@login_required(login_url='login')
@admin_only
def customer_create(request):
	form = CustomerCreateForm(request.POST or None)
	if form.is_valid():
		form.save()
	
	context = {
		'form': form
	} 	
	return render(request,"accounts/customer_create.html", context)
	
@login_required(login_url='login')
@admin_only
def order_create(request):
	form = OrderCreateForm(request.POST or None)
	if form.is_valid():
		form.save()
	
	context = {
		'form': form
	} 	
	return render(request,"accounts/order_create.html", context)	

def registerPage(request):

	form = CreateUserForm()
	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			username = form.cleaned_data.get('username')


			messages.success(request, 'Account was created for ' + username)

			return redirect('login')
		

	context = {'form':form}
	return render(request, 'accounts/register.html', context)

@unauthenticated_user
def loginPage(request):

	if request.method == 'POST':
		username = request.POST.get('username')
		password =request.POST.get('password')

		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			return redirect('home')
		else:
			messages.info(request, 'Username OR password is incorrect')

	context = {}
	return render(request, 'accounts/login.html', context)

def logoutUser(request):
	logout(request)
	return redirect('login')

@login_required(login_url='login')
@admin_only
def home(request):
	orders = Order.objects.all()
	customers = Customer.objects.all()

	total_customers = customers.count()

	total_orders = orders.count()
	delivered = orders.filter(status='Delivered').count()
	pending = orders.filter(status='Pending').count()
	page = request.GET.get('page', 1)

	paginator = Paginator(customers, 5)	
	try:
		customers = paginator.page(page)
	except PageNotAnInteger:
		customers = paginator.page(1)
	except EmptyPage:
		customers= paginator.page(paginator.num_pages)

	paginator_two = Paginator(orders, 5)	
	try:
		orders = paginator_two.page(page)
	except PageNotAnInteger:
		orders = paginator_two.page(1)
	except EmptyPage:
		orders= paginator_two.page(paginator_two.num_pages)	

	context = {'orders':orders, 'customers':customers,
	'total_orders':total_orders,'delivered':delivered,
	'pending':pending, 'total_customers':total_customers, 'page':page, 'paginator':paginator, 'paginator_two':paginator_two }

	return render(request, 'accounts/dashboard.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
	orders = request.user.customer.order_set.all()

	total_orders = orders.count()
	delivered = orders.filter(status='Delivered').count()
	pending = orders.filter(status='Pending').count()

	print('ORDERS:', orders)

	context = {'orders':orders, 'total_orders':total_orders,
	'delivered':delivered,'pending':pending}
	return render(request, 'accounts/user.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def accountSettings(request):
	customer = request.user.customer
	form = CustomerForm(instance=customer)

	if request.method == 'POST':
		form = CustomerForm(request.POST, request.FILES,instance=customer)
		if form.is_valid():
			form.save()


	context = {'form':form}
	return render(request, 'accounts/account_settings.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def Orders(request):
	orders = Order.objects.all()
	orders_count = orders.count()
	myFilter = OrderFilter(request.GET, queryset=orders)
	orders = myFilter.qs

	page = request.GET.get('page', 1)

	paginator = Paginator(orders, 5)	
	try:
		orders = paginator.page(page)
	except PageNotAnInteger:
		orders = paginator.page(1)
	except EmptyPage:
		orders = paginator.page(paginator.num_pages) 

	context = {'orders_count':orders_count,
	'myFilter':myFilter,'orders':orders}
	return render(request, 'accounts/orders.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def products(request):
	products = Product.objects.all()

	products_count = products.count()
	myFilter = ProductFilter(request.GET, queryset=products)
	products = myFilter.qs 

	page = request.GET.get('page', 1)

	paginator = Paginator(products, 5)	
	try:
		products = paginator.page(page)
	except PageNotAnInteger:
		products = paginator.page(1)
	except EmptyPage:
		products = paginator.page(paginator.num_pages)
	context = {'products_count':products_count,
	'myFilter':myFilter,'products':products}

	return render(request, 'accounts/products.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customer(request, pk_test):
	customer = Customer.objects.get(id=pk_test)

	orders = customer.order_set.all()
	order_count = orders.count()

	myFilter = OrderFilter(request.GET, queryset=orders)
	orders = myFilter.qs 

	context = {'customer':customer, 'orders':orders, 'order_count':order_count,
	'myFilter':myFilter}
	return render(request, 'accounts/customer.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customers(request):
	customers = Customer.objects.all()
	page = request.GET.get('page', 1)
	myFilter = CustomerFilter(request.GET, queryset=customers)
	customers = myFilter.qs 
	form = CustomerCreateForm()
	if request.method == 'POST':
		form = CustomerCreateForm(request.POST)
		if form.is_valid():
			user = form.save()
			
			messages.success(request, 'Customer Created ')

			return redirect('login')
	paginator = Paginator(customers, 5)	
	try:
		customers = paginator.page(page)
	except PageNotAnInteger:
		customers = paginator.page(1)
	except EmptyPage:
		customers = paginator.page(paginator.num_pages)

	context = {'customers':customers,'myFilter':myFilter}
	return render(request, 'accounts/customers.html',context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createOrder(request, pk):
	OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=10 )
	customer = Customer.objects.get(id=pk)
	formset = OrderFormSet(queryset=Order.objects.none(),instance=customer)
	#form = OrderForm(initial={'customer':customer})
	if request.method == 'POST':
		#print('Printing POST:', request.POST)
		form = OrderForm(request.POST)
		formset = OrderFormSet(request.POST, instance=customer)
		if formset.is_valid():
			formset.save()
			return redirect('/')

	context = {'form':formset}
	return render(request, 'accounts/order_form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateOrder(request, pk):
	order = Order.objects.get(id=pk)
	form = OrderForm(instance=order)
	print('ORDER:', order)
	if request.method == 'POST':

		form = OrderForm(request.POST, instance=order)
		if form.is_valid():
			form.save()
			return redirect('/')

	context = {'form':form}
	return render(request, 'accounts/order_form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateProduct(request, pk):
	product = Product.objects.get(id=pk)
	form = ProductForm(instance=product)
	print('PRODUCT:', product)
	if request.method == 'POST':

		form = ProductForm(request.POST, instance=product)
		if form.is_valid():
			form.save()
			return redirect('/')

	context = {'form':form}
	return render(request, 'accounts/product_form.html', context)	

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateCustomer(request, pk):
	customer = Customer.objects.get(id=pk)
	form = CustomerForm(instance=customer)
	print('CUSTOMER:', customer)
	if request.method == 'POST':

		form = CustomerForm(request.POST, instance=customer)
		if form.is_valid():
			form.save()
			return redirect('/')

	context = {'form':form}
	return render(request, 'accounts/customer_form.html', context)	

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request, pk):
	order = Order.objects.get(id=pk)
	if request.method == "POST":
		order.delete()
		return redirect('/')

	context = {'item':order}
	return render(request, 'accounts/delete.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteProduct(request, pk):
	product = Product.objects.get(id=pk)
	if request.method == "POST":
		product.delete()
		return redirect('/')

	context = {'item':product}
	return render(request, 'accounts/delete.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteCustomer(request, pk):
	customer = Customer.objects.get(id=pk)
	if request.method == "POST":
		customer.delete()
		return redirect('/')

	context = {'item':customer}
	return render(request, 'accounts/delete.html', context)

def visualisations(request):
	orders = Order.objects.all()
	customers = Customer.objects.all()

	total_customers = customers.count()

	total_orders = orders.count()

	delivered = orders.filter(status='Delivered').count()
	pending = orders.filter(status='Pending').count()

	context = {'orders':orders, 'customers':customers,
	'total_orders':total_orders,'delivered':delivered,
	'pending':pending, 'total_customers':total_customers}

	return render(request, 'accounts/visualisations.html', context)		

def download_csv(request):
 
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="customers.csv"' # your filename
 
    writer = csv.writer(response)
    writer.writerow(['name','phone'])
 
    customers = Customer.objects.all().values_list('name','phone')
 
    for customer in customers:
        writer.writerow(customer)
 
     
    return response


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateAddress(request, pk):
	CustomerAddress = CustomerAddress.objects.get(id=pk)
	form = CustomerAddressForm(instance=order)
	print('CUSTOMERADDRESS:', CustomerAddress)
	if request.method == 'POST':

		form = CustomerAddressForm(request.POST, instance=order)
		if form.is_valid():
			form.save()
			return redirect('/')

	context = {'form':form}
	return render(request, 'accounts/CustomerAddress_form.html', context)	

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteAddress(request, pk):
	customer = CustomerAddress.objects.get(id=pk)
	if request.method == "POST":
		customer.delete()
		return redirect('/')

	context = {'item':customer}
	return render(request, 'accounts/delete.html', context)

@login_required(login_url='login')
@admin_only
def createAddress(request):
	form = CustomerAddressForm(request.POST or None)
	if form.is_valid():
		form.save()
		return redirect('/customer_create')

	context = {
		'form': form
	} 	
	return render(request,"accounts/CustomerAddress_form.html", context)