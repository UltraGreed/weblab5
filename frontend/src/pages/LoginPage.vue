<script setup lang='ts'>
import {ref} from 'vue';
import {api} from 'src/boot/axios';
import {LocalStorage} from "quasar";
import {Router} from "src/router";

const email = ref('');
const password = ref('');
const username = ref('');

const isPwd = ref(true);

const errors = ref<string[]>([]);

const submitForm = () => {
  errors.value = [];
  const formData = {
    email: email.value,
    username: username.value,
    password: password.value
  }

  if (email.value === '' || username.value === '' || password.value === '')
    return;

  api.post('/auth/users/', formData)
      .then(response => {
        api.post('/auth/jwt/create/', {
          username: username.value,
          password: password.value
        })
            .then(response1 => {
              const data = response1.data;

              const accessToken = data.access;
              const refreshToken = data.refresh;

              LocalStorage.set('accessToken', accessToken);
              LocalStorage.set('refreshToken', refreshToken);
              LocalStorage.set('username', username);

              api.defaults.headers.common['Authorization'] = `Bearer ${accessToken}`;

              Router.push({path: '/rooms'});
            })
      })
      .catch(error => {
        if (error.response && error.response.data) {
          const errorData = error.response.data;
          for (const key in errorData) {
            for (let i = 0; i < errorData[key].length; i++) {
              errors.value.push(errorData[key][i]);
            }
          }
        }
      })
}

const closeBanner = () => {
  errors.value = [];
  return;
};
const tab = ref('login');


const username1 = ref('');
const password1 = ref('');
const errors1 = ref<string[]>([]);

const isPwd1 = ref(true);

const submitForm1 = () => {
  errors1.value = [];

  const formData = {
    username: username1.value,
    password: password1.value
  }

  if (username1.value === '' || password1.value === '')
    return;

  api.post('/auth/jwt/create/', formData)
      .then(response => {
        const data = response.data;

        const accessToken = data.access;
        const refreshToken = data.refresh;

        LocalStorage.set('accessToken', accessToken);
        LocalStorage.set('refreshToken', refreshToken);
        LocalStorage.set('username', username);

        api.defaults.headers.common['Authorization'] = `Bearer ${accessToken}`;

        Router.push({path: '/rooms'});
      })
      .catch(error => {
        if (error.response && error.response.data) {
          const errorData = error.response.data;
          for (const key in errorData) {
            errors1.value.push(errorData[key]);
          }
        }
      })
}
const closeBanner1 = () => {
  errors1.value = [];
  return;
};

</script>

