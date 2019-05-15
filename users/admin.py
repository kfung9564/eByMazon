from django.contrib import admin
from .models import Profile, UserApplication, UserBlacklist, UserMessages

# Register your models here.

admin.site.register(Profile)
admin.site.register(UserApplication)
admin.site.register(UserBlacklist)
admin.site.register(UserMessages)