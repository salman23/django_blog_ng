from django.shortcuts import render
import models
from django.views.generic import ListView


# Create your views here.

class PostListView(ListView):
    model = models.Post
    context_object_name = 'post_list'
    paginate_by = 10