from django.db import models


class TimeStampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(TimeStampedModel):
    id = models.IntegerField(primary_key=True)
    category = models.CharField(max_length=200)
    info = models.CharField(max_length=200, default="", null=True)

    def __str__(self):
        return self.category


class Nickname(TimeStampedModel):
    nickname = models.CharField(max_length=200)
    category = models.ForeignKey(Category, default=None, on_delete=models.SET_NULL, null=True)
    info = models.CharField(max_length=200, default="", null=True)

    def __str__(self):
        return self.nickname
