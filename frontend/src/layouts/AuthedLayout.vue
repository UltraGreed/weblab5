<template>
  <q-layout view='hHh Lpr fFf' class="background">
    <q-header elevated style="background-color: #1D1D1D">
      <q-toolbar>
        <q-toolbar-title>
          <q-btn flat padding="sm" :to="'/rooms'">
            <span class="text-h3">POKERSCUF</span>
          </q-btn>
        </q-toolbar-title>
        <div class="row col-2">
          <span class="text-h5">BALANCE: {{ balance }}Å</span>
        </div>
        <div class="row">
          <q-btn @click="profile = true" padding="sm" flat icon="account_circle" class="text-h5"></q-btn>
        </div>
      </q-toolbar>
    </q-header>
    <q-page-container>
      <q-dialog v-model="profile">
        <q-card style="min-width: 30%; min-height: 50%; background-color: #1D1D1D"
                class="column items-center">
          <q-card-section style="color:white" class="text-h2">
            Profile
          </q-card-section>
          <q-card-section style="color: white" class="text-h3">
            username: {{ username }}
          </q-card-section>
          <q-card-section style="color: white" class="text-h4 column">
            <span>Enter your phone number</span>
            <q-slider label v-model="telephone" :min="0" :max="100000000000" class="q-mt-sm"/>
          </q-card-section>
          <q-card-section>
            <q-btn label="Submit" style="color:white" size="20px"></q-btn>
          </q-card-section>
        </q-card>
      </q-dialog>
      <router-view/>
    </q-page-container>
  </q-layout>
</template>

<script setup lang='ts'>
import {ref} from 'vue';
import {authGet} from "src/utils";

const balance = ref(0);
const username = ref('')
;
authGet('/users/me/').then(response => {
  balance.value = response.data.chips;
  username.value = response.data.username;
})


const profile = ref(false);
const telephone = ref('');
</script>

<style lang="sass" scoped>
.background
  background: url("/1.jpg")
  background-size: 1920px 1080px
</style>

