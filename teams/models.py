from django.db import models
from django.contrib.auth.models import User
from organisation.models import Department
from reports.models import Project


class Team(models.Model):
    name = models.CharField(max_length=100)
    team_type = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=50, default="Active")
    created_at = models.DateTimeField(auto_now_add=True)

    team_leader = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="leading_teams")
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    skills = models.TextField(blank=True)
    
    def __str__(self):
        return self.name


class TeamMember(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    role_in_team = models.CharField(max_length=100, default="Engineer")
    skills = models.TextField(blank=True)
    hire_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.team.name}"


class Dependency(models.Model):
    dependency_type = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    upstream_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="upstream_dependencies")
    downstream_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="downstream_dependencies")

    def __str__(self):
        return f"{self.upstream_team.name} → {self.downstream_team.name}"


class ContactChannel(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    channel_name = models.CharField(max_length=100)
    channel_type = models.CharField(max_length=100)
    is_private = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.team.name} - {self.channel_name}"


class Meeting(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    date_time = models.DateTimeField()
    platform = models.CharField(max_length=100)
    agenda = models.TextField(blank=True)
    schedule_type = models.CharField(max_length=50)

    def __str__(self):
        return f"Meeting for {self.team.name} on {self.date_time}"
