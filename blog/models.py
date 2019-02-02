from django.db import models
from django.shortcuts import reverse
from django.db.models.signals import pre_save
from blogportfolio.utils import unique_slug_generator
from users.models import CustomUser
from mptt.models import MPTTModel, TreeForeignKey


from django.db.models import Q

# Create your models here.


class MyQuerySet(models.query.QuerySet):
    def search(self, query):
        lookups = (Q(title__icontains=query) |
                   Q(tags__title__icontains=query) |
                   Q(content__icontains=query))
        return self.filter(lookups).distinct()



class DjangoPostManager(models.Manager):
    def get_queryset(self):
        return MyQuerySet(self.model, using=self.db).filter(category='D')

    def search(self, *args):
        return self.get_queryset().search(*args)


class LifestylePostManager(models.Manager):
    def get_queryset(self):
        return MyQuerySet(self.model, using=self.db).filter(category='L')
    def search(self, *args):
        return self.get_queryset().search(*args)

class Tag(models.Model):
    title = models.CharField(max_length=120)
    active = models.BooleanField(default=True)


    def __str__(self):
        return self.title

class Post(models.Model):
    CATEGORY_CHOICES = (
        ('D', 'Django'),
        ('L', 'Lifestyle'),
    )
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    title = models.CharField(max_length=115)
    category = models.CharField(max_length=1, choices=CATEGORY_CHOICES)
    slug = models.SlugField(blank=True, unique=True)
    tags = models.ManyToManyField(Tag, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    django_posts = DjangoPostManager()
    lifestyle_posts = LifestylePostManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        if self.category == 'L':
            return reverse('post_detail_lifestyle', args=[self.slug])
        else:
            return reverse('post_detail_django', args=[self.slug])

class Comment(MPTTModel):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    comment_content = models.TextField(blank=False)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name="children")
    date_posted = models.DateTimeField(auto_now_add=True)

    class MPTTMeta:

        order_insertion_by = ['date_posted']





def tag_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(tag_pre_save_receiver, sender=Tag)


def tag_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(tag_pre_save_receiver, sender=Post)





