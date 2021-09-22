import uuid

from django.db import models


# Create your models here.

class Members(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    name = models.CharField(max_length=255)
    electionDate = models.DateField()
    list = models.CharField(max_length=255)
    region = models.CharField(max_length=255)
    votes = models.PositiveBigIntegerField()
    pledge = models.DateField()
    experience = models.CharField(max_length=255)
    party = models.CharField(max_length=255)
    dateOfBirth = models.CharField(max_length=255, null=True)
    education = models.CharField(max_length=255, null=True)
    school = models.CharField(max_length=255, null=True)
    job = models.CharField(max_length=255, null=True)
    photoUrl = models.URLField(null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Members'
