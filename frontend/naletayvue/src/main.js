import { createApp } from 'vue';
import App from '@/App.vue';
import router from '@/router';
import Cart from '@/classes/cart/cart.js';
import NotificationManager from '@/classes/objects/NotificationManager.js';
import ChatList from '@/classes/chat/chatList.js';
import store from '@/store';

const app = createApp(App);

const notificationManager = new NotificationManager(4);
const chatsManager = new ChatList();
const cartInstance = new Cart(store);

app.provide('notificationManager', notificationManager);
app.provide('chatsManager', chatsManager);
app.provide('Cart', cartInstance);

app.use(store);
app.use(router);

app.mount('#app');
