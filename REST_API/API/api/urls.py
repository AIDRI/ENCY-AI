from django.urls import path
from .views import TextSummarizerView

urlpatterns = [
    path('text_summarizer/', TextSummarizerView.as_view())
]