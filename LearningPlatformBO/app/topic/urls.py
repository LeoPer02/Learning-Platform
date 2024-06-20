from django.urls import path
from .views import (
    TopicViewSet, TopicItemViewSet, ForumViewSet, 
    QuestionViewSet, QuestionAttachmentViewSet
)
from core.utilities.types import URLPatternsList

urlpatterns: URLPatternsList = [
    path('topics/', TopicViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='topic-list'),
    path('topics/<int:pk>/', TopicViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    }), name='topic-detail'),

    path('topic-items/', TopicItemViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='topicitem-list'),
    path('topic-items/<int:pk>/', TopicItemViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    }), name='topicitem-detail'),

    path('forums/', ForumViewSet.as_view({
        'post': 'create'
    }), name='forum-list'),
    path('forums/<int:pk>/', ForumViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    }), name='forum-detail'),

    path('questions/', QuestionViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='question-list'),
    path('questions/<int:pk>/', QuestionViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    }), name='question-detail'),

    path('question-attachments/<int:pk>/', QuestionAttachmentViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    }), name='questionattachment-detail'),
]