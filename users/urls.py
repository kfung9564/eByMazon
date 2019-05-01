from django.urls import include, path
from . import views

# users/

urlpatterns = [
    path('apply/', views.apply, name='apply'),
    path('applications/', views.uapps, name='uapps'),
    path('applications/success', views.uappsuccess, name='uappsuccess'),
    path('applications/approve', views.uappapprove, name='approveUser'),
    path('applications/deny', views.uappdeny, name='denyUser'),

    # users/login/ [name='login']
    # users/logout/ [name='logout']
    # users/password_change/ [name='password_change']
    # users/password_change/done/ [name='password_change_done']
    # users/password_reset/ [name='password_reset']
    # users/password_reset/done/ [name='password_reset_done']
    # users/reset/<uidb64>/<token>/ [name='password_reset_confirm']
    # users/re`set/done/ [name='password_reset_complete']
    path('', include('django.contrib.auth.urls')),
]
