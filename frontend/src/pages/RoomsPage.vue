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
          <q-input class="rounded-borders text-white" color="white "
                   :input-style="{color: 'white'}"
                   style="min-width: 250px; font-size: x-large; border-bottom: 1px solid white; color: white"
                   v-model="searchInput"
                   label="Search"
                   :label-color="'grey-1'"
          >
            <template v-slot:prepend>
              <q-icon name="search" color="white" />
            </template>
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
        <div v-for="room in paginatedAndFilteredRooms" :key="room">
          <q-item clickable v-ripple class="q-mt-sm" @click="joinRoom(room.id)">
            <span class="col-4">{{ room.name }}</span>
            <span class="col-2">{{ room.blind }}</span>
            <span class="col-5">{{ room.chips }}</span>
            <span style="margin-left: 15px">{{ room.players }}</span>
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
                     style="background-color: rgba(120, 0, 0, 0.9); font-size: x-large; "
                     label="Name"
                     label-color="black"
                     color="white"
                     :input-style="{color: 'white'}"
                     outlined
                     v-model="roomName"
            ></q-input>
            <q-input class="text-white  q-mt-sm rounded-borders"
                     style="background-color: rgba(120, 0, 0, 0.9); font-size: x-large"
                     label="Big blind"
                     label-color="black"
                     color="white"
                     :input-style="{color: 'white'}"
                     outlined
                     v-model="bigBlindValue"></q-input>
            <q-input class="text-white q-mt-sm rounded-borders"
                     style="background-color: rgba(120, 0, 0, 0.9); font-size: x-large"
                     label="Starting chips"
                     label-color="black"
                     color="white"
                     :input-style="{color: 'white'}"
                     outlined
                     v-model="startingChips"
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
import {ref, computed, onMounted, watch} from 'vue';
import {LocalStorage} from 'quasar';
import {authGet, authPost} from 'src/utils';
import {Router} from 'src/router';
import {useQuasar} from 'quasar';

let balance = 0;
authGet('/users/me/').then(response => {
  balance = response.data.chips;
})

const $q = useQuasar();

const roomList = ref([]);
const addRoom = ref(false);

const username = LocalStorage.getItem('username');
const accessToken = LocalStorage.getItem('accessToken')

onMounted(async () => {
  await authGet('/rooms/')
    .then(response => {
      const roomArray = response.data;

      roomArray.forEach((tuple) => {
        const id = tuple.id;
        const name = tuple.name;
        const max_players = tuple.max_players;
        const players = tuple.n_players;
        const chips = tuple.starting_chips;
        const blind = tuple.big_blind_value;

        roomList.value.push({
          id: id,
          name: name,
          blind: blind,
          chips: chips,
          players: players.toString() + '/' + max_players.toString()
        })
      })
    })
})

const itemsPerPage = 7;
const currentPage = ref(1);
const maxPages = computed(() => Math.ceil(roomList.value.length / itemsPerPage));

const paginatedAndFilteredRooms = computed(() => {
  const search = searchInput.value.toLowerCase();
  const filteredList = roomList.value.filter(room => room.name.toLowerCase().includes(search));
  const startIndex = (currentPage.value - 1) * itemsPerPage;
  const endIndex = startIndex + itemsPerPage;
  return filteredList.slice(startIndex, endIndex);
});


const changePage = (page) => {
  currentPage.value = page;
}

const roomName = ref('');
const bigBlindValue = ref(0);
const startingChips = ref(0);
const searchInput = ref('');

const handleNumericValue = (value, ref) => {
  if (value.toString() === '') {
    ref.value = 0;
  } else if (value.toString() === '0') {
    ref.value = 0;
  } else {
    ref.value = parseInt(value.toString(), 10);
  }
};

watch(bigBlindValue, (newValue) => {
  handleNumericValue(newValue, bigBlindValue);
});

watch(startingChips, (newValue) => {
  handleNumericValue(newValue, startingChips);
});

const createRoom = () => {
  authPost('/rooms/create/', {
    name: roomName.value,
    max_players: 7,
    starting_chips: startingChips.value,
    big_blind_value: bigBlindValue.value
  })
    .then(response => {
      const room_id = response.data.id;
      Router.push({path: '/game-room/' + room_id + '/'})
    })

  addRoom.value = false;
}
const joinRoom = (id) => {
  authGet('/rooms/')
    .then(response => {
      const roomArray = response.data;

      roomArray.forEach((tuple) => {
        if (tuple.id === id) {
          if (tuple.n_players > 7) {
            $q.notify({
              message: 'Not enough space',
              color: 'red-10',
              textColor: 'white',
              position: 'top',
              timeout: 1000,
            });
            return;
          } else if (!(balance >= tuple.starting_chips)) {
            $q.notify({
              message: 'Not enough Altushkas',
              color: 'red-10',
              textColor: 'white',
              position: 'top',
              timeout: 1000,
            });
            return;
          }
          Router.push({path: '/game-room/' + id + '/'})
        }
      })
    })
}
</script>

<style lang="sass" scoped>
body
  overflow: hidden
  height: 100%
  width: 100%


</style>
