from django.db import models
from favourites.zoo import models as zoo_models


class StaysWithEndDate(models.Model):
    """
    This is a PostgreSQL view on the Stay, Location and Animal table. Do not use for writing.
    Definition in migration 3
    id field is just a row number - do not use for lookups! Necessary for Django though.
    """
    id = models.IntegerField(primary_key=True)
    stay = models.ForeignKey(zoo_models.Stay, on_delete=models.DO_NOTHING)
    location = models.ForeignKey(zoo_models.Location, on_delete=models.DO_NOTHING)
    location_name = models.CharField(max_length=255)
    animal = models.ForeignKey(zoo_models.Animal, on_delete=models.DO_NOTHING)
    animal_name = models.CharField(max_length=255)
    start = models.DateField()
    end = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'zoo_stays_with_end'

    def __str__(self):
        return "{} - {} ({}:{})".format(self.location_name, self.animal_name, self.start, self.end)
