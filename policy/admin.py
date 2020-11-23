from django.contrib import admin
t
from django.contrib.auth.admin import UserAdmin
from . models import Category, Policy, UserManager, User, UserProfile, AdminProfile, AgentProfile


# register your models here
admin.site.register(AgentProfile)
admin.site.register(AdminProfile)
admin.site.register(UserProfile)
admin.site.register(Policy)
admin.site.register(Category)
admin.site.register(User)



