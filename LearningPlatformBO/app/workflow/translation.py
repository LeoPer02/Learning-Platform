from modeltranslation.translator import TranslationOptions, register
from workflow import models


@register(models.TestModel)
class TestModelTranslation(TranslationOptions):
    fields = ("name",)
