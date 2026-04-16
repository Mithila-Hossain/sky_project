from django.db import models


class Project(models.Model):
    jira_project_name = models.CharField(max_length=200)
    jira_board_link = models.URLField(max_length=300)
    repo_url = models.URLField(max_length=300, unique=True)
    work_stream = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.jira_project_name
