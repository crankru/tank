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
    template: '<div style="min-height: 200px;"> \
    <img src="http://192.168.1.123:5500/video_feed" class="img-fluid"> \
    <!--<video id="videoPlayer" controls> \
        <source src="http://192.168.1.123:5500" type="video/mp4"> \
    </video>--> \
    </div>',
}

var SliderX = {
    template: '<div> \
        <vue-slider v-model="value" v-bind="options" v-on:change="change"></vue-slider> \
    </div>',

    data() {
        return {
            value: 330,
            options: {
                min: 180,
                max: 500,
                tooltip: 'always',
                direction: 'rtl',
                marks: [180, 500],
            }
        }
    },

    components: {
        'vueSlider': window[ 'vue-slider-component' ],
    },

    methods: {
        change: function(value) {
            this.$store.commit('setServoX', value);
            this.$store.dispatch('SERVO_MOVE');
        }
    }
}

var SliderY = {
    template: '<div> \
        <vue-slider v-model="value" v-bind="options" v-on:change="change"></vue-slider> \
    </div>',

    data() {
        return {
            value: 400,
            options: {
                min: 300,
                max: 550,
                tooltip: 'always',
                height: 200,
                width: 4,
                direction: 'btt',
                marks: [300, 550],
            }
        }
    },

    components: {
        'vueSlider': window[ 'vue-slider-component' ],
    },

    methods: {
        change: function(value) {
            this.$store.commit('setServoY', value);
            this.$store.dispatch('SERVO_MOVE');
        }
    }
}

var ButtonsBar = {
    template: '<div class="col-sm text-center"> \
        <button id="btn-move-stop" type="button" class="btn btn-danger" title="Stop moving"> \
            <i class="fas fa-stop-circle"></i> \
        </button> \
        <button id="btn-camera-stop" type="button" class="btn btn-primary" title="Camera on/off"> \
            <i class="fas fa-video"></i> \
        </button> \
        <button id="btn-camera-photo" type="button" class="btn btn-primary" title="Take photo"> \
            <i class="fas fa-camera"></i> \
        </button> \
        <button id="btn-camera-center" type="button" class="btn btn-primary" title="Camera to center"> \
            <i class="fas fa-angle-down"></i> \
        </button> \
        <button id="btn-servo-stop" type="button" class="btn btn-danger" title="Stop servo"> \
            <i class="fas fa-stop-circle"></i> \
        </button> \
    </div>',
}

var App = {
    template: '<div class="container"> \
        <Header /> \
        <div id="j_zone1" class="j_zone1 row text-center p-3"> \
            <div class="col-1 text-left"> \
                <SliderY /> \
            </div> \
            <div class="col-11"> \
                <Video /> \
                <SliderX /> \
            </div> \
        </div> \
        <div class="row mb-3"><ButtonsBar /></div> \
        <div class="row"> \
                <div class="col-sm"> \
                    <div id="j_zone2" class="j_zone2"> \
                        <div id="div-xy" class="small"></div> \
                        <h1>Move control</h1> \
                    </div> \
                </div> \
            </div> \
    </div>',
    components: { Header, Video, SliderY, SliderX, ButtonsBar },
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