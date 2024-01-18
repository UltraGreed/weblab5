from django.urls import path
from .views import RoomCreate, RoomList


urlpatterns = [
    # path('<int:pk>/', RoomDetail.as_view(), name='room-detail'),
    path('create/', RoomCreate.as_view(), name='room-create'),
    path('', RoomList.as_view(), name='room-list')
    # path('join/<int:pk>/', RoomJoin.as_view(), name='room-join'),
    # path('leave/<int:pk>/', RoomLeave.as_view(), name='room-leave'),
]
