# Generated by Django 2.0 on 2018-02-02 15:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('zoo', '0002_auto_20180202_1420'),
    ]

    operations = [
        migrations.RunSQL([
            """
            DROP VIEW IF EXISTS zoo_stays_with_end;
            CREATE VIEW zoo_stays_with_end AS (
            SELECT
                row_number() OVER () AS id,
                stay.id AS stay_id,
                animal.id AS animal_id,
                animal.name AS animal_name,
                location.id AS location_id,
                location.name AS location_name,
                stay.start,
                "end"
            FROM (
                SELECT *,
                LEAD(start) OVER (PARTITION BY animal_id ORDER BY start ASC) AS "end"
                FROM zoo_stay
            ) AS zoo_stays_with_end,
            zoo_animal AS animal,
            zoo_location AS location,
            zoo_stay AS stay
            WHERE zoo_stays_with_end.animal_id = animal.id
            AND zoo_stays_with_end.location_id = location.id
            AND zoo_stays_with_end.id = stay.id
            );
            """], [
            "DROP VIEW IF EXISTS zoo_stays_with_end"
        ])
    ]