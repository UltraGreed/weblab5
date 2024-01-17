import {RouteRecordRaw} from 'vue-router';

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    component: () => import('layouts/LoginLayout.vue'),
    children: [
      {
        path: '',
        component: () => import('pages/LoginPage.vue'),
      },
    ],
  },
{
    path: '/',
    component: () => import('layouts/AuthedLayout.vue'),
    children: [
      {
        path: 'rooms',
        component: () => import('pages/RoomsPage.vue'),
      },
      {
        path: 'game-room',
        component: () => import('pages/GameRoom.vue')
      }
    ],
  },
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue'),
  },
];

export default routes;
