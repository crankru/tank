var Header = {
    template: '<div class="row"> \
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
    template: '<img src="" class="img-fluid">',
}

var SliderX = {
    template: '',
}

var SliderY = {
    template: '<input id="servo_y" data-slider-id="servoSliderY" type="text" :data-slider-min="servo.yMin" :data-slider-max="servo.yMax" data-slider-step="1" data-slider-value="500" data-slider-orientation="vertical" />',
    data() {
        return {
            servo: {
                yMin: 100,
                yMax: 200,
            }
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
    components: { Header, Video, SliderY },
}

new Vue({
    el: '#app',
    components: { App },
    template: '<App />',
});