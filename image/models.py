import datetime
import os
from uuid import uuid4

from django.db import models
from django.utils.deconstruct import deconstructible

from nickname.models import Nickname


class TimeStampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


@deconstructible
class PathAndRename(object):

    def __init__(self, sub_path):
        self.path = sub_path

    def __call__(self, instance, file_name):
        now = datetime.datetime.now()
        name = file_name.split('.')[0]
        ext = file_name.split('.')[-1]

        file_name = '{}.{}'.format(now.strftime("%Y%m%d%H%M") + name, ext)

        file_path = self.path
        return os.path.join(file_path, file_name)


raw_image_path = PathAndRename("faces/raw")


class Image(TimeStampedModel):
    image = models.ImageField(upload_to=raw_image_path, height_field="height_field", width_field="width_field")
    info = models.CharField(max_length=200, default="", blank=True)
    height_field = models.IntegerField(null=True, default=0)
    width_field = models.IntegerField(null=True, default=0)

    @staticmethod
    def create_image(image_file):
        new_image = Image.objects.create(image=image_file)
        new_image.save()

        return new_image


class ExtractedImage(TimeStampedModel):
    image = models.ImageField(upload_to='not_used', height_field="height_field", width_field="width_field")
    origin_image = models.ForeignKey(Image, default=None, on_delete=models.SET_NULL, null=True)
    nickname = models.ForeignKey(Nickname, default=None, on_delete=models.SET_NULL, null=True)
    height_field = models.IntegerField(null=True, default=0)
    width_field = models.IntegerField(null=True, default=0)

    @staticmethod
    def create_image(image_file):
        new_image = Image.objects.create(image=image_file)
        new_image.save()

        return new_image

    @staticmethod
    def get_image_by_nickname(nickname):
        image = Image.objects.filter(nickname=nickname)

        return image
