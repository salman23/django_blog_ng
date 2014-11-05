from django.db import models
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
# Create your models here.


class Post(models.Model):
    title = models.CharField(max_length=200)
    pub_date = models.DateTimeField()
    text = models.TextField()
    slug = models.SlugField(max_length=250, unique=True)
    author = models.ForeignKey(User)
    site = models.ForeignKey(Site, default="1")

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        post_url = "/{}/{}/{}/{}/".format(self.pub_date.year, self.pub_date.month, self.pub_date.day, self.slug)
        return post_url

    class Meta:
        ordering = ["-pub_date"]