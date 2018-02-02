from django.contrib import admin

from . import models


class AnimalAdmin(admin.ModelAdmin):
    # todo: add method for transferring a group of animals to a different location. Add current location field
    list_display = ('name', 'species', 'date_of_birth')
    search_fields = ('name',)
    readonly_fields = ('ancestors', 'descendants')

    @staticmethod
    def ancestors(obj):
        return ", ".join([i for i in obj.get_all_ancestors()[:-1]])

    @staticmethod
    def descendants(obj):
        return ", ".join([i['name'] for i in obj.get_all_descendants() if i['name'] != obj.name])

admin.site.register(models.Animal, AnimalAdmin)


admin.site.register(models.Species)
admin.site.register(models.Location)
admin.site.register(models.Stay)
