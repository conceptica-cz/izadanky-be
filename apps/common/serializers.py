from rest_framework import serializers


class ResultField(serializers.Field):
    def to_representation(self, value):
        return value

    def to_internal_value(self, data):
        return data


class TaskSerializer(serializers.Serializer):
    state = serializers.CharField(max_length=20)
    result = ResultField()
