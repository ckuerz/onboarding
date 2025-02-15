from rest_framework import serializers

class UserBaseSerializer(serializers.Serializer):
    """Base serializer with common fields"""
    id = serializers.IntegerField(read_only=True)
    login = serializers.EmailField(max_length=100, required=False)
    first_name = serializers.CharField(max_length=100, required=False)
    last_name = serializers.CharField(max_length=100, required=False)
    created_at = serializers.DateTimeField(read_only=True)
    is_active = serializers.BooleanField(read_only=True, default=True)
    test_bool = serializers.CharField(required=False, allow_null=True)

    def validate_test_bool(self, value):
        if value is None:
            return None
        if value.lower() == 'ja':
            return True
        if value.lower() == 'nein':
            return False
        raise serializers.ValidationError("test_bool must be 'ja' or 'nein'")

class UserCreateSerializer(UserBaseSerializer):
    """Serializer for user creation - all fields required except defaults"""
    login = serializers.EmailField(max_length=100, required=True)
    password = serializers.CharField(max_length=64, write_only=True, required=True)  # SHA256 length
    first_name = serializers.CharField(max_length=100, required=True)
    last_name = serializers.CharField(max_length=100, required=True)

class UserUpdateSerializer(UserBaseSerializer):
    """Serializer for user updates - all fields optional"""
    password = serializers.CharField(max_length=64, write_only=True, required=False)
    first_name = serializers.CharField(max_length=100, required=False)
    last_name = serializers.CharField(max_length=100, required=False)
    login = None  # Login cannot be updated

class UserReadSerializer(UserBaseSerializer):
    """Serializer for reading user data - no password"""
    pass

    def to_representation(self, instance):
        """Convert boolean back to ja/nein for test_bool field"""
        data = super().to_representation(instance)
        if 'test_bool' in data and data['test_bool'] is not None:
            data['test_bool'] = 'ja' if data['test_bool'] else 'nein'
        return data