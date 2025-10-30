from django.http import HttpRequest
from django.contrib.auth import login , logout, authenticate
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.contrib import messages
from core.forms import LoginForm, RegisterForm
from django.contrib.auth.decorators import login_required
from shop.models import Product
def home(request:HttpRequest):
    products = Product.objects.all()
    return render(request, 'home.html', {
        'products': products,
    })
def login_to_site(request: HttpRequest, user: User):
    login(request, user)
    #log = UserLog.objects.create(user = user, ip_address = request.META.get('REMOTE_ADDR'))
    #return log is not None
def login_page(request:HttpRequest):
    if not request.user.is_authenticated :
        login_form = LoginForm(request.POST or None)
        if login_form.is_valid():
            phone = login_form.cleaned_data.get('phone')
            password = login_form.cleaned_data.get('password')
            user = authenticate(request, username=phone, password=password)
            if user :
                #login(request, user)
                if login_to_site(request, user):
                    messages.success(request, f'سلام {user.first_name} {user.last_name} به سایت ما خوش آمدی !')
                return redirect('home')
            else :
                #raise Http404
                messages.warning(request, f'شماره تلفن یا رمز عبور صحیح نمیباشد !')
        return render(request, 'auth/login.html', {'form': login_form})
    return redirect('home')
def register_page(request:HttpRequest):
    if not request.user.is_authenticated :
        register_form = RegisterForm(request.POST or None)
        if register_form.is_valid():
            first_name = register_form.cleaned_data.get('first_name')
            last_name = register_form.cleaned_data.get('last_name')
            phone = register_form.cleaned_data.get('phone')
            email = register_form.cleaned_data.get('email')
            password = register_form.cleaned_data.get('password')
            user = User.objects.create_user(phone,email,password, first_name=first_name, last_name=last_name)
            user.save()
            if user :
                login_to_site(request, user)
                messages.success(request, f'سلام {first_name} {last_name} به سایت ما خوش آمدی !')
                # return redirect('dashboard:profile') # redirect to user profile
            return redirect('home')
        return render(request, 'auth/register.html', {'form': register_form})
    return redirect('home')
@login_required
def logout_page(request:HttpRequest):
    logout(request)
    messages.success(f'{request.user.first_name} {request.user.last_name} عزیز ، با موفقیت در سامانه خارج شده اید !')
    return redirect('home')