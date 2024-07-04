import axios from 'axios';
import store from '@/store';

const backendURL = import.meta.env.VITE_BACKEND_URL ? import.meta.env.VITE_BACKEND_URL : 'http://127.0.0.1:8000';

const api = axios.create({
    baseURL: backendURL,
});

api.interceptors.request.use(config => {
    const currentUser = store.getters['user/currentUser'];
    if (currentUser && currentUser.accessToken) {
        if (config.data instanceof FormData) {
            if (!config.data.has('token')) {
                config.data.append('token', currentUser.accessToken);
            }
        } else {
            if (!config.data) {
                config.data = {};
            }
            if (!config.data.token) {
                config.data.token = currentUser.accessToken;
            }
        }
    }
    return config;
}, error => {
    return Promise.reject(error);
});

api.getBackendURL = function() {
    return backendURL;
};

export default api;
