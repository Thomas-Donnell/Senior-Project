from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import Account
from django.contrib.auth.models import User
from .forms import CreateUserForm, AccountForm
from django.contrib import messages



def register(request):
    form = CreateUserForm()
    account_form = AccountForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        account_form = AccountForm(request.POST)
        if form.is_valid() and account_form.is_valid():
            user = form.save()
            account = account_form.save(commit=False)
            account.user = user
            account.save()
            return redirect('users:loginPage')
        else:
            messages.error(request, 'Could Not Register account')

    context = {'form':form, 'account_form':account_form}
    return render(request, "users/registration.html", context)

def loginPage(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
            account = Account.objects.get(user=user)
            if account is not None:
                auth = authenticate(request, username=username, password=password)
                if auth is not None:
                    is_teacher = account.is_teacher
                    login(request, user)
                    if is_teacher:
                        return redirect('teachers:home')
                    else:
                        return redirect('students:home')
                else:
                    messages.error(request, 'The Password is Incorrect')
        except Exception as e:
            messages.error(request, "The username does Not Exist")

    context = {}
    return render(request, "users/login.html", context)

def logoutPage(request):
    logout(request)
    return redirect('users:loginPage') 

