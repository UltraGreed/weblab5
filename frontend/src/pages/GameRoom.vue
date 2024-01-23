<template>
  <q-page class="column items-center q-pt-xl" style="overflow: hidden;">
    <div class="table-container">
      <div>
        <img
          v-for="(card, index) in playercards"
          :key="index"
          :src="`/cards/${card.name}`"
          class="game-card"
          style="position: absolute; left: 47.5%; top: 9%; opacity: 0"
          alt=""
          draggable="false"
        />
      </div>
      <div>
        <img
          v-for="(card, index) in commoncards"
          :key="index"
          :src="`/cards/${card.name}`"
          class="common-card"
          style="position: absolute; left: 47.5%; top: 9%; opacity: 0"
          alt=""
          draggable="false"
        />
      </div>
      <div v-if="countdown" style="position: absolute; left: 47.5%; top:43%;" class="text-white text-h1">
        <p>{{ countdown }}</p>
      </div>
      <img
        src="/cards/back01.png"
        style="width: 5%; position: absolute; left: 47.5%; top: 9%; z-index: 999; pointer-events: auto;"
        @click="dealCommonCards"
        alt=""
        draggable="false"
      />
      <span style="position:absolute; left: 46%; top: 30%;
                   font-size: x-large; color: white;
                   background-color: rgba(0,0,0,0.6);
                   border-radius: 15px;
                   padding: 0 50px 0 50px">
        {{ pot }}
      </span>
      <q-img src="/public/chips2.png" style="height: 45px; width: 45px; left: 35.5vw; top: 21.3vh"
             draggable="false"></q-img>
      <div v-for="(player,i) in players" :key="i">
        <div class="column items-center"
             style="position: absolute; z-index: 1"
             :style="`top: ${playerPositions[i].top + 15}%; left: ${playerPositions[i].left-13.5}%`"
             v-if="player.dealerStatus"
        >
          <img src="/dealer.png" style="width: 10%">
        </div>
        <div class="column items-center"
             style="position: absolute; z-index: 1"
             :style="`top: ${playerPositions[i].top + 15}%; left: ${playerPositions[i].left+3}%`"
             v-if="player.smallBlindStatus"
        >
          <img src="/sb.png" style="width: 17%">
        </div>
        <div class="column items-center"
             style="position: absolute; z-index: 1"
             :style="`top: ${playerPositions[i].top + 15}%; left: ${playerPositions[i].left+3}%`"
             v-if="player.bigBlindStatus"
        >
          <img src="/bb.png" style="width: 17%">
        </div>
        <q-card class="column items-center"
                style="position: absolute; min-width: 15%; min-height: 24%; background-color: rgba(0,0,0,0.6);
          color: white"
                :style="`top: ${playerPositions[i].top}%; left: ${playerPositions[i].left}%`"
                :class="{ 'border-white': player.isMove }"
        >
          <span style="font-size: x-large; bottom: 23%; position:absolute;">
            {{ player.username }}
          </span>
            <span style="font-size: x-large; bottom: 3%; position:absolute;">
            {{ player.chips }}Å
          </span>
          <q-card class="transparent" v-if="player.isWinner"
                  style="z-index: 1; color: gold; max-width: 100px; font-size: x-large; bottom: -40%; position: absolute;">
            WINNER!
          </q-card>
        </q-card>
        <q-card class="column items-center"
                style="position: absolute; min-width: 15%; min-height: 5%; background-color: rgba(0,0,0,0.6);
          color: white; border-top: 1px solid white;"
                :style="`top: ${playerPositions[i].top + 24}%; left: ${playerPositions[i].left}%`"
        >
          <span style="font-size: x-large; bottom: 3%; position: absolute" v-if="player.lastAction === 'raise' || player.lastAction === 'bet'">
            {{ player.lastAction }} + {{ chipsAction }}Å
          </span>
          <span style="font-size: x-large; bottom: 3%; position: absolute" v-else>
            {{ player.lastAction }}
          </span>
        </q-card>
      </div>
    </div>
    <div class="row justify-center q-pa-md" style="position: absolute; bottom: -1%;">
      <div class="button-container q-pb-lg" v-if="(players.find((player) => player.isMove) || {id: 0}).id === ourId">
        <q-btn v-if="!was_raised"
               style="font-size: 20px; background-color: #960018; color: #ffffff; width: 100px; height: 50px; box-shadow: 3px 3px 5px rgba(0, 0, 0, 0.3);"
               label="CHECK"
               class="q-mr-md"
               @click="processingActions('CHECK')"
        />
        <q-btn v-if="was_raised"
               style="font-size: 20px; background-color: #960018; color: #ffffff; width: 100px; height: 50px; box-shadow: 3px 3px 5px rgba(0, 0, 0, 0.3);"
               label="CALL"
               class="q-mr-md"
               @click="processingActions('CALL')"
        />
        <q-btn
          style="font-size: 20px; background-color: #960018; color: #ffffff; width: 100px; height: 50px; box-shadow: 3px 3px 5px rgba(0, 0, 0, 0.3);"
          label="FOLD"
          class="q-mr-md"
          @click="processingActions('FOLD')"
        />
        <q-btn v-if="was_raised"
               style="font-size: 20px; background-color: #960018; color: #ffffff; width: 100px; height: 50px; box-shadow: 3px 3px 5px rgba(0, 0, 0, 0.3);"
               label="RAISE"
               @click="processingActions('RAISE'); show.isVisible = !show.isVisible; show.balance = players[players.findIndex((player) => player.isMove)].chips;"
        />
        <q-btn v-if="!was_raised"
               style="font-size: 20px; background-color: #960018; color: #ffffff; width: 100px; height: 50px; box-shadow: 3px 3px 5px rgba(0, 0, 0, 0.3);"
               label="BET"
               class="q-mr-md"
               @click="processingActions('BET'); show.isVisible = !show.isVisible; show.balance = players[players.findIndex((player) => player.isMove)].chips;"
        />
      </div>

      <q-dialog v-model="show.isVisible">
        <q-card class="q-pa-md q-gutter-sm q-dark">
          <q-card-section>
            <div class="text-h5 text-center">Select the number of chips</div>
          </q-card-section>
          <q-card-section>
            <q-btn-toggle
              v-model="chipValue"
              push
              style="background-color: #960018;"
              toggle-color="grey-9"
              :options="[
                  {label: 'min', value: currentAmount + bigBlindValue },
                  {label: '1/4', value: Math.floor(show.balance/4)},
                  {label: '1/2', value: Math.floor(show.balance/2)},
                  {label: '3/4', value: Math.floor(show.balance*(3/4))},
                  {label: 'All In', value: show.balance},
                ]"
            />
          </q-card-section>
          <q-card-section>
            <q-input v-model="chipValue"
                     label-color="white"
                     :input-style="{color: 'white', 'padding-left': '10px'}"
                     color="red-14"
                     style="font-size: 20px"
                     maxlength="14"
                     :rules="[val => (val <= show.balance) || 'The entered value is greater than your balance']"
            />
          </q-card-section>
          <q-card-section class="text-h4 text-center" style="border: 1px solid white; padding: 10px; "
                          max="10000000000000">
            {{ chipValue }}Å
          </q-card-section>
          <q-card-actions align="center">
            <q-btn flat label="Submit" style="background-color: #960018;" @click="checkBalance"
                   :disable="!checkBalance()" v-close-popup/>
            <q-btn flat label="Close" style="background-color: #960018;" v-close-popup/>
          </q-card-actions>
        </q-card>
      </q-dialog>
    </div>
    <q-btn @click="dealPlayerCard" label="1231231"></q-btn>
  </q-page>
