<template>
  <q-page class="column items-center justify-center">
    <div class="table-container">
      <img
        v-for="(card, index) in cards"
        :key="index"
        :src="`/cards/${card.name}.png`"
        class="game-card"
        style="position: absolute; left: 47.5%; top: 9%; opacity: 0"
      />
      <img
        src="/cards/back01.png"
        style="width: 5%; position: absolute; left: 47.5%; top: 9%; z-index: 999; pointer-events: auto;"
        @click="dealCards"
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
const cardPositions = ref<CardPosition[]>([
  { top: 40, left: 26.5 },
  { top: 40, left: 36.5 },
  { top: 40, left: 46.5 },
  { top: 40, left: 56.5 },
  { top: 40, left: 66.5 },
]);

cards.value =[
  {name: 'card1'},
  {name: 'card2'},
  {name: 'card3'},
  {name: 'card4'},
  {name: 'card5'}
]

const dealCards = (): void => {
  const tl = gsap.timeline();

  // Спавн карты на колоде
  cards.value.forEach((card, index) => {
    gsap.set(`.game-card:nth-child(${index + 1})`, {
       opacity: 0, // Устанавливаем начальную прозрачность
      top: '9%',
      left: '47.5%',
    });
  });

  // Анимация перемещения карт на свои слоты с задержкой
  cards.value.forEach((card, index) => {
    tl.to(`.game-card:nth-child(${index + 1})`, {
      duration: 0.1, // Время анимации
      opacity:1,
      top: `${cardPositions.value[index].top}%`,
      left: `${cardPositions.value[index].left}%`,
      ease: 'power2.out',
    }, `+=0.2`); // Задержка между картами
  });
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

</style>
