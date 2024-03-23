
# Create your views here.
from django.shortcuts import render ,HttpResponse,redirect
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth.decorators import login_required, user_passes_test
from quiz.models import UserRank, Quiz, QuizSubmission, Question
import math

import datetime
from django.contrib import messages
# Create your views here.
# def home(request):
#     return render(request,'land.html')
from .models import User
from .models import Profile
from django.db.models.signals import post_save
from django.dispatch import receiver
# def register_applicant(request):
#     if request.method == 'POST':
#         form = RegisterUserForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.is_applicant = True
#             user.username = user.email
#             user.save()  # Save the user object first

#             # Now create a profile for the user
#             profile = Profile.objects.create(user=user)

#             # Optionally, you can populate other fields of the profile here
#             # For example:
#             # profile.bio = "Some bio"
#             # profile.location = "Some location"
#             # profile.gender = "Male"
#             # profile.save()

#             messages.info(request, 'Your account has been created. Please login.')
#             return redirect('login')
#         else:
#             messages.warning(request, 'Something went wrong')
#             return redirect('register-applicant')
#     else:
#         form = RegisterUserForm()
#     return render(request, 'register_applicant.html', {'form': form})


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
@login_required(login_url='login')
def profile(request, username):

    # profile user
    user_object2 = User.objects.get(username=username)
    user_profile2 = Profile.objects.get(user=user_object2)

    # request user
    user_object = User.objects.get(username=request.user)
    user_profile = Profile.objects.get(user=user_object)

    submissions = QuizSubmission.objects.filter(user=user_object2)

    context = {"user_profile": user_profile, "user_profile2": user_profile2,"submissions":submissions}
    return render(request, "base/profile.html", context)

@login_required(login_url='login')
def editProfile(request):

    user_object = User.objects.get(username=request.user)
    user_profile = Profile.objects.get(user=user_object)

    if request.method == "POST":
        # Image
        if request.FILES.get('profile_img') != None:
            user_profile.profile_img = request.FILES.get('profile_img')
            user_profile.save()

        # Email
        if request.POST.get('email') != None:
            u = User.objects.filter(email=request.POST.get('email')).first()

            if u == None:
                user_object.email = request.POST.get('email')
                user_object.save()
            else:
                if u != user_object:
                    messages.info(request, "Email Already Used, Choose a different one!")
                    return redirect('edit_profile')

        # Username
        if request.POST.get('username') != None:
            u = User.objects.filter(username=request.POST.get('username')).first()

            if u == None:
                user_object.username = request.POST.get('username')
                user_object.save()
            else:
                if u != user_object:
                    messages.info(request, "Username Already Taken, Choose an unique one!")
                    return redirect('edit_profile')

        # firstname lastname
        user_object.first_name = request.POST.get('firstname')
        user_object.last_name = request.POST.get('lastname')
        user_object.save()

        # location , bio, gender
        user_profile.location = request.POST.get('location')
        user_profile.gender = request.POST.get('gender')
        user_profile.bio = request.POST.get('bio')
        user_profile.save()

        return redirect('profile', user_object.username)


    context = {"user_profile": user_profile}
    return render(request, 'base/profile-edit.html', context)


@login_required(login_url='login')
def deleteProfile(request):

    user_object = User.objects.get(username=request.user)
    user_profile = Profile.objects.get(user=user_object)

    if request.method == "POST":
        user_profile.delete()
        user_object.delete()
        return redirect('logout')



    context = {"user_profile": user_profile}
    return render(request, 'base/confirm.html', context)


def practice(request):
    leaderboard_users = UserRank.objects.order_by('rank')[:4]
    if request.user.is_authenticated:
        user_object = User.objects.get(username=request.user)
        user_profile = Profile.objects.get(user=user_object)
        context = {"user_profile":user_profile,"leaderboard_users":leaderboard_users}
    else:
        context ={"leaderboard_users":leaderboard_users}
    return render(request,'base/welcome.html',context)


@login_required(login_url="login")
def leaderboard_view(request):

    user_object = User.objects.get(username=request.user)
    user_profile = Profile.objects.get(user=user_object)

    leaderboard_users = UserRank.objects.order_by('rank')

    context = {"leaderboard_users": leaderboard_users, "user_profile": user_profile}
    return render(request, "base/leaderboard.html", context)

def is_superuser(user):
    return user.is_superuser

@user_passes_test(is_superuser)
@login_required(login_url='login')
def dashboard_view(request):

    user_object = User.objects.get(username=request.user)
    user_profile = Profile.objects.get(user=user_object)


    # Total Number
    total_users = User.objects.all().count()
    total_quizzes = Quiz.objects.all().count()
    total_quiz_submit = QuizSubmission.objects.all().count()
    total_questions = Question.objects.all().count()

    # today_numbers
    today_users = User.objects.filter(date_joined__date=datetime.date.today()).count()
    today_quizzes_objs = Quiz.objects.filter(created_at__date=datetime.date.today())
    today_quizzes = Quiz.objects.filter(created_at__date=datetime.date.today()).count()
    today_quiz_submit = QuizSubmission.objects.filter(submitted_at__date=datetime.date.today()).count()
    today_questions = 0
    for quiz in today_quizzes_objs:
        today_questions += quiz.question_set.count()

    # Gain %
    gain_users = gain_percentage(total_users, today_users)
    gain_quizzes = gain_percentage(total_quizzes, today_quizzes)
    gain_quiz_submit = gain_percentage(total_quiz_submit, today_quiz_submit)
    gain_questions = gain_percentage(total_questions, today_questions)

    # Inbox Messages
    #messages = Message.objects.filter(created_at__date=datetime.date.today()).order_by('-created_at')


    context = {"user_profile": user_profile, 
               "total_users": total_users,
               "total_quizzes": total_quizzes,
               "total_quiz_submit": total_quiz_submit,
               "total_questions": total_questions,
               "today_users":today_users,
               "today_quizzes":today_quizzes,
               "today_quiz_submit":today_quiz_submit,
               "today_questions":today_questions,
               "gain_users": gain_users,
               "gain_quizzes": gain_quizzes,
               "gain_quiz_submit": gain_quiz_submit,
               "gain_questions": gain_questions,
               #"messages": messages,
               }
    return render(request, "dashboard.html", context)

def gain_percentage(total, today):
    if total > 0 and today > 0:
        gain = math.floor((today *100)/total)
        return gain

def about_view(request):

    if request.user.is_authenticated:
        # request user
        user_object = User.objects.get(username=request.user)
        user_profile = Profile.objects.get(user=user_object)
        context = {"user_profile": user_profile}
    else:
        context = {}
    return render(request, "base/about.html", context)


def contact_view(request):
    return render(request,"base/contact.html")