from django.test import TestCase, LiveServerTestCase, Client
from django.utils import timezone
from blogengine.models import Post
import markdown
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
        # login page
        response = self.client.get('/admin/', follow=True)
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

    def test_create_post(self):
        # login
        self.client.login(username='ngtest', password='password')

        # check response code 
        response = self.client.get('/admin/blogengine/post/add/')
        self.assertEquals(response.status_code, 200)

        post = {
            'title': 'My first post',
            'text': 'This is a test post checking from the test.py',
            'pub_date_0': '2014-10-27',
            'pub_date_1': '06:57:26',
        }

        response = self.client.post('/admin/blogengine/post/add/', post, follow=True)

        self.assertEquals(response.status_code, 200)
        self.assertTrue('added successfully' in response.content)
        
        all_post = Post.objects.all()
        self.assertEquals(len(all_post), 1)


class PostViewTest(LiveServerTestCase):
    """docstring for PostViewTest"""
    def setUp(self):
        self.client = Client()

    def test_index(self):
        post = Post()
        post.title = 'My first post'
        post.text = 'This is [my first blog post](http://127.0.0.1:8000/blog/)',
        post.pub_date = timezone.now()
        post.save()
        all_post = Post.objects.all()
        self.assertEquals(len(all_post), 1)

        # fetch the index
        response = self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)

        # check the post title in response
        self.assertTrue(post.title in response.content)

        # check the post text in response
        self.assertTrue(markdown.markdown(post.text) in response.content)

        # check the post date year in response
        self.assertTrue(str(post.pub_date.year) in response.content)
        self.assertTrue(str(post.pub_date.day) in response.content)

        # check the link is markedup as properly
        self.assertTrue('<a href="http://127.0.0.1:8000/blog/">my first blog post</a>' in response.content)

