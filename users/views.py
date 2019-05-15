from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import SetPasswordForm
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from .forms import UserAppForm, UserUpdateForm
from .models import UserApplication, Profile, UserBlacklist, UserMessages
from .decorators import su_required
from django.contrib.auth.hashers import make_password


def apply(request):
    if request.method == 'POST':
        form = UserAppForm(request.POST)

        isValid = True
        if UserBlacklist.objects.filter(username=request.POST['username']).exists():
            messages.success(request, 'This user is blocked from re-application')
            isValid = False
        else:
            if User.objects.filter(username=request.POST['username']).exists():
                messages.success(request, 'User already exists.')
                isValid = False

        if form.is_valid() and isValid:
            form.save()
            return redirect('uappsuccess')
    else:
        form = UserAppForm()
    return render(request, 'registration/apply.html', {'form': form})


def uappsuccess(request):
    return render(request, 'registration/uappsuccess.html')


def usermessages(request):
    receivedMessages = UserMessages.objects.filter(recipient=request.user)
    sentMessages = UserMessages.objects.filter(sender=request.user)

    content = {'receivedMessages': receivedMessages,
               'sentMessages': sentMessages}
    return render(request, 'users/messages.html', content)


def viewmessages(request):
    message = UserMessages.objects.get(pk=request.GET['id'])

    return render(request, 'users/viewmessage.html', {'message': message})


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


@login_required
def EditProfile(request):
    try:
        if request.method == 'POST':
            u_form = UserUpdateForm(request.POST, instance=request.user.profile)
            if u_form.is_valid():
                u_form.save()
                messages.success(request, "Your account has been updated !")
                return redirect('index')
        else:
            u_form = UserUpdateForm(instance=request.user, initial={'credit_card_num': request.user.profile.credit_card_num,
                                                                    'address': request.user.profile.address,
                                                                    'state': request.user.profile.state,
                                                                    'phone_num': request.user.profile.phone_num})

        context = {
            'u_form' : u_form,
        }
        return render(request, 'users/edit_profile.html', context)

    except ObjectDoesNotExist:
        return render(request, 'users/account_not_exist.html')

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
            UserBlacklist.objects.create(username=applicant.username)
            messages.success(request, applicant.username + ' has been denied and added to the Blacklist.')

            applicant.delete()
        return redirect('uapps')

    return render(request, 'users/denyUser.html', {'applicant': applicant})


@su_required
def ublacklist(request):
    blacklist = UserBlacklist.objects.all()

    return render(request, 'users/userblacklist.html', {'blacklist': blacklist})
