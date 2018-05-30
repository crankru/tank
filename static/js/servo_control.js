class ServoControl 
{
    constructor(socket) {
        this.socket = socket;
        this.x = this.centerX = 400;
        this.y = this.centerY = 500;

        //  = '#servoSliderY';
        //  = '#servoSliderX';

        this.sliderY = $('#servo_y').slider({
            formatter: function(value) { return value }
        });

        this.sliderX = $('#servo_x').slider({
            reversed : true,
            formatter: function(value) { return value }
        });

        this.bindEvents();
        this.listenEvents();
    }

    bindEvents() {
        var $this = this;
        $('#btn-camera-center').on('click', function() {
            $this.center();
        });

        this.sliderX.on('slide', function(evt) {
            var x = evt.value;
            if($this.x != x) {
                $this.x = x;
                var data = {action: 'move', x: $this.x, y: $this.y};
                $this.socket.emit('servo', data);
            }
        });

        this.sliderY.on('slide', function(evt) {
            var y = evt.value;
            if($this.y != y) {
                $this.y = y;
                var data = {action: 'move', x: $this.x, y: $this.y};
                $this.socket.emit('servo', data);
            }
            // console.log(evt.value);
        });
    }

    listenEvents() {
        this.socket.on('servo', function(msg) {
            // console.log(msg);
        });
    }

    // move(nipple) {
    //     var x = Math.round(nipple.instance.frontPosition.x);
    //     var y = Math.round(nipple.instance.frontPosition.y * -1);
    //     // console.log('move', nipple);

    //     if(x != this.x || y != this.y) {
    //         this.x = x;
    //         this.y = y;
    //         var data = {action: 'move', x: x, y: y};
    //         console.log(data);
    //         this.socket.emit('servo', data);
    //     }
    // }

    stop() {
        console.log('stop');
        this.socket.emit('servo', {action: 'stop'});
    }

    center() {
        console.log('center camera');
        this.socket.emit('servo', {action: 'center'});
        // console.log(this.centerX, this.centerY);
        this.sliderX.slider('setValue', this.centerX);
        this.sliderY.slider('setValue', this.centerY);
    }
}