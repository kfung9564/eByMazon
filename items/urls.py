from django.urls import path
from . import views

urlpatterns = [
    path('blacklist/', views.catalogblacklist, name='catalogblacklist'),
    path('review/', views.catalogreview, name='catalogreview'),
    path('', views.catalog, name='catalog'),
]