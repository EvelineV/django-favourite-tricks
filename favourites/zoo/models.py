from datetime import timedelta
from django.db import connection, models
from django.core.exceptions import ValidationError

from favourites.zoo import sql_methods
from favourites.zoo import utils


class Species(models.Model):
    name = models.CharField(max_length=255, unique=True, db_index=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = 'species'

    def __str__(self):
        return self.name


class Animal(models.Model):
    species = models.ForeignKey(Species, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, unique=True, db_index=True)
    date_of_birth = models.DateField(blank=False, null=False)
    mother = models.ForeignKey('self', blank=True, null=True, on_delete=models.CASCADE, related_name='children')

    def __str__(self):
        return "{}: {}".format(self.species.name, self.name)

    def get_all_descendants(self):
        with connection.cursor() as cursor:
            cursor.execute(sql_methods.get_list_of_descendants(self.name))
            result = utils.dict_fetch_all(cursor)
        return result

    def get_all_ancestors(self):
        with connection.cursor() as cursor:
            cursor.execute(sql_methods.get_list_of_ancestors(self.name))
            result = cursor.fetchall()[0][0]
        return result

    def save(self, *args, **kwargs):
        if self.date_of_birth < (self.mother.date_of_birth + timedelta(days=365)):
            # todo: make this a parameter for each species.
            raise ValidationError("An animal cannot be born when its mother was less than a year old.")
        super(Animal, self).save(*args, **kwargs)


class Location(models.Model):
    # todo: add validation that only possible occupants will actually end up here. We would not want an elephant in an aquarium.
    name = models.CharField(max_length=255, unique=True)
    possible_occupants = models.ManyToManyField(Species)

    def __str__(self):
        return self.name


class Stay(models.Model):
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    start = models.DateField(blank=False, null=False)

    def __str__(self):
        return "{}, {}: {}".format(self.location.name, self.animal.name, str(self.start))

    def save(self, *args, **kwargs):
        if self.start < self.animal.date_of_birth:
            self.start = self.animal.date_of_birth
        super(Stay, self).save(*args, **kwargs)
