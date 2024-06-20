from modeltranslation.translator import TranslationOptions, register
from jobs import models


@register(models.JobsModel)
class JobsModelTranslation(TranslationOptions):
    fields = ("title","description")
