import html
import logging
from typing import Any, Literal, Optional, Sequence
from googletrans import Translator
from django.core.exceptions import FieldDoesNotExist
from django.db import models
from core.utilities import empty


logger = logging.getLogger(__name__)

t = Translator()


def translate(text: str, language: Literal["en"] | Literal["es"]) -> str:  # pragma: no cover # always mocked in tests
    """
    Shortcut function to translate portuguese to english / spanish.

    If the translation fails, returns an empty string.
    """
    try:
        translated = t.translate(text, dest=language)
        return translated.text
    except Exception as e:
        # The translator sometimes simply fails. Log the error in case we want to look into it in the future.
        logger.warn(e)
        return ""


class AutoTranslateableModelMixin(models.Model):
    """
    Custom model mixin to enable automatic translation of model fields on save, from portuguese to EN / PT. Should
    only be applied to models registered for translation, and with fields that are registered for translations.

    This translation is only placed if the "foreign language" field is empty, and the portuguese one isn't.

    The fields to be translated can be set by the property `auto_translate_fields` (Sequence[str]).

    If `only_first_save` is set (default=True), the automatic translation will only happen on the first save.
    """

    auto_translate_fields: Sequence[str] = tuple()
    only_first_save: bool = True

    class Meta:
        abstract = True

    def save(self, *args: Any, **kwargs: Any) -> None:
        """Override the save method to translate fields if appropriate."""
        if not self._state.adding and self.only_first_save:
            # Not first save
            return super().save(*args, **kwargs)
        for field_name in self.auto_translate_fields:
            field_path_str = f"{self._meta.app_label}.{self._meta.object_name}.{field_name}"
            try:
                field = self._meta.get_field(field_name)
                field_pt = self._meta.get_field(f"{field_name}_pt")
                field_en = self._meta.get_field(f"{field_name}_en")
                field_es = self._meta.get_field(f"{field_name}_es")
            except FieldDoesNotExist:
                logger.warn(f"'{field_path_str}' does not exist. Translation skipped.")
                continue
            if not isinstance(field, models.Field) or field.get_internal_type() not in ["CharField", "TextField"]:
                logger.warn(f"Field '{field_path_str}' is not a Charfield or TextField. Translation skipped.")
                continue
            text_pt: Optional[str] = getattr(self, field_pt.name, None)
            if empty(text_pt):
                # Nothing to translate
                continue

            assert isinstance(text_pt, str)  # TypeGuard
            # TODO: currently we're unescaping the HTML and then translating, and not escaping back. We might need to
            # take a look back at this.
            escaped_text_pt: str = html.unescape(text_pt)

            # Translate to EN
            if empty(getattr(self, field_en.name, None)):
                translation_en = translate(escaped_text_pt, "en")
                if empty(translation_en):
                    logger.warn(f"Failed to translate '{escaped_text_pt}' to EN for '{field_path_str}'.")
                else:
                    setattr(self, field_en.name, translation_en)
            # Translate to ES
            if empty(getattr(self, field_es.name, None)):
                translation_es = translate(escaped_text_pt, "es")
                if empty(translation_es):
                    logger.warn(f"Failed to translate '{escaped_text_pt}' to ES for '{field_path_str}'.")
                else:
                    setattr(self, field_es.name, translation_es)
        return super().save(*args, **kwargs)
