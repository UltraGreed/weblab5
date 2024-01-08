from django.urls import path
from .views import *

urlpatterns = [
    path('rooms/<int:pk>/', RoomDetail.as_view(), name='room-detail'),
    path('rooms/create/', RoomCreateView.as_view(), name='room-create'),
    path('rooms/join/<int:pk>/', RoomJoinView.as_view(), name='room-join'),
    path('rooms/leave/<int:pk>/', RoomLeaveView.as_view(), name='room-leave'),
    path('rooms/invite/<int:pk>/', RoomInviteView.as_view(), name='room-invite'),
    path('rooms/accept_invite/<int:pk>/', RoomAcceptInviteView.as_view(), name='room-accept-invite'),
    path('users/', get_user_list, name='user-list'),
    path('get/game-detail/', GameDetailView.as_view(), name='game-detail'),
    path('get/player-detail/', PlayerDetailView.as_view(), name='player-detail'),
    path('get/players-details/', PlayersDetailsView.as_view(), name='players-details'),
    path('get/cards-detail/', CardsDetailView.as_view(), name='cards-detail'),
    path('get/table-cards-detail/', TableCardsDetailView.as_view(), name='table-cards-detail'),
    path('get/player-actions/', PlayerActionsView.as_view(), name='player-actions'),
    path('post/game/', GameDetailView.as_view(), name='game-create'),
    path('post/player/raise/', PlayerRaiseView.as_view(), name='player-raise'),
]
