from django.db import models
from core.extensions.models.base_abstract_model import BaseAbstractModel
from course.models import Course

class Forum(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='forums')
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Post(models.Model):
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Attachment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='post_attachments/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Attachment for {self.post.title}"
    