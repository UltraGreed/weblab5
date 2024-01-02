from django.urls import path
from .views import RoomCreateView, RoomDetail, RoomJoinView

urlpatterns = [
    path('rooms/<int:pk>/', RoomDetail.as_view(), name='room-detail'),
    path('rooms/create/', RoomCreateView.as_view(), name='room-create'),
    path('rooms/join/<int:pk>/', RoomJoinView.as_view(), name='room-join'),
]
