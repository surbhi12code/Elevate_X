from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout


from .models import User
from .form import RegisterUserForm
from resume.models import Resume
from company.models import Company

# register applicant only
def register_applicant(request):
    if request.method=='POST':
        form=RegisterUserForm(request.POST)
        if form.is_valid():
            var=form.save(commit=False)
            var.is_applicant =True
            var.username=var.email
            var.save()
            Company.objects.create(user=var)
            messages.info(request,'Your account has been created.Please Login')
            return redirect('login')
        else:
            messages.warning(request,'something went wrong')   
            return redirect('register-applicant')
    else:
        form=RegisterUserForm()
        context={'form':form}
        return render(request,'users/register_applicant.html',context)
        
# register recuriter only

def register_recuriter(request):
    if request.method=='POST':
        form=RegisterUserForm(request.POST)
        if form.is_valid():
            var=form.save(commit=False)
            var.is_recuriter =True
            var.username=var.email
            var.save()
            Resume.objects.create(user=var)
            messages.info(request,'Your account has been created.Please login')
            return redirect('login')
        else:
            messages.warning(request,'something went wrong')   
            return redirect('register-recuriter')
    else:
        form=RegisterUserForm()
        context={'form':form}
        return render(request,'users/register_recuriter.html',context)
    pass

# Create your views here.
# login a user
def login_user(request):
    if request.method=='POST':
        email=request.POST.get('email')
        password=request.POST.get('password')
        
        user=authenticate(request,username=email,password=password)
        if user is not None and user.is_active:
            login(request,user)
            return render(request,'land.html')
            # if request.user.is_applicant:
            #     return redirect('applicant-dashboard')
            # elif request.user.is_recuriter:
            #     return redirect('recuriter-dashboard')
            # else:
            #     return redirect('login')
        else:
            messages.warning(request,'something went wrong') 
            return redirect('login')       
    else:
        return render(request,'users/login.html')
    
def logout_user(request):
    logout(request)
    messages.info(request,'your session has ended')
    return redirect('login')       