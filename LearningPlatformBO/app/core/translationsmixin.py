from typing import Any, Optional, TypedDict, cast
from modeltranslation.translator import translator
from rest_framework import serializers
from rest_framework.fields import Field
from rest_framework.fields import Field as Field
from rest_framework.request import Request
from rest_framework.utils.model_meta import FieldInfo
from django.conf import settings

class TranslationsSerializerMixin(serializers.ModelSerializer):
    """
    Custom mixin to return the correct field in the case the field is translateable and the user requests for a
    different language. This is achieved by replacing the source of the field in translateable fields with the
    correctly translated one.
    """

    def build_field(
        self, field_name: str, info: FieldInfo, model_class: Any, nested_depth: int
    ) -> tuple[type[Field], dict[str, Any]]:
        """
        Override this method so that we can replace translateable fields with the appropriate translations if the
        request asks for a different language.
        """
        field, kwargs = super().build_field(field_name, info, model_class, nested_depth)
        translatable_fields = translator.get_options_for_model(self.Meta.model).get_field_names()

        if field_name not in translatable_fields:
            return field, kwargs
        
        request = self.context.get("request")
        if not request:
            return field, kwargs

        language = request.headers.get("Accept-Language", 'en').split(',')[0].strip()
        if language not in [code for code, _ in settings.LANGUAGES]:
            language = 'en'

        translated_field_name = f"{field_name}_{language}"
        default_field_name = f"{field_name}_en"
        if hasattr(model_class, translated_field_name):
            kwargs['source'] = translated_field_name
        elif hasattr(model_class, default_field_name):
            kwargs['source'] = default_field_name
        else:
            kwargs['source'] = field_name

        return field, kwargs   


    def to_representation(self, instance):
        """
        Overrides the default to_representation to handle translations dynamically.
        """
        ret = super().to_representation(instance)
        request = self.context.get('request')
        language = request.headers.get('Accept-Language', 'en') if request else 'en'
        language = language.split(',')[0].strip()

        for field_name in ret:
            translated_field_name = f"{field_name}_{language}"
            default_field_name = f"{field_name}_en"

            translated_value = getattr(instance, translated_field_name, None)
            if not translated_value:
                english_value = getattr(instance, default_field_name, None)
                ret[field_name] = english_value if english_value else getattr(instance, field_name)

        return ret