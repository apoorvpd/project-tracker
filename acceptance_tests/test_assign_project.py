from django.test import TestCase
from django.test import Client
from tracker_app.models import Developer, Manager, Project

class ProjectCreateTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.manager1 = Manager.objects.create(username='manager1', password='password')
        self.project1 = Project.objects.create(name='Great Project', description='Very good',
                                               priority='High', project_manager=self.manager1)

        self.developer1 = Developer.objects.create(username='spiderman', project_manager=self.manager1)
        self.developer2 = Developer.objects.create(username='apoorv', project_manager=self.manager1)

    def test_valid_assign_project_access(self):
        response = self.client.post('/', {'username': 'manager1', 'password': 'password'})
        get_assign_response = self.client.get('/assign/')
        self.assertEqual(list(get_assign_response.context['projects']), [self.project1])

    def test_valid_assign_developers_access(self):
        response = self.client.post('/', {'username': 'manager1', 'password': 'password'})
        get_assign_response = self.client.get('/assign/')
        self.assertEqual(list(get_assign_response.context['developers']), [self.developer1, self.developer2])

    def test_invalid_assign_developers_to_project(self):
        response = self.client.post('/', {'username': 'manager1', 'password': 'password'})
        post_assign_response = self.client.post('/assign/', {'name': self.project1.name, 'priority': self.project1.priority, 'developers': []})
        print(post_assign_response.context['message'])
        self.assertEqual(post_assign_response.context['message'], 'Not Saved and Assigned Successfully')

    def test_valid_assign_developers_to_project(self):
        response = self.client.post('/', {'username': 'manager1', 'password': 'password'})
        post_assign_response = self.client.post('/assign/', {'name': self.project1.name, 'priority': self.project1.priority, 'developers': [self.developer1]})
        print(post_assign_response.context['message'])
        self.assertEqual(post_assign_response.context['message'], 'Project Saved and Assigned Successfully')

