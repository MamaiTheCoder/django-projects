from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from .fields import OrderField
# Create your models here.

class Subject(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    
    class Meta:
        ordering = ['title']
    
    def __str__(self):
        return self.title

class Course(models.Model):
    owner = models.ForeignKey(
        User,
        related_name='courses_created',
        on_delete=models.CASCADE
    )
    subject = models.ForeignKey(
        Subject,
        related_name='courses',
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    overview = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created']
    
    def __str__(self):
        return self.title

class Module(models.Model):
    course = models.ForeignKey(
        Course,
        related_name='modules',
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    # The order for a new module will be assigned by
    # adding 1 to the last module of the same Course object.
    order = OrderField(blank=True, for_fields=['course'])
    
    def __str__(self):
        return f'{self.order}. {self.title}'
    
    class Meta:
        ordering = ['order']

class Content(models.Model):
    module = models.ForeignKey(
        Module,
        related_name='contents',
        on_delete=models.CASCADE
    )
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        # limit the ContentType objects that can be used for the 
        # generic relation. You use the model__in field lookup 
        # to filter the query to the ContentType objects with 
        # a model attribute that is 'text', 'video', 'image', or 'file'.
        limit_choices_to={
            'models__in': ('text', 'video', 'image', 'file')
        }
    )
    object_id = models.PositiveBigIntegerField()
    item = GenericForeignKey('content_type', 'object_id')
    order = OrderField(blank=True, for_fields=['module'])
    
    class Meta:
        ordering = ['order']

class ItemBase(models.Model):
    owner = models.ForeignKey(
        User,
        related_name='%(class)s_related',
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True
    
    def __str__(self):
        return self.title

class Text(ItemBase):
    content = models.TextField()

class File(ItemBase):
    content = models.FileField(upload_to='files')

class Image(ItemBase):
    content = models.FileField(upload_to='images')

class Video(ItemBase):
    content = models.URLField()

