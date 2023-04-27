from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField #진형추가
from ckeditor.fields import RichTextField #진형추가
from django.utils import timezone #진형추가
from django.urls import reverse

class Member(models.Model):
    email = models.TextField(primary_key=True) 
    name = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    rdate = models.DateTimeField(default=timezone.now())
    dept = models.CharField(max_length=10)
    fire = models.CharField(max_length=2)
    classnames = models.ForeignKey('ClassNames', on_delete=models.CASCADE)
    
class Categories(models.Model):
    Cat_name = models.CharField(primary_key=True, max_length=20)
    Cat_info = models.TextField()
    
class ClassNames(models.Model):
    classnames = models.CharField(primary_key=True, max_length=30)
    
from uuid import uuid4

def get_file_path(instance, filename):
    uuid_name = uuid4().hex
    return uuid_name

class Post(models.Model):
    title = models.CharField(max_length=100)
    date = models.DateTimeField(default=timezone.now())
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    author = models.ForeignKey(Member, on_delete=models.CASCADE)
    body = RichTextUploadingField()
    file = models.FileField(upload_to=get_file_path, null=True, blank=True, verbose_name='파일')
    filename = models.CharField(max_length=64, null=True, verbose_name='첨부파일명')
    viewcount = models.PositiveIntegerField(default=0)
    post_fix = models.BooleanField(default=False)
    post_like = models.PositiveIntegerField(default=0)
    
class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    @property
    def get_html_url(self):
        url = reverse('event_edit', args=(self.id,))
        return f'<a href="{url}"> {self.title} </a>'

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    comment_date = models.DateTimeField(default=timezone.now)
    comment_user = models.ForeignKey(Member, on_delete=models.CASCADE)
    comment_text = models.TextField()
    
class Like(models.Model):
    like_user =models.ForeignKey(Member, on_delete=models.CASCADE)
    like_post =models.ForeignKey(Post, on_delete=models.CASCADE)