from django.contrib import admin
from .models import Team, TeamMember, Dependency, ContactChannel, Meeting

admin.site.register(Team)
admin.site.register(TeamMember)
admin.site.register(Dependency)
admin.site.register(ContactChannel)
admin.site.register(Meeting)
