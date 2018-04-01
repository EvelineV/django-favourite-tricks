# pylint: disable=attribute-defined-outside-init

from datetime import datetime, timedelta
import pytest
from model_mommy import mommy
from django.test import TestCase
from django.utils import timezone

from favourites.zoo import models, models_sql

pytestmark = pytest.mark.django_db


class TestSQLViews(TestCase):
    """Test that the SQL view StaysWithEndDate gives correct dates"""
    def setUp(self):
        mommy.make("Species", name="elephant")
        dolphin = mommy.make("Species", name="dolphin")

        self.aquarium = mommy.make("Location", name="aquarium", possible_occupants=[dolphin])
        self.sea = mommy.make("Location", name="the wide open sea", possible_occupants=[dolphin])

        self.flipper_birth_date = (timezone.now()-timedelta(days=6*365)).date()
        self.flipper = mommy.make("Animal", species=dolphin, name="Flipper", date_of_birth=self.flipper_birth_date)
        self.skipper_birth_date = (timezone.now()-timedelta(days=3*365)).date()
        self.skipper = mommy.make("Animal", species=dolphin, name="Skipper", date_of_birth=self.skipper_birth_date, mother=self.flipper)

        mommy.make("Stay", animal=self.flipper, location=self.sea, start=(timezone.now()-timedelta(days=10*365)).date())
        self.flipper_got_caught = (timezone.now() - timedelta(days=4*365)).date()
        mommy.make("Stay", animal=self.flipper, location=self.aquarium, start=self.flipper_got_caught)
        mommy.make("Stay", animal=self.skipper, location=self.aquarium, start=self.flipper_got_caught)

    def test_stay_starts_not_earlier_than_birth(self):
        skipper_stay = models.Stay.objects.filter(animal=self.skipper)
        self.assertEqual(len(skipper_stay), 1)
        self.assertEqual(skipper_stay[0].start, self.skipper_birth_date)

    def test_stays_with_end_date_sql_view(self):
        flipper_stays = models_sql.StaysWithEndDate.objects.filter(animal=self.flipper).order_by('start')
        flipper_in_sea = flipper_stays[0]
        self.assertEqual(flipper_in_sea.location, self.sea)
        self.assertEqual(flipper_in_sea.start, self.flipper_birth_date)
        self.assertEqual(flipper_in_sea.end, self.flipper_got_caught)
        flipper_caught = flipper_stays[1]
        self.assertEqual(flipper_caught.location, self.aquarium)
        self.assertEqual(flipper_caught.start, self.flipper_got_caught)
        self.assertEqual(flipper_caught.end, None)
