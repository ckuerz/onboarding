from rest_framework import serializers

class BaseSerializer(serializers.Serializer):
    # Common field that all serializers will inherit
    created_at = serializers.DateTimeField(read_only=True)
    created_from = serializers.CharField(max_length=255, write_only=True)
    changed_at = serializers.DateTimeField(read_only=True)
    changed_from = serializers.CharField(max_length=255, required=False, write_only=True)

    def validate(self, data):
        request = self.context.get('request') 
        print("request: ", request)
        if request and request.method in ['PUT', 'PATCH']:
            if not data.get('changed_from'):
                raise serializers.ValidationError({'changed_from': 'This field is required for PATCH/PUT.'})
        elif request and request.method == 'POST':
            # For POST requests, changed_from should not be present
            if 'changed_from' in data:
                raise serializers.ValidationError({'changed_from': 'This field should not be included for POST requests.'})
        return data