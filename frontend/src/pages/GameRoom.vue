<template>
  <q-page class="column items-center justify-center">
    <div class="table-container">
      <img
        v-for="(card, index) in cards"
        :key="index"
        :src="`/cards/${card.name}.png`"
        class="game-card"
        :style="getCardStyle(index)"
        style="position: absolute; left: 47.5%; top: 9%; opacity: 0"
        alt=""/>
      <img
        src="/cards/back01.png"
        style="width: 5%; position: absolute; left: 47.5%; top: 9%; z-index: 999; pointer-events: auto;"
        @click="dealCards"
        alt=""/>
      <span style="position:absolute; left: 47%; top: 30%; font-size: x-large; color: white">
        Pot: {{ pot }}Å
      </span>
      <div v-for="(player,i) in players" :key="i">
        <q-card class="column items-center"
                style="position: absolute; min-width: 15%; min-height: 24%; background-color: rgba(0,0,0,0.6); color: white"
                :style="`top: ${playerPositions[i].top}%; left: ${playerPositions[i].left}%`"
        >
          <span style="font-size: x-large; bottom: 23%; position:absolute;">
          {{ player.username }}
        </span>
          <span style="font-size: x-large; bottom: 3%; position:absolute;">
          {{ player.balance }}Å
        </span>
        </q-card>
      </div>
    </div>
    <div class="row justify-center q-pa-md" style="position: absolute; bottom: 2%;">
      <div class="button-container">
        <q-btn
          style="font-size: 20px; background-color: #960018; color: #ffffff; width: 100px;
          height: 50px; box-shadow: 3px 3px 5px rgba(0, 0, 0, 0.3);"
          label="CHECK" class="q-mr-md"/>
        <q-btn
          style="font-size: 20px; background-color: #960018; color: #ffffff; width: 100px;
          height: 50px; box-shadow: 3px 3px 5px rgba(0, 0, 0, 0.3);"
          label="FOLD" class="q-mr-md"/>
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
                     style="font-size: 20px; "
                     maxlength="14"
                     :rules="[val => (val <= show.balance) || 'The entered value is greater than your balance']"
            />
          </q-card-section>
          <q-card-section class="text-h4 text-center" style="border: 1px solid white; padding: 10px; "
                          max="10000000000000">
            {{ chipValue }}Å
          </q-card-section>
          <q-card-actions align="center">
            <q-btn flat label="Submit" style="background-color: #960018;" @click="checkBalance" :disable="!checkBalance()" v-close-popup/>
            <q-btn flat label="Close" style="background-color: #960018;" v-close-popup/>
          </q-card-actions>
        </q-card>
      </q-dialog>

    </div>
  </q-page>
</template>

<script setup lang="ts">
import {ref, watch} from 'vue';
import gsap from 'gsap';
import {LocalStorage} from 'quasar';

let username = LocalStorage.getItem('username');

if (username === null)
  username = '';

interface Card {
  name: string;
}

interface CardPosition {
  top: number;
  left: number;
}

interface Player {
  username: string,
  balance: number,
}

const cards = ref<Card[]>([]);
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

const cardPositions = ref<CardPosition[][]>([
  // Table cards
  [
    {top: 40, left: 26.5},
    {top: 40, left: 36.5},
    {top: 40, left: 46.5},
    {top: 40, left: 56.5},
    {top: 40, left: 66.5},
  ],
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

const players = ref<Player[]>([
  {
    username: username.toString(),
    balance: 1000
  },
  {
    username: 'Vladik',
    balance: 9999
  },
  {
    username: 'Semen',
    balance: 100
  },
  {
    username: 'Ilia',
    balance: 228
  },
  {
    username: 'Jopic',
    balance: 322
  },
  {
    username: 'Rtomii',
    balance: 1337
  },
  {
    username: 'Danya',
    balance: 100000000
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

cards.value = [
  {name: 'hearts_ace'},
  {name: 'hearts_king'},
  {name: 'hearts_queen'},
  {name: 'hearts_jack'},
  {name: 'hearts_10'},

  {name: 'hearts_09'},
  {name: 'hearts_08'},

  {name: 'back'},
  {name: 'back'},

  {name: 'back'},
  {name: 'back'},

  {name: 'back'},
  {name: 'back'},

  {name: 'back'},
  {name: 'back'},

  {name: 'back'},
  {name: 'back'},

  {name: 'back'},
  {name: 'back'},
];

const pot = ref(1000)


let cardsDealt = false;

const cardsToDeal = 5;
let cardsDealtCount = 0;

const getCardStyle = (index: number) => {
  const isTableCard = index < cardsToDeal;

  const size = isTableCard ? '7%' : '4.5%';
  const initialOpacity = cardsDealt ? 1 : 0;

  return {
    position: 'absolute',
    width: size,
    zIndex: 10,
    opacity: initialOpacity,
  };
};

const dealCards = (): void => {
  const tl = gsap.timeline();

  if (!cardsDealt) {
    cards.value.forEach((card, index) => {
      if (index < cardsToDeal) {
        const positionGroup = cardPositions.value[0];
        gsap.set(`.game-card:nth-child(${index + 1})`, {
          opacity: 0,
          top: '9%',
          left: '47.5%',
        });

        tl.to(`.game-card:nth-child(${index + 1})`, {
          duration: 0.1,
          opacity: 1,
          top: `${positionGroup[index].top}%`,
          left: `${positionGroup[index].left}%`,
          ease: 'power2.out',
        }, '+=0.2');
        cardsDealtCount++;
      }
    });

    if (cardsDealtCount === cardsToDeal) {
      cardsDealt = true;
    }
  } else {
    cards.value.forEach((card, index) => {
      if (index >= cardsToDeal) {
        const playerIndex = Math.floor((index - cardsToDeal) / 2) + 1;
        const positionGroup = cardPositions.value[playerIndex];
        gsap.set(`.game-card:nth-child(${index + 1})`, {
          opacity: 0,
          top: '9%',
          left: '47.5%',
        });

        tl.to(`.game-card:nth-child(${index + 1})`, {
          duration: 0.1,
          opacity: 1,
          top: `${positionGroup[(index - cardsToDeal) % 2].top}%`,
          left: `${positionGroup[(index - cardsToDeal) % 2].left}%`,
          ease: 'power2.out',
        }, '+=0.2');
        cardsDealtCount++;
      }
    });
    cardsDealt = false;
    cardsDealtCount = 0;
  }
};
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

</style>
