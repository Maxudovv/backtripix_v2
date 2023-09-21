import uuid

from PIL import ImageOps


def upload_to(instance, filename):
    from auth.models.user import User

    ext = filename.split(".")[-1]
    filename = str(uuid.uuid4()) + f".{ext}"
    if isinstance(instance, User):
        return f"users/avatars/{filename}"


class RemoveExifData(object):
    """Custom ImageKit Processor"""

    def process(self, image):
        # Return image copy without exif data.
        # Possible orientation values can be found here:
        # https://sirv.com/help/articles/rotate-photos-to-be-upright/
        orientation_value = image.getexif().get(274)

        if orientation_value is None:
            return image.copy()

        is_mirrored = orientation_value % 2 == 0
        if orientation_value in (3, 4):
            degrees = 180
        elif orientation_value in (5, 6):
            degrees = 90
        elif orientation_value in (7, 8):
            degrees = 270
        else:
            degrees = 0

        if is_mirrored:
            image = ImageOps.mirror(image)
        image = image.rotate(degrees)

        return image.copy()
