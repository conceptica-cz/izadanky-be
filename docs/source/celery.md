# Celery tasks

For background tasks, Celery is used. Redis is used as a broker.

Application have background tasks for:
: - updating some models (references, patients, cares) from iCiselniky API. See {mod}`updates.tasks`
  - getting patients from UNIS API.   See {mod}`requisitions.tasks`

## Celery Beat

For periodic tasks, [Django Celery Beat](https://github.com/celery/django-celery-beat) is used.

Tasks are available through the Django admin interface.

Use {ref}`create_beat` management command to create the needed tasks initially.
