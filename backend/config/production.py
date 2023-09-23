import os  # noqa

from common.utils import str2bool

from .settings import *  # noqa

DEBUG = str2bool(os.getenv("DEBUG", "false"))
# Amazon s3
AWS_S3_REGION_NAME = os.getenv("AWS_REGION_NAME")
AWS_DEFAULT_ACL = None
AWS_AUTO_CREATE_BUCKET = False

AWS_S3_OBJECT_PARAMETERS = {"CacheControl": "max-age=86400"}
AWS_S3_SIGNATURE_VERSION = "s3v4"

AWS_S3_ACCESS_KEY_ID = os.getenv("AWS_S3_ACCESS_KEY_ID")
AWS_S3_SECRET_ACCESS_KEY = os.getenv("AWS_S3_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = os.getenv("AWS_BUCKET_NAME")
AWS_S3_CUSTOM_DOMAIN = "%s.s3.%s.amazonaws.com" % (
    AWS_STORAGE_BUCKET_NAME,
    AWS_S3_REGION_NAME,
)
AWS_LOCATION = "media"

MEDIA_ROOT = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)
