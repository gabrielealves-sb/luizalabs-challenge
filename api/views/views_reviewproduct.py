from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.models import ReviewProduct
from api.serializers.serializer_reviewproduct import ReviewProductSerializer


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated,])
def review_list(request):
    """ List all reviews, or create a new review. """
    if request.method == "GET":
        if "product" in request.GET:
            reviews = ReviewProduct.objects.filter(product=request.GET.get('product'))
        else:
            reviews = ReviewProduct.objects.all()
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(reviews, request)
        serializer = ReviewProductSerializer(result_page, many=True)
        return paginator.get_paginated_response({'success': True, 'data': serializer.data})

    if request.method == "POST":
        serializer = ReviewProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': True, 'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'success': False, 'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated,])
def review_detail(request, pk):
    """ Retrieve, update or delete a review instance. """
    try:
        review = ReviewProduct.objects.get(pk=pk)
    except ReviewProduct.DoesNotExist:
        return Response({'success': False, 'error': 'Review does not exist'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = ReviewProductSerializer(review)
        return Response({'success': True, 'data': serializer.data})

    if request.method == "PUT":
        serializer = ReviewProductSerializer(review, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': True, 'data': serializer.data})
        return Response({'success': False, 'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    if request.method == "DELETE":
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
