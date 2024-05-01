import json
from django.test import TestCase, Client
from django.urls import reverse
from myapp.views import signup, login, to_do_list, filter_tasks, remaining_time, list_saved_files, save_task
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from datetime import datetime, timedelta

class SignUpTestCase(TestCase):
    def test_signup(self):
        client = Client()
        url = reverse('signup')
        data = {
            'username': 'test_user',
            'password': 'test_password'
        }
        response = client.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.data)
        print("Test 'test_signup' is successful")

class LoginTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test_user', password='test_password')

    def test_login(self):
        client = Client()
        url = reverse('login')
        data = {
            'username': 'test_user',
            'password': 'test_password'
        }
        response = client.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 302)
        print("Test 'test_login' is successful")

class ToDoListTestCase(TestCase):
    def test_to_do_list(self):
        client = Client()
        url = reverse('task-list')
        response = client.get(url)
        self.assertEqual(response.status_code, 200)
        print("Test 'test_to_do_list' is successful")

    def test_to_do_list_post(self):
        client = Client()
        url = reverse('task-list')
        data = {
            'task_name': 'Test Task',
            'description': 'This is a test task.',
            'status': 'Pending',
            'priority': 'High',
            'due_date': (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')
        }
        response = client.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        print("Test 'test_to_do_list_post' is successful")

    def test_to_do_list_put(self):
        client = Client()
        url = reverse('task-list')
        data = {'task_name': 'Test Task'}
        response = client.put(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        print("Test 'test_to_do_list_put' is successful")

    def test_to_do_list_delete(self):
        client = Client()
        url = reverse('task-list')
        data = {'task_name': 'Test Task'}
        response = client.delete(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        print("Test 'test_to_do_list_delete' is successful")

class FilterTasksTestCase(TestCase):
    def test_filter_tasks(self):
        tasks = {
            'task1.json': {'task_name': 'Task 1', 'description': 'Task 1 Description', 'status': 'Pending', 'priority': 'Low'},
            'task2.json': {'task_name': 'Task 2', 'description': 'Task 2 Description', 'status': 'Completed', 'priority': 'High'},
            'task3.json': {'task_name': 'Task 3', 'description': 'Task 3 Description', 'status': 'In Progress', 'priority': 'Medium'},
        }
        filtered_tasks = filter_tasks(tasks, status='Pending')
        self.assertEqual(len(filtered_tasks), 1)
        print("Test 'test_filter_tasks' is successful")

class RemainingTimeTestCase(TestCase):
    def test_remaining_time(self):
        due_date = datetime.now() + timedelta(days=5)
        remaining_days = remaining_time(due_date.date())
        self.assertEqual(remaining_days, 5)
        print("Test 'test_remaining_time' is successful")

class ListSavedFilesTestCase(TestCase):
    def test_list_saved_files(self):
        tasks = list_saved_files()
        self.assertIsInstance(tasks, dict)
        print("Test 'test_list_saved_files' is successful")

class SaveTaskTestCase(TestCase):
    def test_save_task(self):
        task_name = 'Test Task'
        task_data = {
            'task_name': task_name,
            'description': 'This is a test task.',
            'status': 'Pending',
            'priority': 'High',
            'due_date': (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')
        }
        success, message = save_task(task_name, task_data)
        self.assertTrue(success)
        print("Test 'test_save_task' is successful")

if __name__ == '__main__':
    import unittest
    unittest.main()
