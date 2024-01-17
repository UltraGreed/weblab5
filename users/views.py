from rest_framework import generics
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from .models import PokerUser
from .serializers import PokerUserSerializer


class GetMe(generics.RetrieveAPIView):
    queryset = PokerUser.objects.all()
    serializer_class = PokerUserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class UserList(generics.ListAPIView):
    queryset = PokerUser.objects.all()
    serializer_class = PokerUserSerializer
    permission_classes = [IsAdminUser]
