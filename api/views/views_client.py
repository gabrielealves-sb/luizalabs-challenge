from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.models import Client
from api.serializers.serializer_client import ClientSerializer


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated,])
def client_list(request):
    """ List all clients, or create a new client. """
    if request.method == "GET":
        paginator = PageNumberPagination()
        clients = Client.objects.all()
        result_page = paginator.paginate_queryset(clients, request)
        serializer = ClientSerializer(result_page, many=True)
        return paginator.get_paginated_response({'success': True, 'data': serializer.data})

    if request.method == "POST":
        serializer = ClientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': True, 'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'success': False, 'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated,])
def client_detail(request, pk):
    """ Retrieve, update or delete a client instance. """
    try:
        client = Client.objects.get(pk=pk)
    except Client.DoesNotExist:
        return Response({'success': False, 'error': 'Client does not exist'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = ClientSerializer(client)
        return Response({'success': True, 'data': serializer.data})

    if request.method == "PUT":
        serializer = ClientSerializer(client, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': True, 'data': serializer.data})
        return Response({'success': False, 'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    if request.method == "DELETE":
        client.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
