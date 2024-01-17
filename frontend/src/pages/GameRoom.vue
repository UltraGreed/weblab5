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
      />
      <img
        src="/cards/back01.png"
        style="width: 5%; position: absolute; left: 47.5%; top: 9%; z-index: 999; pointer-events: auto;"
        @click="dealCards"
       />
      />
      <q-card style="position: absolute;left: 8%; min-width: 15%; min-height: 20%;background-color: rgba(0, 0, 0, 0.6); color: white"/>
      <q-card style="position: absolute;right: 8%; min-width: 15%; min-height: 20%;background-color: rgba(0, 0, 0, 0.6); color: white"/>
      <q-card style="position: absolute;min-width: 15%; min-height: 20%; top: 40%;background-color: rgba(0, 0, 0, 0.6); color: white"/>
      <q-card style="position: absolute;min-width: 15%; min-height: 20%; top: 40%; right: 0%;background-color: rgba(0, 0, 0, 0.6); color: white"/>
      <q-card style="position: absolute;left: 8%; min-width: 15%; min-height: 20%; top: 80%;background-color: rgba(0, 0, 0, 0.6); color: white"/>
      <q-card style="position: absolute; left: 42.5%; max-width: 15%; max-height: 40%; top: 76%;background-color: rgba(0, 0, 0, 0.6); color: white"
              class="column items-center"
      >
        <div class="row justify-center">
          <img src="/cards/clubs_05.png" style="width: 30%" class="q-mr-sm">
          <img src="/cards/clubs_05.png" style="width: 30%">
        </div>
        <span style="font-size: x-large">
          boggruz
        </span>
        <span style="font-size: x-large">
          9999$
        </span>
      </q-card>
      <q-card style="position: absolute;right:8%; min-width: 15%; min-height: 20%; top: 80%;background-color: rgba(0, 0, 0, 0.6); color: white"/>
    </div>
  </q-page>
</template>

<script setup lang="ts">

import {ref} from 'vue';
import gsap from 'gsap';

interface Card {
  name: string;
}

interface CardPosition {
  top: number;
  left: number;
}

const cards = ref<Card[]>([]);

const cardPositions = ref<CardPosition[][]>([
  // Table cards
  [
    { top: 40, left: 26.5 },
    { top: 40, left: 36.5 },
    { top: 40, left: 46.5 },
    { top: 40, left: 56.5 },
    { top: 40, left: 66.5 },
  ],
  // Player 1 cards
  [
    { top: 76, left: 45.3 },
    { top: 76, left: 50.3 },
  ],
  // Player 2 cards
  [
    { top: 80, left: 11 },
    { top: 80, left: 16 },
  ],
  // Player 3 cards
  [
    { top: 40, left: 3 },
    { top: 40, left: 8 },
  ],
  // Player 4 cards
  [
    { top: 3, left: 11 },
    { top: 3, left: 16 },
  ],
  // Player 5 cards
  [
    { top: 3, left: 80 },
    { top: 3, left: 85 },
  ],
  // Player 6 cards
  [
    { top: 40, left: 88 },
    { top: 40, left: 93 },
  ],
  // Player 7 cards
  [
    { top: 80, left: 80 },
    { top: 80, left: 85 },
  ]
])


cards.value = [
  { name: 'hearts_ace' },
  { name: 'hearts_king' },
  { name: 'hearts_queen' },
  { name: 'hearts_jack' },
  { name: 'hearts_10' },

  { name: 'hearts_09' },
  { name: 'hearts_08' },

  { name: 'hearts_07' },
  { name: 'hearts_06' },

  { name: 'hearts_05' },
  { name: 'hearts_04' },

  { name: 'hearts_03' },
  { name: 'hearts_02' },

  { name: 'spades_02' },
  { name: 'spades_03' },

  { name: 'spades_04' },
  { name: 'spades_05' },

  { name: 'spades_06' },
  { name: 'spades_07' },
];

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
