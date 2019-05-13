from django.urls import path
from . import views

urlpatterns = [
    # path(URL_NAME, views.VIEW_NAME, NAME)

    path('blacklist/', views.catalogblacklist, name='catalogblacklist'),
    path('application/', views.catalogreview, name='catalogreview'),
    path('apply/', views.apply, name='itemapply'),
    path('manage/', views.manageitems, name='itemmanager'),
    path('edit/', views.edititems, name='edititems'),
    path('', views.catalog, name='catalog'),
]