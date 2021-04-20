from django.contrib import admin
from tracker_app.models import Manager, Developer, Project
# Register your models here.
admin.site.register(Manager)
admin.site.register(Developer)
admin.site.register(Project)
