from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.serializers.serializer_user import UserSerializer


@api_view(['POST'])
def create_user(request):
    if request.method == "POST":
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': True, 'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'success': False, 'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)