</template>

<script setup lang="ts">
import {ref, watch} from 'vue';
import gsap from 'gsap';
import {LocalStorage} from 'quasar';
import {authGet} from "src/utils";

let username = LocalStorage.getItem('username');
if (username === null)
  username = '';

// Arrays of player and table cards
interface Card {
  name: string;
}

const playercards = ref<Card[]>([
  {name: 'clubs_02.png'},
  {name: 'clubs_03.png'},
  {name: 'back.png'},
  {name: 'back.png'},
  {name: 'back.png'},
  {name: 'back.png'},
  {name: 'back.png'},
  {name: 'back.png'},
  {name: 'back.png'},
  {name: 'back.png'},
  {name: 'back.png'},
  {name: 'back.png'},
  {name: 'back.png'},
  {name: 'back.png'},

]);
const commoncards = ref<Card[]>([
  {name: 'diamonds_07.png'},
  {name: 'diamonds_07.png'},
  {name: 'diamonds_07.png'},
  {name: 'diamonds_07.png'},
  {name: 'diamonds_07.png'},
])

// Arrays of positions of the cards for each player and each slot on table
interface playerCardPosition {
  top: number;
  left: number;
}

const playerCardPositions = ref<playerCardPosition[][]>([
  // Player 1 cards
  [
    {top: 76.5, left: 45.3},
    {top: 76.5, left: 50.3},
  ],
  // Player 2 cards
  [
    {top: 76.5, left: 11},
    {top: 76.5, left: 16},
  ],
  // Player 3 cards
  [
    {top: 39, left: 3},
    {top: 39, left: 8},
  ],
  // Player 4 cards
  [
    {top: 0.5, left: 11},
    {top: 0.5, left: 16},
  ],
  // Player 5 cards
  [
    {top: 0.5, left: 80},
    {top: 0.5, left: 85},
  ],
  // Player 6 cards
  [
    {top: 39, left: 88},
    {top: 39, left: 93},
  ],
  // Player 7 cards
  [
    {top: 76.5, left: 80},
    {top: 76.5, left: 85},
  ]
])
const commonCardPositions = ref<playerCardPosition[]>([
  {top: 40, left: 26.5},
  {top: 40, left: 36.5},
  {top: 40, left: 46.5},
  {top: 40, left: 56.5},
  {top: 40, left: 66.5},
])

