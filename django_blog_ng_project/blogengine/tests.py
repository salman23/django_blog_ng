from django.test import TestCase, LiveServerTestCase, Client
from django.utils import timezone
from blogengine.models import Post
import markdown
from selenium import webdriver
from django.contrib.flatpages.models import FlatPage
from django.contrib.sites.models import Site
from django.contrib.auth.models import User

# Create your tests here.

class PostTest(TestCase):
    def test_create_post(self):
        # create a author
        author = User.objects.create_user('testuser', 'user@example.com', 'password')
        author.save()

        # create site
        site = Site()
        site.name = 'example.com'
        site.domain = 'example.com'
        site.save()

        # create a post
        post = Post()
        post.title = 'First test post'
        post.text = 'Fists test post body'
        post.pub_date = timezone.now()
        post.author = author
        post.site = site

        # save post
        post.save()
        all_post = Post.objects.all()
        self.assertEquals(len(all_post), 1)
        only_post = all_post[0]
        self.assertEquals(only_post, post)
        self.assertEqual(only_post.author.username, post.author.username)
        self.assertEquals(only_post.author.email, post.author.email)


class BaseAcceptanceTest(LiveServerTestCase):
    def setUp(self):
        self.client = Client()


class AdminTest(BaseAcceptanceTest):
    fixtures = ['users.json']

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
        response = self.client.get('/admin/', follow=True)
        self.assertEqual(response.status_code, 200)

        # check response code 
        response = self.client.get('/admin/blogengine/post/add/')
        self.assertEquals(response.status_code, 200)

        post = {
            'title': 'My first post',
            'text': 'This is a test post checking from the test.py',
            'pub_date': timezone.now(),
            'slug': 'my-first-post',
            'site': 1,
        }

        response = self.client.post('/admin/blogengine/post/add/', post, follow=True)
        self.assertEquals(response.status_code, 200)
        all_posts = Post.objects.all()
        self.assertEquals(len(all_posts), 1)

    def test_edit_post(self):
        # create author
        author = User.objects.create_user('testuser', 'user@example.com', 'password')
        author.save()

        # create site
        site = Site()
        site.name = 'example.com'
        site.domain = 'example.com'
        site.save()

        # create post
        post = Post()
        post.title = 'My first post',
        post.text = 'This is a test post checking from the test.py',
        post.pub_date = timezone.now()
        post.slug = 'my-first-post'
        post.author = author
        post.site = site
        post.save()

        # login
        self.client.login(username='ngtest', password='password')

        # edit the post
        new_post = {
            'title': 'My second post',
            'text': 'This is a test post checking the test.py',
            'pub_date': timezone.now(),
            'slug': 'my-second-post',
            'site': 1,
        }
        response = self.client.post('/admin/blogengine/post/1/', new_post, follow=True)
        #self.assertEquals(response.status_code, 200)
        #self.assertTrue('changed successfully' in response.content)

    def test_delete_post(self):
        # create the author
        author = User.objects.create_user('testuser', 'user@example.com', 'password')
        author.save()

        # create a site
        site = Site()
        site.name = 'example.com'
        site.domain = 'example.com'
        site.save()

        # create post
        post = Post()
        post.title = 'Delete Test'
        post.content = 'Test post for delete test'
        post.author = author
        post.pub_date = timezone.now()
        post.slug = 'delete-test'
        post.site = site
        post.save()

        # check the post is saved
        all_post = Post.objects.all()
        self.assertEquals(len(all_post), 1)
        only_post = all_post[0]

        # login
        self.client.login(username='ngtest', password='password')

        # delete post
        response = self.client.post('/admin/blogengine/post/1/delete/', dict(post='yes'), follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertTrue('deleted successfully' in response.content)
        all_post = Post.objects.all()
        self.assertNotEquals(len(all_post), 1)


class PostViewTest(BaseAcceptanceTest):
    """docstring for PostViewTest"""

    def test_index(self):
        # create author
        author = User.objects.create_user('testuser', 'user@example.com', 'password')
        author.save()

        # create a site
        site = Site()
        site.name = 'example.com'
        site.domain = 'example.com'
        site.save()

        # create post
        post = Post()
        post.title = 'My first post'
        post.text = 'This is [my first blog post](http://127.0.0.1:8000/)',
        post.pub_date = timezone.now()
        post.author = author
        post.site = site
        post.save()
        all_post = Post.objects.all()
        self.assertEquals(len(all_post), 1)

        # fetch the index
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

        # check the post title in response
        self.assertTrue(post.title in response.content)

        # check the post date year in response
        self.assertTrue(str(post.pub_date.year) in response.content)
        self.assertTrue(str(post.pub_date.day) in response.content)

        # check the link is markedup as properly
        self.assertTrue('<a href="http://127.0.0.1:8000/">my first blog post</a>' in response.content)

    def test_post_page(self):
        # create author
        author = User.objects.create_user('testuser', 'user@example.com', 'password')
        author.save()

        # create a site
        site = Site()
        site.name = 'example.com'
        site.domain = 'example.com'
        site.save()

        # create post
        post = Post()
        post.title = 'My first post'
        post.text = 'This is [my first blog post](http://127.0.0.1:8000/blog/)',
        post.pub_date = timezone.now()
        post.slug = 'my-first-post'
        post.author = author
        post.site = site
        post.save()
        all_post = Post.objects.all()
        only_post = all_post[0]

        # check post the post
        self.assertEquals(only_post, post)

        # check attributes
        self.assertEqual(only_post.title, 'My first post')
        self.assertEqual(only_post.slug, 'my-first-post')
        self.assertEqual(only_post.get_absolute_url(), '/2014/11/5/my-first-post/')

        # check post url
        post_url = only_post.get_absolute_url()
        response = self.client.get(post_url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(post.title in response.content)


class FlatPageViewTest(BaseAcceptanceTest):
    """
    Flat page app test class
    """

    def test_create_flat_page(self):
        # create a flat page
        page = FlatPage()
        page.url = '/about/'
        page.title = 'About me'
        page.content = 'All about me'
        page.save()
        page.sites.add(Site.objects.all()[0])
        page.save()

        # check the new page is saved
        all_pages = FlatPage.objects.all()
        self.assertEqual(len(all_pages), 1)
        only_page = all_pages[0]
        self.assertEqual(only_page, page)

        # check the data of the page
        self.assertEquals(only_page.url, page.url)
        self.assertEquals(only_page.title, page.title)
        self.assertEquals(only_page.content, page.content)

        # check the page url
        page_url = only_page.get_absolute_url()
        response = self.client.get(page_url)
        self.assertEquals(response.status_code, 200)

