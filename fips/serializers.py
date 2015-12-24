from rest_framework import serializers


class FipsSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=1024)
    type = serializers.CharField(max_length=2)
    fips_id = serializers.IntegerField()
