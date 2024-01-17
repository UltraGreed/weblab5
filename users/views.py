from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import PokerUser
from .serializers import PokerUserSerializer


# @api_view(['GET'])
# def get_user_list(request):
#     users = PokerUser.objects.all()
#     serializer = PokerUserSerializer(users, many=True)
#     return Response(serializer.data, status=status.HTTP_200_OK)
