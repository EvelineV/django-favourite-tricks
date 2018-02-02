from django.db import models


class Species(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = 'species'

    def __str__(self):
        return self.name


class Animal(models.Model):
    species = models.ForeignKey(Species, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, unique=True)
    date_of_birth = models.DateField(blank=False, null=False)
    mother = models.ForeignKey('self', blank=True, null=True, on_delete=models.CASCADE, related_name='children')

    def __str__(self):
        return "{}: {}".format(self.species.name, self.name)


class Location(models.Model):
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
