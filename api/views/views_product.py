from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.models import Product
from api.serializers.serializer_product import ProductSerializer


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated,])
def product_list(request):
    """ List all products, or create a new product. """
    if request.method == "GET":
        paginator = PageNumberPagination()
        products = Product.objects.all()
        result_page = paginator.paginate_queryset(products, request)
        serializer = ProductSerializer(result_page, many=True)
        return paginator.get_paginated_response({'success': True, 'data': serializer.data})

    if request.method == "POST":
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': True, 'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'success': False, 'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated,])
def product_detail(request, pk):
    """ Retrieve, update or delete a product instance. """
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response({'success': False, 'error': 'Product does not exist'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = ProductSerializer(product)
        return Response({'success': True, 'data': serializer.data})

    if request.method == "PUT":
        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': True, 'data': serializer.data})
        return Response({'success': False, 'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    if request.method == "DELETE":
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
