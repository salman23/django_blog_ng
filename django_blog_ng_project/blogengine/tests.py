from django.test import TestCase, LiveServerTestCase, Client
from django.utils import timezone
from blogengine.models import Post
from selenium import webdriver

# Create your tests here.

class PostTest(TestCase):
    def test_create_post(self):
        post = Post()
        post.title = 'First test post'
        post.text = 'Fists test post body'
        post.pub_date = timezone.now()
        post.save()
        all_post = Post.objects.all()
        self.assertEquals(len(all_post), 1)
        only_post = all_post[0]
        self.assertEquals(only_post, post)


class AdminTest(LiveServerTestCase):
    fixtures = ['users.json']

    def setUp(self):
        self.client = Client()
        

    def test_login(self):
        # before login
        response = self.client.get('/admin/')
        self.assertNotEqual(response.status_code, 200)

        # login page
        response = self.client.get('/admin/login/?next=/admin/')
        self.assertEquals(response.status_code, 200)
        self.assertEqual(isinstance(response.content, str), True)
        self.assertTrue('Log in' in response.content)
        
        # login
        login = self.client.login(username='ngtest', password="password")
        self.assertEqual(login, True)
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('Log out' in response.content)
    
    def test_logout(self):
        # login
        login = self.client.login(username='ngtest', password="password")
        self.assertEqual(login, True)
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 200)

        # logout 
        self.client.logout()
        response = self.client.get('/admin/')
        self.assertNotEquals(response.status_code, 200)