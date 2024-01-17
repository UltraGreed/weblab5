<template>
  <q-page class="column items-center" style="padding-top: 100px">
    <q-card flat
            style="min-width: 60%; min-height: 670px;background-color: rgba(0, 0, 0, 0.4);"
            class="q-pa-xl"
    >
      <q-card-section class="row justify-between">
        <div>
          <span class="text-white text-h2 oswald-regular">ROOMS</span>
        </div>
        <div>
          <q-input class="rounded-borders text-white" color="white"
                   :input-style="{color: 'white'}"
                   style="min-width: 250px; font-size: x-large">
            <q-btn flat icon="search" size="lg">
            </q-btn>
          </q-input>
        </div>
      </q-card-section>
      <q-splitter horizontal class="bg-white q-mb-none q-pb-none">
      </q-splitter>
      <q-list bordered class="text-white text-h5" style="margin-top: -5px">
        <q-item class="row">
          <span class="col-4"></span>
          <span class="col-2">BET</span>
          <span class="col-5">STACK</span>
          <span style="margin-left: -13px">PLAYERS</span>
        </q-item>
        <q-splitter horizontal class="bg-white q-mb-none"/>
        <div v-for="room in paginatedRooms" :key="room">
          <q-item clickable v-ripple class="q-mt-sm">
            <span class="col-4">{{ room.name }}</span>
            <span class="col-2">{{ room.blind }}</span>
            <span class="col-5">{{ room.bank }}</span>
            <span style="margin-left: 15px">{{ room.people }}</span>
          </q-item>
          <q-splitter horizontal class="bg-white"></q-splitter>
        </div>
      </q-list>
      <q-pagination v-model="currentPage"
                    :max="maxPages"
                    color="white"
                    flat
                    active-color="transparent"
                    class="q-mb-md"
                    @input="changePage"
                    style="position: absolute; bottom: 10px; right: 5%"
      />
      <q-btn @click="addRoom = true"
             label="Create Room"
             text-color="white"
             size="lg"
             style="position: absolute; bottom: 15px; left:5%; background-color: rgba(100, 0, 0, 0.9)"
      >
      </q-btn>
      <q-dialog v-model="addRoom">
        <q-card style="min-width: 30%; min-height: 50%; background-color: rgba(36, 36 , 36 , 0.99)"
                class="column items-center">
          <q-card-section class="text-white text-h3 q-mt-lg">ROOM SETTINGS</q-card-section>
          <q-card-section class="column q-pt-none justify-start" style="min-width: 300px">
            <q-input class="text-white q-mt-lg rounded-borders"
                     style="background-color: rgba(120, 0, 0, 0.9); font-size: x-large"
                     label="name"
                     label-color="black"
                     color="white"
                     :input-style="{color: 'white'}"
                     outlined
                     v-model="roomName"
            ></q-input>
            <q-input class="text-white  q-mt-sm rounded-borders"
                     style="background-color: rgba(120, 0, 0, 0.9); font-size: x-large"
                     label="bet"
                     label-color="black"
                     color="white"
                     :input-style="{color: 'white'}"
                     outlined
                     v-model="roomBet"></q-input>
            <q-input class="text-white q-mt-sm rounded-borders"
                     style="background-color: rgba(120, 0, 0, 0.9); font-size: x-large"
                     label="stack"
                     label-color="black"
                     color="white"
                     :input-style="{color: 'white'}"
                     outlined
                     v-model="stack"
            ></q-input>
          </q-card-section>
          <q-btn
            label="SUBMIT"
            text-color="white"
            size="lg"
            style=" background-color: rgba(100, 0, 0, 0.9); min-width: 150px"
            class="q-mt-md"
            @click="createRoom"
          >
          </q-btn>
        </q-card>
      </q-dialog>
    </q-card>
  </q-page>
</template>

<script setup>
import {ref, computed} from 'vue';
import {LocalStorage} from "quasar";
import {authGet} from "src/utils";

const roomList = ref([
  {
    name: 'room1',
    blind: '25$',
    bank: '1000$',
    people: '1/6'
  },
  {
    name: 'room2',
    blind: '50$',
    bank: '2000$',
    people: '2/6'
  },
  {
    name: 'room3',
    blind: '75$',
    bank: '3000$',
    people: '3/6'
  },
  {
    name: 'room4',
    blind: '100$',
    bank: '4000$',
    people: '4/6'
  },
  {
    name: 'room5',
    blind: '125$',
    bank: '5000$',
    people: '5/6'
  }, {
    name: 'room1',
    blind: '25$',
    bank: '1000$',
    people: '1/6'
  },
  {
    name: 'room2',
    blind: '50$',
    bank: '2000$',
    people: '2/6'
  },
  {
    name: 'room3',
    blind: '75$',
    bank: '3000$',
    people: '3/6'
  },
  {
    name: 'room4',
    blind: '100$',
    bank: '4000$',
    people: '4/6'
  },
  {
    name: 'room5',
    blind: '125$',
    bank: '5000$',
    people: '5/6'
  }, {
    name: 'room1',
    blind: '25$',
    bank: '1000$',
    people: '1/6'
  },
  {
    name: 'room2',
    blind: '50$',
    bank: '2000$',
    people: '2/6'
  },
  {
    name: 'room3',
    blind: '75$',
    bank: '3000$',
    people: '3/6'
  },
  {
    name: 'room4',
    blind: '100$',
    bank: '4000$',
    people: '4/6'
  },
  {
    name: 'room5',
    blind: '125$',
    bank: '5000$',
    people: '5/6'
  }
]);
const addRoom = ref(false);

const username = LocalStorage.getItem('username');
const accessToken = LocalStorage.getItem('accessToken')

const itemsPerPage = 7;
const currentPage = ref(1);
const maxPages = computed(() => Math.ceil(roomList.value.length / itemsPerPage));
const paginatedRooms = computed(() => {
  const startIndex = (currentPage.value - 1) * itemsPerPage;
  const endIndex = startIndex + itemsPerPage;
  return roomList.value.slice(startIndex, endIndex);
});

const changePage = (page) => {
  currentPage.value = page;
}

const roomName = ref('');
const roomBet = ref(0);
const stack = ref(0);

const createRoom = () => {
  api.post('/rooms/create/', {
    name: roomName,
    bet: roomBet,
    stack: stack
  })
    .then(response => {
      name = response.data.name;

      const socket = new WebSocket('ws://127.0.0.1:8000/ws/' + name + '/');
    })
}

</script>

<style lang="sass" scoped>

</style>
