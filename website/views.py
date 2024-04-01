from django.shortcuts import render
from job.models import Job,ApplyJob
from .filter import JobFilter

# Create your views here.
def home(request):
    return render(request,'land.html')
def getHired(request):
    filter=JobFilter(request.GET,queryset=Job.objects.filter(is_available=True).order_by('-timestamp'))
    context={'filter':filter}
    return render(request,'website/home.html',context)

def doquiz(request):
    return render(request,'base/welcome.html')

def get_certified(request):
    return render(request,'certificate/welcome.html')

def job_listing(request,):
 
    jobs=Job.objects.filter(is_available=True).order_by('-timestamp')
    context={'jobs':jobs}
    return render(request,'website/job_listing.html',context)
def job_details(request,pk):
    if ApplyJob.objects.filter(user=request.user,job=pk).exists():
        has_applied=True
    else:
        has_applied=False
        
        
    jobs=Job.objects.get(pk=pk)
    context={'job':jobs ,'has_applied':has_applied}
    return render(request,'website/job_details.html',context)
