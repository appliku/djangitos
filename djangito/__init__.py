try:
    from .celeryapp import app as celery_app
    __all__ = ('celery_app',)
except ModuleNotFoundError:
    print("Celery not installed, skipping")
