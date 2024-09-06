from django.urls import path
from .views import * # Certifique-se de que a importação está correta

urlpatterns = [
    path('webhook/', webhook, name='webhook'),
    path('chat/', chat, name='chat'),
    path('ia/<str:session_id>/chat/', gemini, name='gemini'),
]
