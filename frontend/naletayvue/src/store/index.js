import { createStore } from 'vuex';
import createPersistedState from 'vuex-persistedstate';
import Cookies from 'js-cookie';
import userModule from './modules/UserModule';
import productModule from './modules/ProductModule';
import orderModule from './modules/OrderModule';
import cartModule from './modules/CartModule';

const localStoragePlugin = createPersistedState({
  key: 'naletay_cart',
  paths: ['cart'],
  storage: window.localStorage,
});

const cookieStorage = {
  getItem: (key) => Cookies.get(key),
  setItem: (key, value) => Cookies.set(key, value, { expires: 30 }),
  removeItem: (key) => Cookies.remove(key),
};

const cookiePlugin = createPersistedState({
  key: 'naletay_user_data',
  paths: ['user', 'user.accessToken'],
  storage: cookieStorage,
});

const store = createStore({
  modules: {
    user: userModule,
    products: productModule,
    orders: orderModule,
    cart: cartModule
  },
  plugins: [localStoragePlugin, cookiePlugin]
});

export default store;