// Arrays of players and their positions on the table for painting them correctly
interface Player {
  id: number,
  username: string,
  chips: number,
  isMove: boolean
  smallBlindStatus: boolean,
  bigBlindStatus: boolean,
  dealerStatus: boolean,
  isWinner: boolean,
  lastAction: string
}

const players = ref<Player[]>([
  {
    id: 1,
    username: username.toString(),
    chips: 1000,
    isMove: false,
    smallBlindStatus: false,
    bigBlindStatus: false,
    dealerStatus: true,
    isWinner: false,
    lastAction: ''
  },
  {
    id: 2,
    username: 'Vladik',
    chips: 9999,
    isMove: false,
    smallBlindStatus: true,
    bigBlindStatus: false,
    dealerStatus: false,
    isWinner: false,
    lastAction: ''
  },
  {
    id: 3,
    username: 'Semen',
    chips: 100,
    isMove: false,
    smallBlindStatus: false,
    bigBlindStatus: true,
    dealerStatus: false,
    isWinner: false,
    lastAction: ''
  },
])
const playerPositions = ([
  {
    top: 76,
    left: 42.5
  },
  {
    top: 76,
    left: 8
  },
  {
    top: 38.5,
    left: 0
  },
  {
    top: 0,
    left: 8
  },
  {
    top: 0,
    left: 77
  },
  {
    top: 38.5,
    left: 85
  },
  {
    top: 76,
    left: 77
  }
])

let countOfPlayer = 0;
const bigBlindValue = ref(0);
const was_raised = ref(true);
const currentAmount = ref(10);
const url = window.location.href;
const arr = url.split('/')
const chipValue = ref<number>(0);
const chipsAction = ref<number>(0);

