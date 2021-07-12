from django.http import HttpResponse
from django.shortcuts import redirect
from .models import*

def authenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
       if request.user.is_authenticated:
           return redirect('dashboard')
       else:
        return view_func(request, *args, **kwargs)
    return wrapper_func


def check_teacher_authentication(view_func):
    def wrapper_func(request, *args, **kwargs):
        user = User.objects.all().filter(username= request.user)
        print(request.user)
        teacher = UserProfileInfo.objects.all().filter(user__in=user).first()
        print(teacher)
        if teacher.userType == 'Teacher':
            return view_func(request, *args, **kwargs)
        else:
            return redirect('login')
    return wrapper_func

def check_student_authentication(view_func):
    def wrapper_func(request, *args, **kwargs):
        user = User.objects.all().filter(username= request.user)
        print(request.user)
        teacher = UserProfileInfo.objects.all().filter(user__in=user).first()
        print(teacher)
        if teacher.userType == 'Student':
            return view_func(request, *args, **kwargs)
        else:
            return redirect('login')
    return wrapper_func

def check_super_user(view_func):
    def wrapper_func(request, *args, **kwargs):
       if request.user.is_superuser:
           return view_func(request, *args, **kwargs)
       else:
           return redirect('login')
    return wrapper_func