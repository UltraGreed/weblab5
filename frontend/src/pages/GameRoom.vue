<template>
  <q-page class="column items-center justify-center">
    <div class="table-container">
      <img
        v-for="(card, index) in playercards"
        :key="index"
        :src="`/cards/${card.name}`"
        class="game-card"
        :style="{width: 4.5+'%'}"
        style="position: absolute; left: 47.5%; top: 9%; opacity: 0"
        alt=""
        draggable="false"
      />
      <img
        src="/cards/back01.png"
        style="width: 5%; position: absolute; left: 47.5%; top: 9%; z-index: 999; pointer-events: auto;"
        @click="dealPlayerCard"
        alt=""
        draggable="false"
      />
      <span style="position:absolute; left: 47%; top: 30%; font-size: x-large; color: white">
        Pot: {{ pot }}Å
      </span>
      <div v-for="(player,i) in players" :key="i">
        <div class="column items-center"
             style="position: absolute; z-index: 1"
             :style="`top: ${playerPositions[i].top + 15}%; left: ${playerPositions[i].left-13.5}%`"
             v-if="player.dealer_status"
        >
          <img src="/dealer.png" style="width: 10%">
        </div>
        <div class="column items-center"
             style="position: absolute; z-index: 1"
             :style="`top: ${playerPositions[i].top + 15}%; left: ${playerPositions[i].left+3}%`"
             v-if="player.small_blind_status"
        >
          <img src="/sb.png" style="width: 17%">
        </div>
        <div class="column items-center"
             style="position: absolute; z-index: 1"
             :style="`top: ${playerPositions[i].top + 15}%; left: ${playerPositions[i].left+3}%`"
             v-if="player.big_blind_status"
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
          {{ player.balance }}Å
        </span>
          <q-card class="transparent" v-if="player.is_winner"
                  style="z-index: 1; color: gold; max-width: 100px; font-size: x-large; bottom: -40%; position: absolute;">
            WINNER!
          </q-card>
        </q-card>
        <q-card class="column items-center"
                style="position: absolute; min-width: 15%; min-height: 5%; background-color: rgba(0,0,0,0.6);
          color: white; border-top: 1px solid white;"
                :style="`top: ${playerPositions[i].top + 24}%; left: ${playerPositions[i].left}%`"
        >
          <span style="font-size: x-large; bottom: 3%; position:absolute;">
            RAISE
          </span>
        </q-card>
      </div>
    </div>
    <div class="row justify-center q-pa-md" style="position: absolute; bottom: -1%;">
      <div class="button-container">
        <q-btn
          style="font-size: 20px;
          background-color: #960018;
          color: #ffffff; width: 100px;
          height: 50px;
          box-shadow: 3px 3px 5px rgba(0, 0, 0, 0.3);"
          label="CHECK"
          class="q-mr-md"/>
        <q-btn
          style="font-size: 20px; background-color: #960018; color: #ffffff; width: 100px; height: 50px; box-shadow: 3px 3px 5px rgba(0, 0, 0, 0.3);"
          label="FOLD"
          class="q-mr-md"
        />
        <q-btn style="font-size: 20px; background-color: #960018; color: #ffffff; width: 100px;
         height: 50px; box-shadow: 3px 3px 5px rgba(0, 0, 0, 0.3);" label="RAISE"
               @click="show.isVisible = !show.isVisible; show.balance = players[0].balance;"/>
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
                  {label: 'min', value: 10},
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
    <q-btn @click="dealPlayerCard">3123</q-btn>
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

interface Player {
  id: number,
  username: string,
  balance: number,
  isMove: boolean
  small_blind_status: boolean,
  big_blind_status: boolean,
  dealer_status: boolean,
  is_winner: boolean,
  isFolded: boolean
}

const players = ref<Player[]>([
  {
    id: 1,
    username: username.toString(),
    balance: 1000,
    small_blind_status: false,
    big_blind_status: false,
    dealer_status: true,
    is_winner: false,
    isMove: true,
    isFolded: false
  },
  {
    id: 2,
    username: 'Vladik',
    balance: 9999,
    isMove: false,
    small_blind_status: true,
    big_blind_status: false,
    dealer_status: false,
    is_winner: false,
    isFolded: false
  },
  {
    id: 3,
    username: 'Semen',
    balance: 100,
    isMove: false,
    small_blind_status: false,
    big_blind_status: true,
    dealer_status: false,
    is_winner: false,
    isFolded: false
  },
  {
    id: 4,
    username: 'Ilia',
    balance: 228,
    isMove: false,
    small_blind_status: false,
    big_blind_status: false,
    dealer_status: false,
    is_winner: true,
    isFolded: false
  },
  {
    id: 5,
    username: 'Jopic',
    balance: 322,
    isMove: false,
    small_blind_status: false,
    big_blind_status: false,
    dealer_status: false,
    is_winner: false,
    isFolded: false
  },
  {
    id: 6,
    username: 'Rtomii',
    balance: 1337,
    isMove: false,
    small_blind_status: false,
    big_blind_status: false,
    dealer_status: false,
    is_winner: false,
    isFolded: false
  },
  {
    id: 7,
    username: 'Danya',
    balance: 100000000,
    isMove: false,
    small_blind_status: false,
    big_blind_status: false,
    dealer_status: false,
    is_winner: false,
    isFolded: false
  }
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

const url = window.location.href;
const arr = url.split('/')
authGet(`/rooms/detail/${arr[arr.length - 2]}/`)
  .then(response => {
    countOfPlayer = response.data.n_players;
  })
const socket = new WebSocket(`ws://localhost:8000/ws/room/${arr[arr.length - 2]}/?token=${LocalStorage.getItem('accessToken')}`)

const show = ref<{ isVisible: boolean, balance: number }>({isVisible: false, balance: 0});
const chipValue = ref<number>(0);

watch(chipValue, (newValue) => {
  if (newValue.toString() === '') {
    chipValue.value = 0;
  } else if (newValue.toString() === '0') {
    chipValue.value = 0;
  } else {
    chipValue.value = parseInt(newValue.toString(), 10);
  }
});

const checkBalance = () => {
  return chipValue.value <= show.value.balance;
};

const pot = ref(1000)

// const fold = (): void => {
// };

// const animateFoldedPlayerCards = () => {
//   const tl = gsap.timeline();
//
//   const currentPlayerIndex = 0;
//
//   playercards.value.forEach((card, index) => {
//     const playerIndex = Math.floor((index) / 2);
//
//     if (playerIndex === currentPlayerIndex) {
//       const positionGroup = playerCardPositions.value[playerIndex];
//       tl.to(`.game-card:nth-child(${index + 1})`, {
//         duration: 0.5,
//         scale: 0.9,
//         ease: 'power2.out',
//       })
//         .to(`.game-card:nth-child(${index + 1})`, {
//           duration: 0.5,
//           opacity: 0.6,
//           ease: 'power2.out',
//         }, '-=0.5');
//     }
//   });
// };


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

socket.addEventListener('message', (event) => {
  const eventData = JSON.parse(event.data);

  const message = eventData.message;

  if (message.type === 'cards_dealt') {
    playercards.value = [];
    const inputCards = message.player_cards;
    inputCards.forEach((card: any) => {
      playercards.value.push({name: card + '.png'});
    })
    for (let i = 0; i < (countOfPlayer - 1) * 2; i++) {
      playercards.value.push({name: 'back.png'})
    }
    dealPlayerCard();
  }

})

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
  width: 7%
  z-index: 10

.border-white
  border: 1px solid white
  box-shadow: 0 0 10px white

</style>
