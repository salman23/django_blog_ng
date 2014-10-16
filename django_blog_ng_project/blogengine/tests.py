from django.test import TestCase, LiveServerTestCase, Client
from django.utils import timezone
from blogengine.models import Post

# Create your tests here.

class PostTest(TestCase):
    def test_create_test(self):
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
    def test_login(self):
        c = Client()
        response1 = c.get('/admin/')
        response2 = c.get('/admin/login/?next=/admin/')
        self.assertEqual(response1.status_code, 302)
        self.assertEqual(response2.status_code, 200)
        self.assertTrue('Log in' in response2.content)
        c.login(username='salman', password="2312")
        response = c.get('/admin/')
        self.assertEqual(response.status_code, 200)