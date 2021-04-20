from django.shortcuts import render, redirect
from django.views import View
from tracker_app.models import Manager, Project, Developer


# Create your views here.

class Home(View):
    def get(self, request):
        #  For the get method of home, clear the current user as the first line of code. So going to the home page (via get) is equivalent to logging out.
        request.session.pop("username", None)
        return render(request, "main/home.html", {})

    def post(self, request):
        try:
            manager = Manager.objects.get(username=request.POST['username'])
        except Manager.DoesNotExist:
            return render(request, "main/home.html", {'error': 'Something went wrong..'})

        if manager.password == request.POST['password']:
            request.session["username"] = request.POST["username"]
            return redirect('projects')

        return render(request, "main/home.html", {'error': 'username/password incorrect'})


class ProjectView(View):
    def get(self, request):
        #  On the project page, only display the project owned by the current user. When a project is added, give it a foreign key of the current user
        if not request.session.get("username"):
            return redirect("home")

        projects = Project.objects.filter(project_manager__username=request.session.get('username'))
        print(projects)
        return render(request, "main/project.html", {"projects": projects})

    def post(self, request):
        project_name = request.POST['name']
        project_priority = request.POST['priority']
        print(project_name, project_priority)

        if project_name != '' or project_priority != '':
            Project.objects.create(name=project_name, priority=project_priority,
                                   project_manager=Manager.objects.get(username=request.session['username']))

        projects = Project.objects.filter(project_manager__username=request.session.get('username'))
        return render(request, "main/project.html", {"projects": projects})


class AssignView(View):
    def get(self, request):
        if not request.session.get("username"):
            return redirect("home")

        projects = Project.objects.filter(project_manager__username=request.session.get('username'))
        developers = Developer.objects.all()
        return render(request, "main/assign.html", {"projects": projects, "developers": developers})

    def post(self, request):
        project_name = request.POST['name']
        project_priority = request.POST['priority']
        project_developers = request.POST.getlist('developers')
        print(project_name, project_priority, project_developers)

        projects = Project.objects.filter(project_manager__username=request.session.get('username'))
        developers = Developer.objects.all()

        new_project = Project.objects.create(name=project_name, priority=project_priority,
                                             project_manager=Manager.objects.get(username=request.session['username']))
        for dev in project_developers:
            new_project.developer.add(Developer.objects.get(username=dev))

        new_project.save()
        return render(request, "main/assign.html", {"projects": projects, "developers": developers})

