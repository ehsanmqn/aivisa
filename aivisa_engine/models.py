import uuid

from django.db import models

class Photo(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    photo = models.ImageField(upload_to='images/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.photo
