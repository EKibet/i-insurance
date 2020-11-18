from django.contrib import admin
from .models import User, Category, Policy,AdminProfile,UserProfile,AgentProfile
from django.contrib.auth.admin import UserAdmin



# Register your models here.
admin.site.register(User)
admin.site.register(AdminProfile)
admin.site.register(Category)
admin.site.register(Policy)
admin.site.register(UserProfile)
admin.site.register(AgentProfile)

