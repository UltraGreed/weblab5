from django.urls import path
from .views import RoomCreateView, RoomDetail, RoomJoinView, RoomLeaveView, get_user_list


urlpatterns = [
    path('rooms/<int:pk>/', RoomDetail.as_view(), name='room-detail'),
    path('rooms/create/', RoomCreateView.as_view(), name='room-create'),
    path('rooms/join/<int:pk>/', RoomJoinView.as_view(), name='room-join'),
    path('rooms/leave/<int:pk>/', RoomLeaveView.as_view(), name='room-leave'),
    path('users/', get_user_list, name='user-list'),
]
