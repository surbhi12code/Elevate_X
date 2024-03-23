from django.shortcuts import render,redirect

# Create your views here.
def dashboard(request):
    return render(request,'dashboard/dashboard.html')
#     if request.user.is_applicant:
#         return redirect('applicant-dashboard')
#     elif request.user.is_recuriter:
#                 return redirect('recuriter-dashaboard')
#     else:
#         return redirect('login')
# def applicant_dashboard(request):
#     return render('dashaboard/applicant_dashboard.html')

# def recuriter_dashboard(request):
#     return render('dashaboard/recuriter_dashboard.html')