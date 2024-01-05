<template>
  <q-page class="column justify-center items-center">
    <q-card :style="{opacity:0.8}" style="min-width: 500px; background-color: black; border-radius: 10px">
      <q-card-section class="row justify-center text-h2">
        <span style="color: antiquewhite">Sign Up</span>
      </q-card-section>
      <q-card-section>
        <q-input class="rounded-borders text-white"
                 style="background-color: darkred; font-size: x-large"
                 label="Email"
                 label-color="white"
                 color="white"
                 :input-style="{color: 'white'}"
                 outlined
                 v-model="email"
        >
        </q-input>
        <q-input class="rounded-borders text-white q-mt-lg"
                 style="background-color: darkred; font-size: x-large"
                 label="Username"
                 label-color="white"
                 color="white"
                 :input-style="{color: 'white'}"
                 outlined
                 v-model="username"
        >
        </q-input>
        <q-input class="text-white q-mt-lg rounded-borders"
                 style="background-color: darkred; font-size: x-large"
                 label="Password"
                 label-color="white"
                 color="white"
                 :input-style="{color: 'white'}"
                 outlined
                 v-model="password"
        >
        </q-input>
      </q-card-section>
      <q-card-section class="row justify-center">
        <q-btn label="Submit"
               style="background-color: darkred; min-width: 150px"
               text-color="white"
               @click="SubmitForm"
        >
        </q-btn>
      </q-card-section>
    </q-card>
  </q-page>
</template>

<script setup>
import {ref} from 'vue';
import {api} from 'src/boot/axios';
import {LocalStorage} from "quasar";
import {Router} from "src/router";

const email = ref('');
const password = ref('');
const username = ref('');

const SubmitForm = () => {

  api.post('/auth/users/', {
    email: email.value,
    username: username.value,
    password: password.value
  })
    .then(response => {
      api.post('/auth/jwt/create/', {
        username: username.value,
        password: password.value
      })
        .then(response =>{
          const data = response.data;

          const accessToken = data.access;
          const refreshToken = data.refresh;

          LocalStorage.set('accessToken', accessToken);
          LocalStorage.set('refreshToken', refreshToken);
          LocalStorage.set('username', username);
          LocalStorage.set('email', email);

          api.defaults.headers.common['Authorization'] = `Bearer ${accessToken}`;

          Router.push({ path: '/rooms'});
        })
    })
}

</script>

<style lang="sass" scoped>
</style>
