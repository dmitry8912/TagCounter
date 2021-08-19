import uuid
from rest_framework import serializers
from counterservice.models import URLs


class URLsSerializer(serializers.Serializer):
    id = serializers.UUIDField(required=False)
    url = serializers.CharField(required=True)
    result = serializers.JSONField(allow_null=True, required=False)

    def create(self, validated_data):
        return URLs.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.result = validated_data.get('result', instance.result)
        instance.save()
        return instance
