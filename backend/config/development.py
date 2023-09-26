import os

from common.utils import str2bool

from .settings import *  # noqa: F403
from .settings import INSTALLED_APPS, MIDDLEWARE

ALLOWED_HOSTS = ["*"]

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(ROOT_DIR, "tripix-storage")  # noqa: F405

# --- Django-silk ---
DJANGO_SILK_ENABLED = str2bool(os.getenv("DJANGO_SILK_ENABLED", "False"))
if DJANGO_SILK_ENABLED:
    MIDDLEWARE += ["silk.middleware.SilkyMiddleware"]
    INSTALLED_APPS += ["silk"]
