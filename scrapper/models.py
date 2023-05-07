from django.db import models

# Create Article model
class Article(models.Model):
    url = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    content = models.TextField("Output", blank=True)
    published_at = models.TextField(blank=True)
    # published_at = models.DateTimeField(auto_now_add=True, null=True)

