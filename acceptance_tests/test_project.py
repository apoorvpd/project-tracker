from django.test import TestCase
from django.test import Client
from tracker_app.models import Developer, Manager, Project

class ProjectCreateTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.manager1 = Manager.objects.create(username='manager1', password='password')

    def test_valid_project_creation(self):
        response = self.client.post('/', {'username': 'manager1', 'password': 'password'})
        self.assertEqual(response.url, '/projects/')

        response = self.client.get('/projects/')
        add_project_response = self.client.post('/projects/', {'name': 'Great Project', 'priority': 'High'})
        self.assertEqual(len(list(add_project_response.context['projects'])), 1)