authGet(`/rooms/detail/${arr[arr.length - 2]}/`)
  .then(response => {
    countOfPlayer = response.data.n_players;
    bigBlindValue.value = response.data.big_blind_value;
    chipValue.value = currentAmount.value + bigBlindValue.value;
  })
const socket = new WebSocket(`ws://localhost:8000/ws/room/${arr[arr.length - 2]}/?token=${LocalStorage.getItem('accessToken')}`)

// -------------------------------------------------------------------------------------------- //
const show = ref<{ isVisible: boolean, balance: number }>({isVisible: false, balance: 0});

watch(chipValue, (newValue) => {
  if (newValue.toString() === '') {
    chipValue.value = 0;
  } else if (newValue.toString() === '0') {
    chipValue.value = 0;
  } else {
    chipValue.value = parseInt(newValue.toString(), 10);
  }
});

const processingActions = (action: string) => {
  const currentPlayer = players.value.find(player => player.isMove);
  if (!currentPlayer) {
    console.error('Current player not found');
    return;
  }
  const player_id = currentPlayer.id;

  if (action === 'CHECK') {
    socket.send(JSON.stringify({
      type: 'player_action',
      player_id: player_id,
      action: 'check',
      amount: 0
    }));
  } else if (action === 'RAISE') {
    socket.send(JSON.stringify({
      type: 'player_action',
      player_id: player_id,
      action: 'raise',
      amount: chipValue.value
    }));
  } else if (action === 'FOLD') {
    socket.send(JSON.stringify({
      type: 'player_action',
      player_id: player_id,
      action: 'fold',
      amount: 0
    }));
  } else if (action === 'BET') {
    socket.send(JSON.stringify({
      type: 'player_action',
      player_id: player_id,
      action: 'bet',
      amount: chipValue.value
    }));
  } else if (action === 'CALL') {
    socket.send(JSON.stringify({
      type: 'player_action',
      player_id: player_id,
      action: 'call',
      amount: currentAmount.value
    }));
  }
};

const checkBalance = () => {
  return chipValue.value <= show.value.balance && chipValue.value >= currentAmount.value + bigBlindValue.value;
};

const pot = ref(1000)
const countdown = ref(30);
// -------------------------------------------------------------------------------------------- //

const dealPlayerCard = () => {
  const tl = gsap.timeline();
  playercards.value.forEach((card, index) => {
    const playerIndex = Math.floor((index) / 2);
    const positionGroup = playerCardPositions.value[playerIndex];
    gsap.set(`.game-card:nth-child(${index + 1})`, {
      opacity: 0,
      top: '9%',
      left: '47.5%',
    });
    tl.to(`.game-card:nth-child(${index + 1})`, {
      duration: 0.1,
      opacity: 1,
      top: `${positionGroup[(index) % 2].top}%`,
      left: `${positionGroup[(index) % 2].left}%`,
      size: 2,
      ease: 'power2.out',
    }, '+=0.2');
  })
}
const dealCommonCards = () => {
  const tl = gsap.timeline();
  commoncards.value.forEach((card, index) => {
    const positionGroup = commonCardPositions.value[index];
    gsap.set(`.common-card:nth-child(${index + 1})`, {
      opacity: 0,
      top: '9%',
      left: '47.5%',
    });
    tl.to(`.common-card:nth-child(${index + 1})`, {
      duration: 0.1,
      opacity: 1,
      top: `${positionGroup.top}%`,
      left: `${positionGroup.left}%`,
      size: 2,
      ease: 'power2.out',
    }, '+=0.2');
  })
}

let ourId = 0;
authGet('/users/me/')
  .then(response => {
    ourId = response.data.id;
  })
