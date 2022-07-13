from rest_framework import serializers

from api.models import Product


class ProductSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    review_score = serializers.IntegerField(read_only=True)

    class Meta:
        model = Product
        fields = ('id', 'title', 'price', 'image', 'brand', 'review_score')

    @staticmethod
    def validate_price(value):
        if value < 0:
            raise serializers.ValidationError('The price cannot be negative')
        return value