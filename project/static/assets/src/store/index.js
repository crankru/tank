const store = new Vuex.Store({
    state: {
        socket: null,
    },

    getters: {
        getSocket(state) {
            return state.socket;
        }
    },

    mutations: {
        setSocket(state, socket) {
            state.socket = socket;
        }
    },

    actions: {
        SET_SOCKET(context, socket) {
            context.commit('setSocket', socket);
        }
    }
});