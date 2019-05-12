from django.urls import path
from . import views

urlpatterns = [
    # path(URL_NAME, views.VIEW_NAME, HTML_FILE_NAME)

    path('blacklist/', views.catalogblacklist, name='catalogblacklist'),
    path('application/', views.catalogreview, name='catalogreview'),
    path('apply/', views.apply, name='itemapply'),
    path('', views.catalog, name='catalog'),
]