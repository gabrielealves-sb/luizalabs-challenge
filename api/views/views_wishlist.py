from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.models import Wishlist
from api.serializers.serializer_wishlist import WishlistResponseSerializer, WishListRequestSerializer


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated, ])
def wishlist_list(request):
    """ List all wishlists, or create a new wishlist. """
    if request.method == "GET":
        if "client" in request.GET:
            wishlists = Wishlist.objects.filter(client=request.GET.get('client'))
            serializer = WishlistResponseSerializer(wishlists, many=True)
            return Response({'success': True, 'data': serializer.data})
        else:
            wishlists = Wishlist.objects.all()
            paginator = PageNumberPagination()
            result_page = paginator.paginate_queryset(wishlists, request)
            serializer = WishlistResponseSerializer(result_page, many=True)
            return paginator.get_paginated_response({'success': True, 'data': serializer.data})

    if request.method == "POST":
        serializer = WishListRequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            wishlist = Wishlist.objects.get(client=serializer.data['client'])
            serializer = WishlistResponseSerializer(wishlist)
            return Response({'success': True, 'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'success': False, 'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated, ])
def wishlist_detail(request, pk):
    """ Retrieve, update or delete a wishlist instance. """
    try:
        wishlist = Wishlist.objects.get(pk=pk)
    except Wishlist.DoesNotExist:
        return Response({'success': False, 'error': 'Wishlist does not exist'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        response_serializer = WishlistResponseSerializer(wishlist)
        return Response({'success': True, 'data': response_serializer.data})

    if request.method == "PUT":
        """ Add new products on wishlist """
        serializer = WishListRequestSerializer(wishlist, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.update(wishlist, serializer.validated_data)
            serializer = WishlistResponseSerializer(wishlist)
            return Response({'success': True, 'data': serializer.data})
        return Response({'success': False, 'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    if request.method == "DELETE":
        if request.data:
            """ Delete only products from Wishlist"""
            serializer = WishListRequestSerializer(wishlist, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.delete(wishlist, serializer.validated_data)
                serializer = WishlistResponseSerializer(wishlist)
                return Response({'success': True, 'data': serializer.data})
            return Response({'success': False, 'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            """ Delete all wishlist """
            wishlist.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
