from django.db import models


# Create your models here.
class Manager(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)

    def __str__(self):
        return self.username


class Developer(models.Model):
    username = models.CharField(max_length=50)
    project_manager = models.ForeignKey(Manager, on_delete=models.CASCADE)

    def __str__(self):
        return self.username


PRIORITY_CHOICES = (
    ("High", "High"),
    ("Low", "Low"),
    ("Medium", "Medium"),

)


class Project(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=50)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES)
    project_manager = models.ForeignKey(Manager, on_delete=models.CASCADE, null=True, blank=True, default='')
    developer = models.ManyToManyField(Developer)

    def __str__(self):
        return self.name