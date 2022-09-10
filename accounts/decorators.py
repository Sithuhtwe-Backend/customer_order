
from django.http import HttpResponse
from django.shortcuts import redirect


def authenticated_user(view_func): #view fun is functions are under decorator
    def wrapper(request): #request from login/register's parameters
        if not request.user.is_authenticated:
            return view_func(request)
        else:
            return redirect('/')
    
    return wrapper

#customized decorator 
def admin_only(view_func):
    def wrapper(request):
        if request.user.groups.first().name =="admin":
            return view_func(request)
        if request.user.groups.first().name =="customer":
            return redirect('/customer_profile')
        
    return wrapper

#customized decorator with customized parameter such as admin/customer role
def allowed_roles(roles=[]):
    def decorator(view_func): #to accept the function as parameter
        def wrapper(request, *args, **kwargs): #args for extra parameters
            if request.user.groups.first().name in roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse("You are not allowed to create order")
        return wrapper
    
    return decorator
        