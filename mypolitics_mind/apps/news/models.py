import uuid

from django.db import models


# Create your models here.

class News(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    content = models.TextField()
    slug = models.SlugField()
    date = models.DateTimeField()
    image = models.JSONField()
    author = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-date']
        verbose_name_plural = 'News'
