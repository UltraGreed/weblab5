<template>
  <q-page class="column items-center justify-center">
    <div class="table-container">
      <img
        v-for="(card, index) in cards"
        :key="index"
        :src="card.faceUp ? `/cards/${card.name}.png` : `/cards/back01.png`"
        class="game-card"
        :style="{ top: `${cardPositions[index].top}%`, left: `${cardPositions[index].left}%`, transform: `rotate(${card.rotation}deg)` }"
        @click="flipCard(index)"
      />
      <img
        src="/cards/back01.png"
        style="width: 5%; position: absolute; left: 47.5%; top: 9%; z-index: 999; pointer-events: auto;"
        @click="dealCards"
      />
      <q-card style="position: absolute;left: 8%; min-width: 15%; min-height: 20%;background-color: rgba(0, 0, 0, 0.6); color: white"

      />
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

<script setup>
import {ref} from 'vue';

const cards = ref([]);
const cardPositions = ref([
  {top: 40, left: 26.5},
  {top: 40, left: 36.5},
  {top: 40, left: 46.5},
  {top: 40, left: 56.5},
  {top: 40, left: 66.5},
]);


const dealCards = () => {
  cards.value = [
    { name: 'card1', rotation: 0, faceUp: false },
    { name: 'card2', rotation: 0, faceUp: false },
    { name: 'card3', rotation: 0, faceUp: false },
    { name: 'card4', rotation: 0, faceUp: false },
    { name: 'card5', rotation: 0, faceUp: false },
  ];

  cards.value.forEach((card, index) => {
    setTimeout(() => {
      moveCardToPosition(index);
    }, index * 1000);
  });
};

const moveCardToPosition = (index) => {

  setTimeout(() => {
    flipCard(index);
  }, 1000);
};

const flipCard = (index) => {
  cards[index].rotation = 180;
  cards[index].faceUp = !cards[index].faceUp;

  setTimeout(() => {
    cards[index].rotation = 0;
  }, 500);
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
  transition: all 1s ease-in-out
  transform-origin: top left
  animation: dealAnimation 1s ease-in-out forwards

@keyframes dealAnimation
  0%
    transform: scale(0)
  100%
    transform: scale(1)
</style>
