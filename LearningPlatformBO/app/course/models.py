from django.db import models
from core.extensions.models.base_abstract_model import BaseAbstractModel
from django.conf import settings
from topic.models import Topic

class Course(models.Model):
    title = models.CharField(max_length=255)
    visibility = models.CharField(max_length=50, choices=(('public', 'Public'), ('private', 'Private')))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Relationships
    enrolled_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='enrolled_courses')

    def __str__(self):
        return self.title
    
class CourseAdmin(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    is_admin = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'course')

    def __str__(self):
        return f"{self.user.get_full_name()} - Admin of {self.course.title}"

    @staticmethod
    def has_course_admin_permission(user, course):
        return CourseAdmin.objects.filter(user=user, course=course).exists()
        #, is_admin=True Add this when I create new database TODO
    

class EnrollmentRequest(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('denied', 'Denied'),
    )
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='enrollment_requests')
    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='enrollment_requests')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.course.title} ({self.status})"

    class Meta:
        unique_together = ('user', 'course')  # Prevent duplicate requests