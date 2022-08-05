import uuid

from django.utils.translation import gettext_lazy as _
from django.db import models

class Photo(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    title = models.TextField(default='', max_length=1024)
    photo = models.ImageField(upload_to='photos/')
    result = models.CharField(default='', max_length=1024)
    width = models.IntegerField(default=0)
    height = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('photo')
        verbose_name_plural = _('photos')

    def __str__(self):
        return self.title

    @classmethod
    def create_photo(cls, photo, title, width, height):
        new_photo = cls.objects.create(photo=photo, title=title, width=width, height=height)
        return new_photo