socket.addEventListener('message', (event) => {
  const eventData = JSON.parse(event.data);

  if (eventData.type === 'players_data') {
    players.value = [];
    const inputPlayers = eventData.players;
    inputPlayers.forEach((player: any) => {
      players.value.push({
        id: player.player_id,
        username: player.username,
        chips: player.chips,
        isMove: false,
        bigBlindStatus: false,
        smallBlindStatus: false,
        dealerStatus: false,
        isWinner: false,
        lastAction: ''
      })
    })

    let ourIndex = players.value.findIndex((p: any) => (p.id === ourId)) || 0;

    const playerCopy = ref<Player[]>([]);
    players.value.forEach((player: any, index: any) => {
      if (index >= ourIndex) {
        playerCopy.value.push(player);
      }
    })
    players.value.forEach((player: any, index: any) => {
      if (index < ourIndex) {
        playerCopy.value.push(player);
      }
    })
    players.value = playerCopy.value;
  }

  if (eventData.type === 'cards_dealt') {
    playercards.value = [];
    const inputCards = eventData.player_cards;
    inputCards.forEach((card: any) => {
      playercards.value.push({name: card + '.png'});
    })
    for (let i = 0; i < (countOfPlayer - 1) * 2; i++) {
      playercards.value.push({name: 'back.png'})
    }
    dealPlayerCard();
  }

  if (eventData.type === 'common_cards_dealt') {
    commoncards.value = [];
    const inputCards = eventData.cards;
    inputCards.forEach((card: any) => {
      commoncards.value.push({name: card + '.png'})
    })
    dealCommonCards();
  }

  if (eventData.type === 'countdown') {
    countdown.value = eventData.countdown;
  }

  if (eventData.type === 'player_left') {
    const playerIdLeft = eventData.player_id;
    players.value = players.value.filter((player: any) => player.id !== playerIdLeft);
  }

  if (eventData.type === 'player_joined') {
    if (eventData.player_id !== ourId) {
      players.value.push({
        id: eventData.player_id,
        username: eventData.username,
        chips: eventData.chips,
        isMove: false,
        bigBlindStatus: false,
        smallBlindStatus: false,
        dealerStatus: false,
        isWinner: false,
        lastAction: ''
      })
    }
  }

  if (eventData.type === 'game_started') {
    const dealerId = eventData.dealer_id;

    let ind = 0;
    players.value.forEach((player: any, index: any) => {
      if (player.id === dealerId) {
        player.dealerStatus = true;
        ind = index;
      }
    })
    players.value[(ind + 1) % 7].smallBlindStatus = true;
    players.value[(ind + 2) % 7].bigBlindStatus = true;
    players.value[(ind + 3) % 7].isMove = true;
  }

  if (eventData.type === 'action_confirmed') {
    const targetPlayer = players.value.find(player => player.id === eventData.player_id);
    if (targetPlayer) {
      targetPlayer.lastAction = eventData.action;
      targetPlayer.chips = eventData.chips_remaining
      chipsAction.value = eventData.chips_action
    }
  }

  if (eventData.type === 'awaiting_turn') {
    const targetPlayer = players.value.find(player => player.id === eventData.player_id);
    if (targetPlayer) {
      targetPlayer.isMove = true;
    }
    was_raised.value = !!eventData.was_raised;
    pot.value = eventData.bank;
    currentAmount.value = eventData.current_bet;
  }

})

const timer = setInterval(() => {
  if (countdown.value > 0) {
    countdown.value -= 1;
  } else {
    clearInterval(timer);
  }
}, 1000);

</script>

<style lang="sass" scoped>
.table-container
  position: absolute
  width: 80%
  background-image: url("/poker_table-removebg.png")
  background-size: cover
  min-height: 720px

.game-card
  position: absolute
  width: 4.5%
  z-index: 10

.common-card
  position: absolute
  width: 7%
  z-index: 10

.border-white
  border: 1px solid white
  box-shadow: 0 0 10px white

</style>
