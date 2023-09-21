import os
from tempfile import SpooledTemporaryFile

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from storages.backends.s3boto3 import S3Boto3Storage


class StaticStorage(S3Boto3Storage):
    location = settings.STATIC_LOCATION
    default_acl = "public-read"
    querystring_auth = False


class MediaStorageBase(S3Boto3Storage):
    file_overwrite = False

    def _save(self, name, content):
        """
        We create a clone of the content file as when this is passed to
        boto3 it wrongly closes the file upon upload where as the storage
        backend expects it to still be open.
        """
        # Seek our content back to the start
        content.seek(0, os.SEEK_SET)

        # Create a temporary file that will write to disk after a specified
        # size. This file will be automatically deleted when closed by
        # boto3 or after exiting the `with` statement if the boto3 is fixed
        with SpooledTemporaryFile() as content_autoclose:
            # Write our original content into our copy that will be closed by boto3
            content_autoclose.write(content.read())

            # Upload the object which will auto close the
            # content_autoclose instance
            return super()._save(name, content_autoclose)


class PublicMediaStorage(MediaStorageBase):
    querystring_auth = False
    location = settings.PUBLIC_MEDIA_LOCATION
    default_acl = "public-read"


class TemporaryS3Storage(MediaStorageBase):
    location = settings.TEMPORARY_STORAGE_LOCATION
    default_acl = "private"
    custom_domain = False


class TemporaryFileStorage(FileSystemStorage):
    location = os.path.join(
        settings.TEMP_MEDIA_ROOT, settings.TEMPORARY_STORAGE_LOCATION
    )


class PrivateMediaStorage(MediaStorageBase):
    location = settings.PRIVATE_MEDIA_LOCATION
    default_acl = "private"
    custom_domain = False
