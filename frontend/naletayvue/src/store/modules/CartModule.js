const cartModule = {
    namespaced: true,
    state: {
        items: [],
        files: [] 
    },
    mutations: {
        setCartItems(state, items) {
            state.items = items;
        },
        setFiles(state, files) {
            state.files = files;
        }
    },
    getters: {
        cartItemsTotal(state) {
            return state.items.length;
        },
        cartItems(state) {
            return state.items;
        },
        cartTotal(state) {
            return state.items.reduce((total, item) => total + item.price * item.quantity, 0);
        }
    },
    actions: {
        setCartItems({ commit }, items) {
            commit('setCartItems', items);
        },
        setFiles({ commit }, files) {
            commit('setFiles', files);
        }
    }
};

export default cartModule;
