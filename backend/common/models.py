from django.utils.translation import gettext_lazy as _


class LANGUAGE:
    EN = "en"
    RU = "ru"

    CHOICES = ((EN, _("English")), (RU, _("Russian")))
