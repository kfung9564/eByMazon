from django.urls import path
from . import views

urlpatterns = [
    # path(URL_NAME, views.VIEW_NAME, NAME)

    path('blacklist/', views.catalogblacklist, name='catalogblacklist'),
    path('application/', views.catalogreview, name='catalogreview'),
    path('apply/', views.apply, name='itemapply'),
    path('manage/', views.manageitems, name='itemmanager'),
    path('manage/edit/', views.edititems, name='edititems'),
    path('manage/sell/', views.sellitems, name='sellitems'),
    path('manage/sell/fixed', views.sellfixed, name='sellfixed'),
    path('manage/sell/bid', views.sellbid, name='sellbid'),
    path('manage/offsale', views.putoffsale, name = 'putoffsale'),
    path('', views.catalog, name='catalog'),
]