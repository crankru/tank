class ServoControl 
{
    constructor(socket) {
        this.socket = socket;
        this.x = this.centerX = 400;
        this.y = this.centerY = 500;

        //  = '#servoSliderY';
        //  = '#servoSliderX';

        this.sliderY = $('#servo_y').slider({
            tooltip: 'show',
            formatter: function(value) { return value }
        });

        this.sliderX = $('#servo_x').slider({
            reversed : true,
            tooltip: 'show',
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

        // slider moving events
        this.sliderX.on('slide', function(e) {
            if($this.x != e.value) {
                $this.x = e.value;
                $this.move();
            }
        });

        this.sliderY.on('slide', function(e) {
            if($this.y != e.value) {
                $this.y = e.value;
                $this.move();
            }
        });

        // slider change by click events
        this.sliderX.on('change', function(e) {
            if($this.x != e.value.newValue) {
                $this.x = e.value.newValue;
                $this.move();
            }
        });

        this.sliderY.on('change', function(e) {
            if($this.y != e.value.newValue) {
                $this.y = e.value.newValue;
                $this.move();
            }
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
        // console.log('center camera');
        // console.log(this.centerX, this.centerY);
        this.socket.emit('servo', {action: 'center'});
        this.sliderX.slider('setValue', this.centerX);
        this.sliderY.slider('setValue', this.centerY);
    }

    move() {
        var data = {action: 'move', x: this.x, y: this.y};
        this.socket.emit('servo', data);
    }
}