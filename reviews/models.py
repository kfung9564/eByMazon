from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.validators import MaxValueValidator, MinValueValidator

class review(models.Model):
	title = models.CharField(null = False ,max_length = 100)
	ratings = models.IntegerField( validators=[MaxValueValidator(5), MinValueValidator(1)])
	target = models.ForeignKey(User, on_delete = models.CASCADE)
	content = models.TextField()
	date_posted = models.DateTimeField(default = timezone.now)


	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('review-detail', kwargs = {'pk': self.pk})