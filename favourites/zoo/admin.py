from django.contrib import admin

from . import models

admin.site.register(models.Animal)
admin.site.register(models.Species)
admin.site.register(models.Location)
admin.site.register(models.Stay)
