from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
	ListView, 
	DetailView, 
	CreateView,
	UpdateView,
	DeleteView
	)
from .models import review

class ReviewListView(ListView):
	model = review
	template_name = 'reviews/home.html' #<app>/<model>_<viewtype>.html
	context_object_name = 'reviews'
	ordering = ['-date_posted']

class ReviewDetailView(DetailView):
	model = review

class ReviewCreateView(LoginRequiredMixin, CreateView):
	model = review
	fields = ['title', 'ratings', 'target', 'content']
	def form_valid(self,form):
		form.instance.target != self.request.user
		return super().form_valid(form)

# def about(request,*args, **kwargs):
# 	print(args, kwargs)
# 	return render(request, "reviews/about.html", {})