from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import pre_save
from django.utils.safestring import mark_safe
from hitcount.models import HitCountMixin, HitCount
from django.contrib.contenttypes.fields import GenericRelation
from markdown_deux import markdown

from .utils import get_read_time


# Create your models here.
STATUS = (
    (0, 'Draft'),
    (1, 'Publish')
)


class Categories(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name


class Post(models.Model, HitCountMixin):
    image = models.ImageField(default='blogdefault.jpg')
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE,related_name='blog_posts')
    updated_on = models.DateTimeField(auto_now=True)
    content = models.TextField()
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    read_time = models.IntegerField(default=0)
    editors_pick = models.BooleanField(default=False)
    trending = models.BooleanField(default=False)
    hit_count_generic = GenericRelation(HitCount, object_id_field='object_pk',
                                        related_query_name='hit_count_generic_relation')

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title

    def get_markdown(self):
        content = self.content
        markdown_text = markdown(content)
        return mark_safe(markdown_text)


def read_time_calculator(sender, instance,  *args, **kwargs):
    if instance.content:
        html_string = instance.get_markdown()
        read_time_var = get_read_time(html_string)
        instance.read_time = read_time_var


pre_save.connect(read_time_calculator, sender=Post)


class CommentManager(models.Manager):
    """Model manager for `Comment` model."""

    def all(self):
        """Return results of instance with no parent (not a reply)."""
        qs = super().filter(parent=None)
        return qs


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    image = models.ImageField(default='user icon.png')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    website = models.CharField(max_length=200, null=True, blank=True)
    message = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)
    parent = models.ForeignKey('self', related_name='children', null=True, blank=True, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return 'Comment {} by {}'.format(self.message, self.name)

    def children(self):
        """Return replies of a comment."""
        return Comment.objects.filter(parent=self)

    @property
    def is_parent(self):
        """Return `True` if instance is a parent."""
        if self.parent is not None:
            return False
        return True



