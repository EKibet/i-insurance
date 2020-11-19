from django.contrib import admin
from .models import User,Policy,AdminProfile,AgentProfile,UserProfile,Category


admin.site.register(User)
admin.site.register(Policy)
admin.site.register(AdminProfile)
admin.site.register(AgentProfile)
admin.site.register(UserProfile)
admin.site.register(Category)



