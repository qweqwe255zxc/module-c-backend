from django.db import models

from django.conf import settings


# Create your models here.

class Listing(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=80)
    description = models.CharField(max_length=500, blank=True, default='')
    price = models.PositiveIntegerField()
    image = models.ImageField(upload_to='listings/')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self) -> str:
        return self.title
