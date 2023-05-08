from django.db import models

# Create Article model
class Article(models.Model):
    url = models.CharField(max_length=200, blank=True, null=True)
    title = models.CharField(max_length=200, blank=True, null=True)
    author = models.CharField(max_length=200, blank=True, null=True)
    content = models.TextField("Output", blank=True, null=True)
    published_at = models.DateTimeField(auto_now_add=True, null=True)

