from rest_framework import serializers
from django.utils import timezone
from drf_yasg import openapi


class YesNoToBooleanField(serializers.Field):
    """
    Serializer field that converts between:
    - API: boolean (true/false)
    - Database: string ('yes'/'no')
    """

    swagger_schema_fields = {
        'type': openapi.TYPE_BOOLEAN,  # Indicates the field is a boolean in Swagger
    }

    def to_representation(self, value):
        """Database ('yes'/'no') -> API (true/false)"""
        if value is None:
            return None
        return value.lower() == 'yes'

    def to_internal_value(self, data):
        print("to_internal_value data:", data, type(data))
        """API (true/false) -> Database ('yes'/'no')"""
        if data is None:
            return None
            
        if isinstance(data, bool):
            return 'yes' if data else 'no'
            
        if isinstance(data, str):
            value = data.lower()
            if value in ('yes', 'true', '1'):
                return 'yes'
            if value in ('no', 'false', '0'):
                return 'no'
            
        raise serializers.ValidationError('Invalid value. Must be a boolean or yes/no string.')

    def get_schema_fields(self, *args, **kwargs):
        return {
            'type': 'boolean',
            'nullable': self.allow_null
        }