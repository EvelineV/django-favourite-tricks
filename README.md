# django-favourite-tricks
Small django project to show some tricks I like. Made with Django 2.0 inside a Docker environment.

Presented as a cookie talk at my workplace and at February 2018's Stockholm Django meetup.

## Topics
+ Use SQL views integrated with the ORM for recursive relationships or window functions.
+ Test examples
+ Admin batch actions

## Run
+ Install docker and docker-compose
+ Run `docker-compose build` and `docker-compose up django` in a terminal. The app will now be running on `localhost:8000/`

## Test
+ use `docker-compose run --rm django pytest favourites` to run the tests.

## Shell commands
+ use `docker-compose exec django python manage.py <<management_command>>` to use Django management commands.

## Security
+ Most of my work is still on Django 1.11 but I wanted to check out Django 2.0.
+ The secret key, debug and database settings should not be checked into the repo under normal circumstances.
+ The open port on the Postgres Docker container allows for connecting pgAdmin or dbVisualizer or similar tools. Do not do this in a production environment.
+ This is a project aimed at showing off some code, not to be run in production. Do not deploy unless you take care of the above issues.

## License
Do not use your new Django powers for evil. No restrictions otherwise.
