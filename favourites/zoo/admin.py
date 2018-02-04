from django import forms
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.shortcuts import render

from . import models, models_sql


class AnimalAdmin(admin.ModelAdmin):
    list_display = ('name', 'species', 'date_of_birth')
    search_fields = ('name',)
    readonly_fields = ('ancestors', 'descendants')
    actions = ['move_to_location']

    @staticmethod
    def ancestors(obj):
        return ", ".join([i for i in obj.get_all_ancestors()[:-1]])

    @staticmethod
    def descendants(obj):
        return ", ".join([i['name'] for i in obj.get_all_descendants() if i['name'] != obj.name])

    class MoveToLocationForm(forms.Form):
        _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
        location = forms.ModelChoiceField(queryset=models.Location.objects.all(), label="location")
        start = forms.DateField()

    def move_to_location(self, request, queryset):
        form = None
        if 'apply' in request.POST:
            form = self.MoveToLocationForm(request.POST)

            if form.is_valid():
                location = form.cleaned_data["location"]
                start = form.cleaned_data["start"]
                for animal in queryset:
                    m = models.Stay.objects.create(
                        animal=animal,
                        location=location,
                        start=start)
                    m.save()
                self.message_user(
                    request, "Moved {n} animals to location {loc}".format(n=queryset.count(), loc=location))
            return HttpResponseRedirect(request.get_full_path())
        if not form:
            form = self.MoveToLocationForm(
                initial={'_selected_action': request.POST.getlist(admin.ACTION_CHECKBOX_NAME)})
        return render(request,
                      'admin/move_to_location.html',
                      context={"animals": queryset, "form": form, "path": request.get_full_path()})
    move_to_location.short_description = "Move animals to location"

admin.site.register(models.Animal, AnimalAdmin)


admin.site.register(models.Species)
admin.site.register(models.Location)
admin.site.register(models.Stay)


class StaysWithEndDateAdmin(admin.ModelAdmin):
    readonly_fields = ('id', 'stay', 'animal', 'animal_name', 'location', 'location_name', 'start', 'end')
admin.site.register(models_sql.StaysWithEndDate, StaysWithEndDateAdmin)
