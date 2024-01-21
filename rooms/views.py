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


# class RoomJoin(generics.UpdateAPIView):
#     queryset = Room.objects.all()
#     serializer_class = RoomSerializer
#     permission_classes = [IsAuthenticated]
#
#     def update(self, request, *args, **kwargs):
#         room = self.get_object()
#         room.players.add(request.user)
#         return Response(RoomSerializer(room).data, status=status.HTTP_200_OK)
#
#
# class RoomLeave(generics.UpdateAPIView):
#     queryset = Room.objects.all()
#     serializer_class = RoomSerializer
#     permission_classes = [IsAuthenticated]
#
#     def update(self, request, *args, **kwargs):
#         room = self.get_object()
#         room.players.remove(request.user)
#         return Response(RoomSerializer(room).data, status=status.HTTP_200_OK)
#
#
# class RoomDetail(generics.RetrieveDestroyAPIView):
#     queryset = Room.objects.all()
#     serializer_class = RoomSerializer
#     permission_classes = [IsAuthenticated]
#
#     def get(self, request, *args, **kwargs):
#         instance = self.get_object()
#         serializer = self.get_serializer(instance)
#         return Response(serializer.data)
#
#     def delete(self, request, *args, **kwargs):
#         instance = self.get_object()
#         self.perform_destroy(instance)
#         return Response(status=status.HTTP_204_NO_CONTENT)


class RoomList(generics.ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
