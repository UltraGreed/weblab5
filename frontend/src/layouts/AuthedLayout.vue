<template>
  <q-layout view='hHh Lpr fFf' class="background">
    <q-header elevated style="background-color: #1D1D1D">
      <q-toolbar>
        <q-toolbar-title>
          <q-btn flat padding="sm" :to="'/rooms'">
            <span class="text-h3">POKERCOCK</span>
          </q-btn>
        </q-toolbar-title>
        <div class="row col-2">
          <span class="text-h5">BALANCE: 9999$</span>
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
          <span class="text-white text-h2 q-pt-lg"> ILUHA POPICH</span>
          <span class="text-white text-h3 q-pt-lg"> SUCK MY COCK</span>
          <span class="text-white text-h4 q-pt-lg"> POSOSOV MEDA</span>
        </q-card>
      </q-dialog>
      <router-view/>
    </q-page-container>
  </q-layout>
</template>

<script setup lang='ts'>
import {ref} from 'vue';

const profile = ref(false);
</script>

<style lang="sass" scoped>
.background
  background: url("public/1.jpg")
  background-size: 1920px 1080px
</style>

