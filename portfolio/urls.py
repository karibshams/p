from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/chat/', views.ai_chat, name='chat'),
    path('api/feedback/', views.submit_feedback, name='feedback'),
]
