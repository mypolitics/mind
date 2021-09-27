from django.db import models


class Voting(models.Model):
    id = models.CharField(primary_key=True, max_length=55, blank=True)
    topic = models.CharField(max_length=255)
    form = models.CharField(max_length=255)
    date = models.DateField(null=True)
    sitting = models.PositiveIntegerField()
    voting = models.PositiveIntegerField()
    results = models.JSONField()

    class Meta:
        ordering = ['-sitting', '-voting']
