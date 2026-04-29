from django.contrib import admin
from .models import Team, TeamMember, Dependency, ContactChannel, Meeting

admin.site.register(Team)
admin.site.register(TeamMember)
admin.site.register(Dependency)
admin.site.register(ContactChannel)
admin.site.register(Meeting)

# ⭐ ADD THIS BELOW — overrides how User appears in admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

# Unregister default User admin
admin.site.unregister(User)

# Custom User admin to show full names
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'get_full_name')

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    get_full_name.short_description = 'Full Name'

admin.site.register(User, CustomUserAdmin)

# Override how User appears in dropdowns
def user_str(self):
    full = f"{self.first_name} {self.last_name}".strip()
    return full if full else self.username

User.__str__ = user_str