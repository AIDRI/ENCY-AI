from rest_framework import serializers, generics
from rest_framework.permissions import AllowAny
from API.models import TextSummarizer
from .serializers import TextSummarizerSerializer


class TextSummarizerView(generics.CreateAPIView):
    queryset = TextSummarizer.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = TextSummarizerSerializer