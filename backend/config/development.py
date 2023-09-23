import os

from .settings import *  # noqa: F403

ALLOWED_HOSTS = ["*"]

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(ROOT_DIR, "tripix-storage")  # noqa: F405
