from rest_framework import serializers


class UsersLabelSerializer(serializers.Serializer):

    user_ids = serializers.ListField(
        child=serializers.CharField(
            required=True,
            allow_blank=False,
            allow_null=False,
            min_length=1,
        ),
        allow_empty=False,
        allow_null=False,
        required=True,
    )
    label = serializers.CharField(
        required=True,
        allow_blank=False,
        allow_null=False,
        min_length=1,
    )
