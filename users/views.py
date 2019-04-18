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


@su_required
def uapps(request):
    apps = UserApplication.objects.all()
    return render(request, 'users/applications.html', {'apps': apps})


def uappsuccess(request):
    return render(request, 'registration/uappsuccess.html')
