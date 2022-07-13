from rest_framework import serializers

from api.models import ReviewProduct


class ReviewProductSerializer(serializers.ModelSerializer):
    def validate_author(self, value):
        product = self.initial_data['product']
        if ReviewProduct.objects.filter(author=value, product=product).exists():
            raise serializers.ValidationError('You already reviewed this product')
        return value

    class Meta:
        model = ReviewProduct
        fields = ('id', 'author', 'product', 'text', 'rate')
        read_only_fields = ('id',)