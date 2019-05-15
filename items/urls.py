from django.urls import path
from . import views

urlpatterns = [
    # path(URL_NAME, views.VIEW_NAME, NAME)
    path('search/', views.search, name='search'),
    path('blacklist/', views.catalogblacklist, name='catalogblacklist'),
    path('application/', views.catalogreview, name='catalogreview'),
    path('apply/', views.apply, name='itemapply'),
    path('rate/', views.rateuser, name='rateuser'),
    path('manage/', views.manageitems, name='itemmanager'),
    path('manage/edit/', views.edititems, name='edititems'),
    path('manage/sell/', views.sellitems, name='sellitems'),
    path('manage/sell/fixed', views.sellfixed, name='sellfixed'),
    path('manage/sell/bid', views.sellbid, name='sellbid'),
    path('manage/offsale', views.putoffsale, name = 'putoffsale'),
    path('manage/itemlist/', views.itemlist, name='itemlist'),
    path('manage/orders/', views.processorders, name='processorders'),
    path('manage/bids/', views.processbids, name='processbids'),
    path('manage/removeitem/', views.removeitem, name='removeitem'),
    path('manage/suedit/', views.su_edititem, name='suedit'),
    path('manage/confirmorder/', views.confirmorder, name='confirmorder'),
    path('manage/confirmnotfirstorder/', views.confirmnotfirst, name='confirmnotfirst'),
    path('manage/winner', views.confirmwinner, name='confirmwinner'),
    path('manage/notwinner/', views.confirmnotwinner, name='confirmnotwinner'),
    path('', views.catalog, name='catalog'),
    path('shopping/itempage', views.fixeditempage, name='fixeditempage'),
    path('shopping/order', views.fixeditemorder, name='fixeditemorder'),
    path('auction/itempage', views.biditempage, name='biditempage'),
    path('auction/bid', views.placebidpage, name='placebidpage'),
]