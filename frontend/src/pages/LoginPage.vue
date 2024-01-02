<template>
  <q-page class="column justify-center items-center">
    <q-card :style="{opacity:0.8}" style="min-width: 500px; background-color: black; border-radius: 10px">
      <q-card-section class="row justify-center text-h2">
        <span style="color: antiquewhite">Sign In</span>
      </q-card-section>
      <q-card-section>
        <q-input class="rounded-borders text-white"
                 style="background-color: darkred; font-size: x-large"
                 label="Username"
                 label-color="white"
                 color="white"
                 :input-style="{color: 'white'}"
                 outlined
        >
        </q-input>
        <q-input class="text-white q-mt-lg rounded-borders"
                 style="background-color: darkred; font-size: x-large"
                 label="Password"
                 label-color="white"
                 color="white"
                 :input-style="{color: 'white'}"
                 outlined
        >
        </q-input>
      </q-card-section>
      <q-card-section class="row justify-center">
        <q-btn label="Submit"
               style="background-color: darkred; min-width: 150px"
               text-color="white">
        </q-btn>
      </q-card-section>
    </q-card>
  </q-page>
</template>

<script setup>
import {ref} from 'vue';

</script>

<style lang="sass" scoped>
</style>
