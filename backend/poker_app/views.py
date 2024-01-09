import math
from rest_framework.decorators import api_view
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from . import player_helper, game_helper
from .serializers import *
from .models import CustomUser
from .utils import make_path


class RoomCreateView(generics.CreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        max_players = self.request.data.get('max_players', 2)
        room = serializer.save(max_players=max_players)
        room.save()
        room.players.add(self.request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class RoomJoinView(generics.UpdateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        room = self.get_object()
        if room.players.count() >= room.max_players:
            return Response({'detail': 'Room is already full.'}, status=status.HTTP_400_BAD_REQUEST)
        if request.user in room.players.all():
            return Response({'detail': 'You are already in the room.'}, status=status.HTTP_400_BAD_REQUEST)
        room.players.add(request.user)
        return Response(RoomSerializer(room).data, status=status.HTTP_200_OK)


class RoomLeaveView(generics.UpdateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        room = self.get_object()
        room.players.remove(request.user)
        return Response(RoomSerializer(room).data, status=status.HTTP_200_OK)


class RoomDetail(generics.RetrieveDestroyAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
