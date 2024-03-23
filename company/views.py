from django.shortcuts import render,redirect
from django.contrib import messages
from .models import Company
from .form import UpdateCompanyForm
from dashboard.views import dashboard

from users.models import User
# Create your views here.


def update_company(request):
    if request.user.is_recuriter:
        try:
            company = Company.objects.get(user=request.user)
        except Company.DoesNotExist:
            # If no Company object is found for the current user, create a new one
            company = Company.objects.create(user=request.user)
        
        if request.method=='POST':
            form=UpdateCompanyForm(request.POST,instance=company)
            if form.is_valid():
                var=form.save(commit=False)
                user=User.objects.get(id=request.user.id)
                user.has_company=True
                var.save()
                user.save()
                messages.info(request,'Your company is now active.You can start creating job ads')
                return redirect('dashboard')
            else:
                messages.warning(request,'something went wrong')   
        else:
            form=UpdateCompanyForm(instance=company)  
            context={'form':form}
            return render(request,'company/update_company.html',context)
    else:
        messages.warning(request,'Permission denied')
        return redirect('dashboard')   
def company_details(request, pk):
    company = Company.objects.get(pk=pk)
    context = {'company': company}
    return render(request, 'company/company_details.html', context)

# def company_details(request,pk):
#     company=company.objects.get(pk=pk)
#     context={'company':company}
#     return render(request,'company/company_details.html',context)
        
    