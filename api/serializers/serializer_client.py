from rest_framework import serializers

from api.models import Client


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ('id', 'name', 'email')
        read_only_fields = ('id',)



