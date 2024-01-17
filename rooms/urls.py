from django.urls import path
from .views import RoomCreate, RoomDetail, RoomJoin, RoomLeave


urlpatterns = [
    path('<int:pk>/', RoomDetail.as_view(), name='room-detail'),
    path('create/', RoomCreate.as_view(), name='room-create'),
    path('join/<int:pk>/', RoomJoin.as_view(), name='room-join'),
    path('leave/<int:pk>/', RoomLeave.as_view(), name='room-leave'),
]
