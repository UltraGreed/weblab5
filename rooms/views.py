from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from rest_framework import generics

from rest_framework.permissions import IsAuthenticated
from .models import Room
from .serializers import RoomSerializer


class RoomCreate(generics.CreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()
        # noinspection PyArgumentList
        async_to_sync(get_channel_layer().send)(
            'poker-game-manager',
            {
                'type': 'create.game',
                'room_id': str(serializer.data['id'])
            }
        )



class RoomDetail(generics.RetrieveAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated]


class RoomList(generics.ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
