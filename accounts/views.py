from ast import Or
from dataclasses import field
import email
from http.client import HTTPResponse
from multiprocessing.sharedctypes import Value
from telnetlib import LOGOUT, STATUS
from django.shortcuts import render, redirect
from accounts.decorators import authenticated_user, admin_only, allowed_roles
from accounts.models import *
from accounts.forms import *
from django.forms import inlineformset_factory
from .filters import *
from django.contrib.auth import authenticate, logout,login
from django.contrib.auth.models import Group
from django.contrib import messages
from django.contrib.auth.decorators import login_required


@login_required(login_url="/login")
@admin_only
def dashboard(request):
    customers = Customer.objects.all()
    orders = Order.objects.all()
    total = orders.count()
    delivered = Order.objects.filter(status="d").count()
    pending = Order.objects.filter(status="pd").count()
    
    return render(request, "accounts/dashboard.html",{
        "customers": customers,
        "orders" : orders,
        "totals" : total,
        "delivered" : delivered,
        "pending" : pending,
        
    })

@login_required(login_url="/login")
@allowed_roles(roles=['admin'])
def customers(request, id):
    
    customers = Customer.objects.get(id=id)
    orders = customers.order_set.all() #we can take the order data from customer table cause of foreign key 
    filterObj = OrderFilter(request.GET, queryset=orders) #take the data from filtered data
    orders = filterObj.qs #qs = queryset to over write to orders object
    order_count = orders.count()
    return render(request, "accounts/customers.html",{
        "customers" : customers,
        "orders" : orders,
        "order_count" : order_count,
        "filterObj" : filterObj
        
    })

@login_required(login_url="/login")
def products(request):
    product = Product.objects.all()
    
    return render(request, "accounts/products.html", {
        'products': product
    })

@login_required(login_url="/login")
@allowed_roles(roles=['admin'])
def orderCreate(request, customerId):
    # return HttpResponse(customerId)
    Orderformset = inlineformset_factory(Customer,Order,fields=('product','status'),extra=10)
    customer = Customer.objects.get(id= customerId)
    formset = Orderformset(instance=customer, queryset=Order.objects.none()) #to add the customer data in the input field
    #to add none object to querset means need to clean the old data in create stage
    if request.method=="POST":
        formset = Orderformset(request.POST, instance=customer) #to take the each data from post request
        if formset.is_valid():
            formset.save()
            return redirect('/')
        
    return render(request, "accounts/order_form.html",{
        "formset" : formset,
        
    })
    
@login_required(login_url="/login")
def orderUpdate(request, orderId):
    order = Order.objects.get(id=orderId)
    form = OrderForm(instance=order)
    if request.method=="POST":
        #instance to take the data what the user wants
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')
    
    return render(request, "accounts/order_form.html",{
        "form" : form
    })
    
@login_required(login_url="/login")
def orderDelete(request, orderId):
    order = Order.objects.get(id= orderId)
    if request.method == "POST":
        order.delete()
        return redirect('/')
    return render(request, "accounts/order_delete.html",{
        "order":order
    })
    
@authenticated_user
def register(request):
    user = RegisterForm() #customize register form by doing inheritance from UserCreationForm
    if request.method == "POST":
        form = RegisterForm(request.POST)
        print(request.POST)
        print(form.is_valid())
        print(form.errors)
        if form.is_valid():
            print(request.POST)
            user = form.save()
            gp = Group.objects.get(name="customer") #need to add usergroup after registration
            user.groups.add(gp)
            #create customer profile for user
            print(request.POST)
            Customer.objects.create(name=request.POST['username'], email = request.POST['email'])
            #log in
            login(request,user)
            return redirect('dashboard')
    return render(request, 'accounts/register.html',{
        "user" :user,
    })


@authenticated_user
def userLogin(request):
    if request.method == "POST":
        print("Value" , request.user.is_authenticated)
        
        username = request.POST['username']
        passwords = request.POST['password']
        user = authenticate(request,username=username,password=passwords)
        
        if user is not None:
            login(request,user)
            return redirect('/')
            
        else :
            messages.error(request,"User Name and Password are incorrect")
            return redirect('/login')
    return render(request, 'accounts/login.html')

@login_required(login_url='/login')
def userLogout(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        username = User.objects.get(email=form.cleaned_data['email'])
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        print(user)
    logout(request)
    return redirect('/login')
    
@login_required(login_url='/login')
@allowed_roles(roles=['customer'])
def customer_profile(request):
#    orders=request.user.customer.order_set.all()
   print(request)
   cust_name = Customer.objects.get(name = request.user)
   print(cust_name)
   orders=Order.objects.filter(customer = cust_name)
#    orders = Order.objects.filter()
   total=orders.count()
   delivered= orders.filter(status="delivered").count()
   pending= orders.filter(status="pending").count()
   return render(request,'accounts/customer_profile.html',{
      'orders':orders,
      'totals':total,
      'delivered':delivered,
      'pending':pending
   })
   
def customer_profile_setting(request):
    form = CustomerProfileSetting(instance=request.user.customer)
    if request.method == "POST":
        form = CustomerProfileSetting(request.POST,request.FILES,instance=request.user.customer)
        print(form.is_valid())
        if form.is_valid():
            user = form.save()
            print(user)
            return redirect('/customer_profile')
    return render(request, 'accounts/profile_setting.html',{
        'form': form
    })