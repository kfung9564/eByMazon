from django.shortcuts import render, redirect
from .forms import UserAppForm
from .models import UserApplication
from .decorators import su_required


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


@su_required
def uapps(request):
    apps = UserApplication.objects.all()
    return render(request, 'users/applications.html', {'apps': apps})


@su_required
def uappapprove(request):
    return render(request, 'users/approveUser.html')


@su_required
def uappdeny(request):
    return render(request, 'users/denyUser.html')
