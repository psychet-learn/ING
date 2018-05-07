from django.contrib import admin

from .models import Image, ExtractedImage

admin.site.register(ExtractedImage)
admin.site.register(Image)
