from rest_framework import serializers
from api.core.serializer import BaseSerializer
from api.core.serializer_fields import YesNoToBooleanField

class UserV2Serializer(BaseSerializer):
    id = serializers.IntegerField(read_only=True)
    login = serializers.EmailField(max_length=100)
    password_sha256 = serializers.CharField(max_length=64, write_only=True)  # SHA256 length
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    is_active = serializers.BooleanField(read_only=True, default=True)
    str_bool = YesNoToBooleanField(required=False, allow_null=True)

    class Meta:
        # fields = ['id', 'login', 'password', 'first_name', 'last_name', 
        #          'is_active', 'str_bool', 'created_at', 'created_from', 
        #          'updated_at', 'updated_from'] 
        fields = '__all__' 