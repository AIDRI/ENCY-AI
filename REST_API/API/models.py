from django.db import models


class TextSummarizer(models.Model):
    text = models.CharField(max_length=100000)
