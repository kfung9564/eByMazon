from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import SetPasswordForm
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User

from .forms import UserAppForm
from .models import UserApplication
from .decorators import su_required
from django.contrib.auth.hashers import make_password


def apply(request):
    if request.method == 'POST':
        form = UserAppForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('uappsuccess')
    else:
        form = UserAppForm()
    return render(request, 'registration/apply.html', {'form': form})


def uappsuccess(request):
    return render(request, 'registration/uappsuccess.html')


@login_required
def newuserlanding(request):
    if request.user.profile.is_new is False:
        return redirect('index')

    if request.method == 'POST':
        form = SetPasswordForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            getUser = User.objects.get(username=user.username)
            getUser.profile.is_new = False
            getUser.save()
            messages.success(request, 'Your password is set. Welcome to eByMazon!')
            return redirect('index')
    else:
        form = SetPasswordForm(request.user)
    return render(request, 'users/newUserLanding.html', {'form': form})


@su_required
def uapps(request):
    apps = UserApplication.objects.all()
    return render(request, 'users/applications.html', {'apps': apps})


@su_required
def uappapprove(request):
    applicant = UserApplication.objects.get(username=request.GET['Username'])
    if request.method == 'POST':
        if request.POST['Approve'] == 'Confirm':
            User.objects.create(username=applicant.username, password=make_password(applicant.username))
            newUser = User.objects.get(username=applicant.username)
            newUser.profile.address = applicant.address
            newUser.profile.state = applicant.state
            newUser.profile.credit_card_num = applicant.credit_card_num
            newUser.profile.name = applicant.name
            newUser.profile.phone_num = applicant.phone_num
            newUser.save()
            applicant.delete()
        return redirect('uapps')

    return render(request, 'users/approveUser.html', {'applicant': applicant})


@su_required
def uappdeny(request):
    applicant = UserApplication.objects.get(username=request.GET['Username'])
    if request.method == 'POST':
        if request.POST['Deny'] == 'Confirm':
            applicant.delete()
        return redirect('uapps')

    return render(request, 'users/denyUser.html', {'applicant': applicant})
