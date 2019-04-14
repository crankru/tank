var Header = {
    template: '<div class="row bg-secondary p-2"> \
            <div id="temperature" class="col-6"> \
                <i class="fas fa-thermometer-empty fa-2x"></i> \
                <span></span> \
            </div> \
            <div id="battery" class="text-right col-6"> \
                <span class="voltage"></span> \
                <span class="fa-layers fa-fw fa-2x"> \
                    <i class="fas fa-battery-full"></i> \
                    <span class="fa-layers-text fa-inverse" data-fa-transform="shrink-12" style="font-weight:900"></span> \
                </span> \
            </div> \
        </div>'
}

var Video = {
    template: '<div> \
    <img src="/video_feed" class="img-fluid"> \
    <!--<video id="videoPlayer" controls> \
        <source src="http://192.168.1.10:5500" type="video/mp4"> \
    </video>--> \
    </div>',
}

var SliderX = {
    template: '<div></div>',
}

var SliderY = {
    template: '<div> \
        <input type="integer" v-model="value" v-on:change="changeValue"> \
    </div>',

    data() {
        return {
            socket: null,
            value: 50,
        }
    },

    components: {
        // 'vueSlider': window[ 'vue-slider-component' ],
    },

    created() {
        this.socket = this.$store.getters.getSocket;
    },

    methods: {
        changeValue: function() {
            console.log('Y', this.value);
            this.socket.emit('servo', {y: this.value});
        }
    }
}

var App = {
    template: '<div class="container"> \
        <Header /> \
        <div id="j_zone1" class="j_zone1 row text-center"> \
            <div class="col-1 text-left"> \
                <SliderY /> \
            </div> \
            <div class="col-11"> \
                <Video /> \
                <SliderX /> \
            </div> \
        </div> \
        <div class="row"> \
                <div class="col-sm"> \
                    <div id="j_zone2" class="j_zone2"> \
                        <div id="div-xy" class="small"></div> \
                        <h1>Move control</h1> \
                    </div> \
                </div> \
                <div class="col-sm text-center"> \
                    <button id="btn-move-stop" type="button" class="btn btn-danger" title="Stop moving"> \
                        <i class="fas fa-stop-circle"></i> \
                    </button><br> \
                    <button id="btn-camera-stop" type="button" class="btn btn-primary" title="Camera on/off"> \
                        <i class="fas fa-video"></i> \
                    </button> \
                    <button id="btn-camera-photo" type="button" class="btn btn-primary" title="Take photo"> \
                        <i class="fas fa-camera"></i> \
                    </button><br> \
                    <button id="btn-camera-center" type="button" class="btn btn-primary" title="Camera to center"> \
                        <i class="fas fa-angle-down"></i> \
                    </button> \
                    <button id="btn-servo-stop" type="button" class="btn btn-danger" title="Stop servo"> \
                        <i class="fas fa-stop-circle"></i> \
                    </button><br> \
                </div> \
            </div> \
    </div>',
    components: { Header, Video, SliderY, SliderX },
}

new Vue({
    el: '#app',
    store,
    components: { App },
    template: '<App />',

    created: function() {
        var socket = io.connect('http://' + document.domain + ':' + location.port + socketNamespace);
        this.$store.dispatch('SET_SOCKET', socket);
    }
});