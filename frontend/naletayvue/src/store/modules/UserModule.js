import api from '@/authAPI.js';
import User from '@/classes/marketplace/user.js';
import router from '@/router';

const fieldsNames = {
  firstNM: "",
  secondNM: "",
  userRole: "",
  userType: "",
  email: "",
  directorNM: "",
  country: "",
  companySite: "",
  mainCity: "",
  phone: "",
  companyName: "",
  inn: "",
  kpp: "",
  ogrn: "",
  legalAddress: "",
  fullDescription: ""
};

const userModule = {
  namespaced: true,
  state: {
    user: null,
    accessToken: null,
  },
  mutations: {
    setUser(state, userData) {
      if (userData) {
        const user = new User(userData);
        state.user = user;
      }
    },
    clearUser(state) {
      state.user = null;
      state.accessToken = null;
    },
    setAccessToken(state, accessToken) {
      state.accessToken = accessToken;
      if (state.user) {
        state.user.setAccessToken(accessToken);
      }
    },
    clearAccessToken(state) {
      state.accessToken = null;
      if (state.user) {
        state.user.clearAccessToken();
      }
    },
    setProfileType(state, profileType) {
      if (state.user) {
        state.user.setProfileType(profileType);
      }
    },
    setSettings(state, settings) {
      if (state.user) {
        state.user.setSettings(settings);
      }
    },
    updateUser(state, updatedData) {
      if (state.user) {
        for (const key in updatedData) {
          if (
            Object.prototype.hasOwnProperty.call(updatedData, key) &&
            updatedData[key] !== 0
          ) {
            state.user[key] = updatedData[key];
          }
        }
      }
    },
  },
  actions: {
    async login({ commit }, { username, password }) {
      try {
        if (!username.trim().length || !password.trim().length) {
          return { success: false, message: 'Поля не могут быть пустыми' };
        }

        const formData = new FormData();
        formData.append('user', username);
        formData.append('pass', password);

        const response = await api.post('/user/form/', formData, {
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
          }
        });

        if (response.data.result === true) {
          const accessToken = response.data.token;

          const secondFormData = new FormData();
          secondFormData.append('userLogin', response.data.name);
          secondFormData.append('token', accessToken);
          secondFormData.append('classToEdit', "UserSuperGet");
          secondFormData.append('fieldsNames', JSON.stringify(fieldsNames));

          const secondResponse = await api.post('/get/', secondFormData);

          const userData = {
            username: response.data.name,
            ...secondResponse.data.fieldsNames
          };
          
          commit('setUser', userData);
          commit('setAccessToken', accessToken);
          return { success: true, message: 'Успешный вход' };
        } else {
          return { success: false, message: 'Неверный логин или пароль' };
        }
      } catch (error) {
        console.error(error);
        return { success: false, message: 'Ошибка при входе' };
      }
    },
    async registration({ commit, dispatch }, { username, password, repeat_password, company_name }) {
      try {
        if (password !== repeat_password) {
          return { success: false, message: 'Пароли не совпадают' };
        }

        const formData = new FormData();
        formData.append('log', username);
        formData.append('pass', password);
        formData.append('role', 'user');

        const fieldsNames = {
          companyName: company_name
        };
        formData.append('fieldsNames', JSON.stringify(fieldsNames));
        
        const response = await api.post('/user/register/', formData, {
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
          }
        });

        if (response.status === 200 && response.data.result !== "Error") {
          const loginSuccess = await dispatch('login', { username, password });
          if (loginSuccess.success) {
            return { success: true, message: 'Вы успешно зарегистрировались' };
          } else {
            console.error('Ошибка при входе после регистрации');
            return { success: false, message: 'Ошибка при входе после регистрации' };
          }
        } else {
          console.error('Ошибка при регистрации:', response.data.error);
          return { success: false, message: response.data.type };
        }
      } catch (error) {
        console.error(error);
        return { success: false, message: 'Пользователь уже существует' };
      }
    },
    logout({ commit }) {
      commit('clearUser');
      commit('clearAccessToken');
      router.push('/');
    },
    updateProfileType({ commit }, profileType) {
      commit('setProfileType', profileType);
    },
    updateSettings({ commit }, settings) {
      commit('setSettings', settings);
    },
    async fetchUserData({ commit, state }, userId) {
      try {
        const formData = new FormData();
        formData.append('action', 'GetUser');
        formData.append('login', userId);

        const response = await api.post('/user/get/', formData);

        const userData = Object.keys(fieldsNames).reduce((acc, key) => {
          if (response.data.user[key] !== 0) {
            acc[key] = response.data.user[key];
          }
          return acc;
        }, { username: userId });

        const updatedUserData = { ...state.user, ...userData };
        commit('updateUser', updatedUserData);
        return updatedUserData;
      } catch (error) {
        console.error('Error fetching user data:', error);
        throw error;
      }
    },
    async updateUser({ commit, state }, { username, updatedData }) {
      try {
        const currentUserData = state.user;

        const mergedData = { ...currentUserData, ...updatedData };

        const fieldsToUpdate = {};
        for (const key in fieldsNames) {
          if (
            mergedData.hasOwnProperty(key) &&
            mergedData[key] !== 0
          ) {
            fieldsToUpdate[key] = mergedData[key];
          }
        }

        const updateFormData = new FormData();
        updateFormData.append('userLogin', username);
        updateFormData.append('classToEdit', 'UserSuperSet');
        updateFormData.append('fieldsNames', JSON.stringify(fieldsToUpdate));

        const updateResponse = await api.post('/set/', updateFormData);
        if (updateResponse.status === 200 && updateResponse.data.result === true) {
          commit('updateUser', fieldsToUpdate);
          return { success: true, message: 'Профиль успешно обновлен' };
        } else {
          return { success: false, message: 'Ошибка при обновлении профиля' };
        }
      } catch (error) {
        console.error('Error updating user data:', error);
        return { success: false, message: 'Ошибка при обновлении профиля' };
      }
    }
  },
  getters: {
    currentUser(state) {
      return state.user;
    },
    hasRole(state) {
      return state.user ? state.user.role : null;
    },
    isAuthenticated(state) {
      return state.user !== null && state.accessToken !== null;
    },
  },
};

export default userModule;
