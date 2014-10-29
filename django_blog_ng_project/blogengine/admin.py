from django.contrib import admin
from models import Post

# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'pub_date', 'text')
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(Post, PostAdmin)