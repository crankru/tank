const store = new Vuex.Store({
    state: {
        online: false,
        socket: null,
        servo: {
            x: 0, 
            y: 400,
        }
    },

    getters: {
        getOnline(state) {
            return  state.online;
        },

        getSocket(state) {
            return state.socket;
        },

        getServo(state) {
            return state.servo;
        },
    },

    mutations: {
        setOnline(state, online) {
            state.online = online;
        },

        setSocket(state, socket) {
            state.socket = socket;
        },

        setServoX(state, x) {
            state.servo.x = x;
        },

        setServoY(state, y) {
            state.servo.y = y;
        },
    },

    actions: {
        UPDATE_ONLINE(state) {
            var socket = state.getters.getSocket;
            socket.emit('online');
        },

        SET_SOCKET(context, socket) {
            context.commit('setSocket', socket);
        },

        SERVO_MOVE(state) {
            var socket = state.getters.getSocket;
            var servo = state.getters.getServo;
            if(socket) {
                var data = {action: 'move', x: servo.x, y: servo.y}
                socket.emit('servo', data);
            } else {
                console.log('Socket undefined');
            }
        },
    }
});