<template>
  <q-page class="column justify-center items-center">
    <q-tabs
        v-model='tab'
        class='text-white'
    >
      <q-tab class="tab" name='login' label='Login'/>
      <q-tab class="tab" name='signup' label='SignUp'/>
    </q-tabs>
    <q-tab-panels v-model='tab'
                  animated
                  :style="{opacity:0.8}"
                  style=" max-width: 25%;
                  background-color: black;
                  border-radius: 10px; min-height: 520px"
                  class='q-px-lg q-pt-lg full-width column items-center'>
      <q-tab-panel name='login' style="">
        <q-card class="bg-black">
          <q-card-section class="row justify-center">
            <span style="color: antiquewhite; font-size: xxx-large">SIGN IN</span>
          </q-card-section>
          <q-form class='fit column' @submit='submitForm1'>
            <q-card-section class='q-pb-none'>
              <q-input class="rounded-borders text-white"
                       style="background-color: darkred; font-size: x-large"
                       label="Username"
                       label-color="black"
                       color="white"
                       :input-style="{color: 'white'}"
                       outlined
                       v-model="username1"
              >
              </q-input>
              <q-input class="text-white q-mt-lg rounded-borders"
                       style="background-color: darkred; font-size: x-large"
                       label="Password"
                       label-color="black"
                       color="white"
                       :input-style="{color: 'white'}"
                       outlined
                       v-model="password1"
                       :type="isPwd1 ? 'password' : 'text'"
              >
                <template v-slot:append>
                  <q-icon
                      :name="isPwd1 ? 'visibility_off' : 'visibility'"
                      class='cursor-pointer'
                      color="black"
                      @click='isPwd1 = !isPwd1'
                  />
                </template>
              </q-input>
            </q-card-section>
            <q-card-section>
              <q-banner
                  v-if='errors1.length > 0'
                  class='relative fit text-white rounded-borders q-mt-sm q-mb-md'
                  style=' background-color: darkred'
                  @submit.prevent='submitForm1'
              >
                <q-card-section>
              <span class="row justify-center" style="font-size: medium" v-for="err in errors1" :key="err">
                {{ err }}
              </span>
                </q-card-section>
                <q-btn round flat size='8px'
                       @click='closeBanner1'
                       class='q-mt-lg q-mr-md absolute-top-right'
                       text-color='white'
                       icon='close'
                />
              </q-banner>
              <div class='row full-width justify-center q-pt-sm q-pb-lg q-px-md'>
                <q-btn class='col-6' style="background-color: darkred; min-height: 50px; font-size: larger" text-color="white"
                       label='sign in'
                       type='submit'/>
              </div>
            </q-card-section>
          </q-form>
        </q-card>
      </q-tab-panel>
      <q-tab-panel name='signup' style="">
        <q-card class="bg-black">
          <q-card-section class="row justify-center">
            <span style="color: antiquewhite; font-size: xxx-large">SIGN UP</span>
          </q-card-section>
          <q-form class='fit column' @submit='submitForm'>
            <q-card-section class='q-pb-none'>
              <q-input class="rounded-borders text-white"
                       style="background-color: darkred; font-size: x-large"
                       label="Email"
                       label-color="black"
                       color="white"
                       :input-style="{color: 'white'}"
                       outlined
                       v-model="email"
              >
              </q-input>
              <q-input class="rounded-borders text-white q-mt-lg"
                       style="background-color: darkred; font-size: x-large"
                       label="Username"
                       label-color="black"
                       color="white"
                       :input-style="{color: 'white'}"
                       outlined
                       v-model="username"
              >
              </q-input>
              <q-input class="text-white q-mt-lg rounded-borders"
                       style="background-color: darkred; font-size: x-large"
                       label="Password"
                       label-color="black"
                       color="white"
                       :input-style="{color: 'white'}"
                       outlined
                       v-model="password"
                       :type="isPwd ? 'password' : 'text'"
              >
                <template v-slot:append>
                  <q-icon
                      :name="isPwd ? 'visibility_off' : 'visibility'"
                      class='cursor-pointer'
                      color="black"
                      @click='isPwd = !isPwd'
                  />
                </template>
              </q-input>
            </q-card-section>
            <q-card-section>
              <q-banner
                  v-if='errors.length > 0'
                  class='relative fit text-white rounded-borders q-mt-sm q-mb-md'
                  style=' background-color: darkred'
                  @submit.prevent='submitForm'
              >
                <q-card-section>
              <span class="row justify-center" style="font-size: medium" v-for="err in errors" :key="err">
                {{ err }}
              </span>
                </q-card-section>
                <q-btn round flat size='8px'
                       @click='closeBanner'
                       class='q-mt-md q-mr-sm absolute-top-right'
                       style="font-size: small"
                       text-color='black'
                       icon='close'
                />
              </q-banner>
              <div class='row full-width justify-center q-pt-sm q-pb-lg q-px-md'>
                <q-btn class='col-6' style="background-color: darkred; min-height: 50px; font-size: medium" text-color="white"
                       label='Sign up'
                       type='submit'/>
              </div>
            </q-card-section>
          </q-form>
        </q-card>
      </q-tab-panel>
    </q-tab-panels>
  </q-page>
</template>

<style lang="sass">

</style>
