from django.db import models
from django.conf import settings
from core.extensions.models.base_abstract_model import BaseAbstractModel

class Topic(models.Model):
    course = models.ForeignKey('course.Course', on_delete=models.CASCADE, related_name='topics')
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='created_topics', on_delete=models.SET_NULL, null=True, blank=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='updated_topics', on_delete=models.SET_NULL, null=True, blank=True)
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

class TopicItem(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='items')
    file = models.FileField(upload_to='topic_items/')
    added_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='created_topic_items', on_delete=models.SET_NULL, null=True, blank=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='updated_topics_items', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Item for {self.topic.title}"
    
class Forum(models.Model):
    course = models.ForeignKey('course.Course', on_delete=models.CASCADE, related_name='forums')
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='created_forums', on_delete=models.SET_NULL, null=True, blank=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='updated_forums', on_delete=models.SET_NULL, null=True, blank=True)
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

class Question(models.Model):
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE, related_name='questions')
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='created_questions', on_delete=models.SET_NULL, null=True, blank=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='updated_questions', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.title

class QuestionAttachment(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='question_attachments/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='uploaded_attachments', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Attachment for {self.question.title}"