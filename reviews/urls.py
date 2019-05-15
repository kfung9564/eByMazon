from django.urls import path
from .views import (
	ReviewDetailView, 
	ReviewCreateView,
	ReviewListView
	)

from . import views


urlpatterns = [
	path('review/', ReviewListView.as_view(), name = 'review'),
	path('review/<int:pk>/', ReviewDetailView.as_view(), name = 'review-detail'),
	path('review/new/', ReviewCreateView.as_view(), name = 'review-create'),
]

#in project folder: urls.py add:
# from django.contrib import admin
# from django.contrib.auth import views as auth_views
# from django.conf import settings
# from django.conf.urls.static import static
# from django.urls import path, include
# from . import views 	
# path('r', include('reviews.urls')),