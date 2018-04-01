# pylint: disable=attribute-defined-outside-init

import pytest
from model_mommy import mommy
from django.test import TestCase

pytestmark = pytest.mark.django_db


class TestModels(TestCase):
    def setUp(self):
        mommy.make("Species", name="elephant")

    def test_dummy(self):
        pass

    def test_dummy_fail(self):
        raise Exception
