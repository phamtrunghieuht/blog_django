from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from datetime import date
from django.utils.text import slugify
import uuid

# Create your models here.
class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField()

    def __str__(self):
        return self.user.username

class Category(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blog:category", args=[self.title])

class Post(models.Model):
    title = models.CharField(_('title'), max_length=255)
    slug = models.SlugField(max_length=254, unique=True, blank=True, editable=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='blog_posts')
    image = models.ImageField(_('image'), blank=True, null=True, upload_to='blog')
    text = RichTextField(_('text'))
    description = models.TextField(_('description'), blank=True, null=True)
    published = models.BooleanField(_('published'), default=False)
    categories = models.ManyToManyField(Category)
    created = models.DateTimeField(_('created'), auto_now_add=True)
    modified = models.DateTimeField(_('modified'), auto_now=True)
    pub_date = models.DateTimeField(_('publish date'), blank=True, null=True)
    featured = models.BooleanField(default=False)
    views = models.IntegerField(default=0)
    previous_post = models.ForeignKey('self', related_name='previous', on_delete=models.SET_NULL, blank=True, null=True)
    next_post = models.ForeignKey('self', related_name='next', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        
        self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("blog:post", args=[self.slug])

    class Meta:
        verbose_name = _('blog post')
        verbose_name_plural = _('blog posts')
        ordering = ['pub_date']
    @property
    def get_comment(self):
        return self.comments.all()    

class Comment(models.Model):
    username = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    published = models.BooleanField(default=True)

    def __str__(self):
        return self.username