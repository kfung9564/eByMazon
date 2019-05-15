from django.urls import include, path
from . import views

# users/

urlpatterns = [
    # path(URL_NAME, views.VIEW_NAME, NAME)

    path('apply/', views.apply, name='apply'),
    path('list/', views.userlist, name='userlist'),
    path('messages/', views.usermessages, name='messages'),
    path('messages/send', views.sendmessages, name='sendmessages'),
    path('messages/view', views.viewmessages, name='viewmessages'),
    path('landing/', views.newuserlanding, name='newUserLanding'),
    path('applications/', views.uapps, name='uapps'),
    path('applications/success', views.uappsuccess, name='uappsuccess'),
    path('applications/approve', views.uappapprove, name='approveUser'),
    path('applications/deny', views.uappdeny, name='denyUser'),
    path('applications/blacklist', views.ublacklist, name='ublacklist'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('edit', views.EditProfile, name = 'editprofile'),
    path('transactions/', views.transhistory, name='transhistory'),
    path('usertransactions/', views.usertransactions, name='usertransactions'),
    # users/login/ [name='login']
    # users/logout/ [name='logout']
    # users/password_change/ [name='password_change']
    # users/password_change/done/ [name='password_change_done']
    # users/password_reset/ [name='password_reset']
    # users/password_reset/done/ [name='password_reset_done']
    # users/reset/<uidb64>/<token>/ [name='password_reset_confirm']
    # users/reset/done/ [name='password_reset_complete']
    path('', include('django.contrib.auth.urls')),
]
