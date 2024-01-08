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


class RoomInviteView(generics.UpdateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        room = self.get_object()
        user_to_invite = CustomUser.objects.get(username=request.data.get('username'))
        room.invitations.add(user_to_invite)
        return Response(RoomSerializer(room).data, status=status.HTTP_200_OK)


class RoomAcceptInviteView(generics.UpdateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        room = self.get_object()
        room.players.add(request.user)
        room.invitations.remove(request.user)
        return Response(RoomSerializer(room).data, status=status.HTTP_200_OK)


class GameDetailView(APIView):
    def get(self, request):
        game_name = request.GET.get('game', '')
        if game_name == '':
            return Response('didnt get parameter "game"', status=status.HTTP_400_BAD_REQUEST)
        game = Game.objects.filter(name=game_name).first()
        if game is None:
            return Response('game not found', status=status.HTTP_400_BAD_REQUEST)
        return Response(GameSerializer(game).data, status=status.HTTP_200_OK)

    def post(self, request):
        if 'players' not in request.data['body'] or 'chips' not in request.data['body']:
            res = {'status': 400, 'msg': 'didnt receive data'}
            return Response(res, status=status.HTTP_400_BAD_REQUEST)
        path, name = make_path('/game/', Game)
        players = int(request.data['body']['players'])
        chips = int(request.data['body']['chips'])
        big_blind = math.ceil(chips / 100)
        small_blind = math.ceil(big_blind / 2)
        Game.objects.create(path=path, big_blind=big_blind, small_blind=small_blind,
                            name=name, max_players=players, starting_chips=chips)
        res = {'status': 200, 'msg': 'success', 'path': path}
        return Response(res, status=status.HTTP_200_OK)


class PlayerDetailView(APIView):
    def get(self, request):
        if 'user_id' not in request.session:
            return Response('user not logged in', status=status.HTTP_401_UNAUTHORIZED)

        game_name = request.GET.get('game', '')
        if game_name == '':
            return Response('game parameter not found', status=status.HTTP_400_BAD_REQUEST)

        game = Game.objects.filter(name=game_name).first()
        if game is None:
            return Response('game from parameter not found', status=status.HTTP_400_BAD_REQUEST)

        player = Player.objects.filter(user=request.session['user_id'], game=game).first()
        if player is None:
            return Response('player not found', status=status.HTTP_400_BAD_REQUEST)
        player_serialized = PlayerSerializer(player).data
        request.session[f'{game_name}_player_id'] = player_serialized['id']
        return Response(player_serialized, status=status.HTTP_200_OK)


class PlayersDetailsView(APIView):
    def get(self, request):
        game_name = request.GET.get('game', '')
        if game_name == '':
            return Response('game parameter not found', status=status.HTTP_400_BAD_REQUEST)

        game = Game.objects.filter(name=game_name).first()
        if game is None:
            return Response('game from parameter not found', status=status.HTTP_400_BAD_REQUEST)
        players = Player.objects.filter(game=game, is_in_game=True)
        if players is None:
            return Response('players not found', status=status.HTTP_400_BAD_REQUEST)
        players_serialized = PlayerSerializer(players, many=True).data
        return Response(players_serialized, status=status.HTTP_200_OK)


class PlayerRaiseView(APIView):
    def post(self, request):
        game_name = request.data['body']['game']
        if game_name == '':
            return Response('didnt get game_name', status=status.HTTP_400_BAD_REQUEST)
        player_id = request.session[f'{game_name}_player_id']
        if player_id is None:
            return Response('didnt get player_id', status=status.HTTP_400_BAD_REQUEST)
        chips = int(request.data['body']['value'])
        if chips == 0 or chips is None:
            return Response('chips was None or 0', status=status.HTTP_400_BAD_REQUEST)
        player = Player.objects.filter(id=player_id).first()
        if player is None:
            return Response('player not found', status=status.HTTP_400_BAD_REQUEST)
        player_helper.raize(player, chips)
        game_helper.check_next_round(game_name)
        return Response('raised successfully', status=status.HTTP_200_OK)


class PlayerCallView(APIView):
    def post(self, request):
        game_name = request.data['body']['game']
        if game_name == '':
            return Response('didnt get game_name', status=status.HTTP_400_BAD_REQUEST)
        player_id = request.session[f'{game_name}_player_id']
        if player_id is None:
            return Response('didnt get player_id', status=status.HTTP_400_BAD_REQUEST)
        chips = int(request.data['body']['value'])
        if chips == 0 or chips is None:
            return Response('chips was None or 0', status=status.HTTP_400_BAD_REQUEST)

        player = Player.objects.filter(id=player_id).first()
        if player is None:
            return Response('player not found', status=status.HTTP_400_BAD_REQUEST)
        player_helper.call(player, chips)
        game_helper.check_next_round(game_name)

        return Response('raised successfully', status=status.HTTP_200_OK)


class PlayerCheckView(APIView):
    def post(self, request):
        game_name = request.data['body']['game']
        if game_name == '':
            return Response('didnt get game_name', status=status.HTTP_400_BAD_REQUEST)
        player_id = request.session[f'{game_name}_player_id']
        if player_id is None:
            return Response('didnt get player_id', status=status.HTTP_400_BAD_REQUEST)
        chips = int(request.data['body']['value'])
        if chips == 0 or chips is None:
            return Response('chips was None or 0', status=status.HTTP_400_BAD_REQUEST)

        player = Player.objects.filter(id=player_id).first()
        if player is None:
            return Response('player not found', status=status.HTTP_400_BAD_REQUEST)
        player_helper.check()
        game_helper.check_next_round(game_name)

        return Response('raised successfully', status=status.HTTP_200_OK)


class PlayerAllInView(APIView):
    def post(self, request):
        game_name = request.data['body']['game']
        if game_name == '':
            return Response('didnt get game_name', status=status.HTTP_400_BAD_REQUEST)
        player_id = request.session[f'{game_name}_player_id']
        if player_id is None:
            return Response('didnt get player_id', status=status.HTTP_400_BAD_REQUEST)
        chips = int(request.data['body']['value'])
        if chips == 0 or chips is None:
            return Response('chips was None or 0', status=status.HTTP_400_BAD_REQUEST)

        player = Player.objects.filter(id=player_id).first()
        if player is None:
            return Response('player not found', status=status.HTTP_400_BAD_REQUEST)
        player_helper.all_in(player, chips)
        game_helper.check_next_round(game_name)

        return Response('raised successfully', status=status.HTTP_200_OK)


class PlayerFoldView(APIView):
    def post(self, request):
        game_name = request.data['body']['game']
        if game_name == '':
            return Response('didnt get game_name', status=status.HTTP_400_BAD_REQUEST)
        player_id = request.session[f'{game_name}_player_id']
        if player_id is None:
            return Response('didnt get player_id', status=status.HTTP_400_BAD_REQUEST)
        game = Game.objects.filter(name=game_name).first()
        if game is None:
            return Response('game not found', status=status.HTTP_400_BAD_REQUEST)
        player = Player.objects.filter(id=player_id).first()
        if player is None:
            return Response('player not found', status=status.HTTP_400_BAD_REQUEST)
        player_helper.fold(player)
        game_helper.check_next_round(game_name)

        return Response('call action success', status=status.HTTP_200_OK)


class PlayerActionsView(APIView):
    def get(self, request):
        game_name = request.GET.get('game', '')
        if game_name == '':
            return Response('didnt get game_name', status=status.HTTP_400_BAD_REQUEST)
        player_id = request.session[f'{game_name}_player_id']
        if player_id is None:
            return Response('didnt get player_id', status=status.HTTP_400_BAD_REQUEST)
        game = Game.objects.filter(name=game_name).first()
        if game is None:
            return Response('game not found', status=status.HTTP_400_BAD_REQUEST)
        player = Player.objects.filter(id=player_id).first()
        if player is None:
            return Response('player not found', status=status.HTTP_400_BAD_REQUEST)
        player = player_helper.set_allowed_actions(game, player)
        player.save()
        return Response(PlayerSerializer(player).data, status=status.HTTP_200_OK)


class CardsDetailView(APIView):
    def get(self, request):
        game_name = request.GET.get('game', '')
        if game_name == '':
            return Response('game from parameter not found', status=status.HTTP_400_BAD_REQUEST)

        if f'{game_name}_player_id' not in request.session:
            return Response('cant get cards, didnt find player_id in session', status.HTTP_401_UNAUTHORIZED)
        cards = Card.objects.filter(player=request.session[f'{game_name}_player_id'])

        if not cards:
            return Response('didnt find any cards for player', status.HTTP_400_BAD_REQUEST)
        return Response(CardSerializer(cards, many=True).data, status=status.HTTP_200_OK)


class TableCardsDetailView(APIView):
    def get(self, request):
        game_name = request.GET.get('game', '')
        if game_name == '':
            return Response('game from parameter not found', status=status.HTTP_400_BAD_REQUEST)

        game = Game.objects.filter(name=game_name).first()
        if game is None:
            return Response('game not found', status=status.HTTP_400_BAD_REQUEST)

        cards = Card.objects.filter(game=game, location='TABLE')

        if not cards:
            return Response('didnt find any cards in game', status.HTTP_204_NO_CONTENT)
        return Response(CardSerializer(cards, many=True).data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_user_list(request):
    users = CustomUser.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
