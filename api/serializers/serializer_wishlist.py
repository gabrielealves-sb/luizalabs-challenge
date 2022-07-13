from rest_framework import serializers
from api.models import Wishlist, Product, Client
from api.serializers.serializer_client import ClientSerializer
from api.serializers.serializer_product import ProductSerializer


class WishlistResponseSerializer(serializers.ModelSerializer):
    """ Show nested data in responses """
    id = serializers.IntegerField(read_only=True)
    client = ClientSerializer(read_only=True)
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = Wishlist
        fields = ('id', 'client', 'products')


class WishListRequestSerializer(serializers.ModelSerializer):
    """ Receive data by id in requests """
    id = serializers.IntegerField(read_only=True)
    client = serializers.PrimaryKeyRelatedField(queryset=Client.objects.all())
    products = serializers.PrimaryKeyRelatedField(many=True, queryset=Product.objects.all())
    remove_products = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Product.objects.all(),
        write_only=True,
        required=False
    )

    def validate_client(self, value):
        """ Check if the client wishlist exists """
        if not self.instance:
            if Wishlist.objects.filter(client=value).exists():
                raise serializers.ValidationError('This client already have a wishlist')
        return value

    def validate_products(self, value):
        """ Check if the products exists on wishlist """
        if self.instance:
            pk = self.instance.pk
            wishlist = Wishlist.objects.filter(pk=pk, products__in=value)
            if wishlist.exists():
                products_qs = Product.objects.filter(wishlist__pk=pk, pk__in=[value.id for value in value])
                products = [product.id for product in products_qs]
                raise serializers.ValidationError(f'This products {products} already exist on wishlist')
        return value

    def validate_remove_products(self, value):
        """ Check if the products can be removed"""
        if self.instance:
            pk = self.instance.pk
            wishlist = Wishlist.objects.filter(pk=pk, products__in=value)
            if not wishlist.exists():
                products = [product.id for product in value]
                raise serializers.ValidationError(f'This products {products} does not exist on wishlist')
        return value

    def update(self, instance, validated_data):
        """ Add new products on wishlist """
        product_data = validated_data.pop('products')
        for product in product_data:
            instance.products.add(product)
        return instance

    def delete(self, instance, validated_data):
        """ Delete products on wishlist """
        remove_products_data = validated_data.pop('remove_products')
        for product in remove_products_data:
            instance.products.remove(product)
        return instance

    class Meta:
        model = Wishlist
        fields = ('id', 'client', 'products', 'remove_products')
