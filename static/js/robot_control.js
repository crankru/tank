class RobotControl 
{
    constructor(socket) {
        this.socket = socket;

        this.repeatTimeout = 300;
        this.x = 0;
        this.y = 0;
        this.speed = 0;
        this.angle = 0;
        this.dataSend = false;
        this.direction = {};

        this.bindEvents();
        this.listenEvents();
    }

    bindEvents() {
        var $this = this;

        $('#btn-move-stop').on('click', function() {
            $this.stop();
        });
    }

    listenEvents() {
        this.socket.on('move', function(msg) {
            // console.log(msg);
            if(msg.params) {
                document.getElementById('div-xy').innerHTML = 'X: ' + msg.params.x + ' Y: ' + msg.params.y;
            }
        });
    }

    sendXY() {
        var data = {
            x: this.x,
            y: this.y,
            speed: this.speed,
            angle: this.angle,
            direction: this.direction,
            action: 'move',
        }

        // console.log(data);

        // TODO set update delay
        // if(this.dataSend == true) {
        //     var $this = this;
            
        //     setTimeout(function() {
        //        $this.resetDataFlag();
        //     }, this.repeatTimeout);

        //     return;
        // }

        this.socket.emit('move', data);
        this.dataSend = true;
    }

    resetDataFlag() {
        if(this.dataSend == true) {
            this.dataSend = false;
            this.sendXY();
        }
        // console.log('reset dataSend', this.dataSend);
    }

    move(nipple) {
        var x = Math.round(nipple.instance.frontPosition.x);
        var y = Math.round(nipple.instance.frontPosition.y * -1);

        // console.log(nipple);
        // console.log(nipple.angle, Math.sin(nipple.angle.radian), Math.cos(nipple.angle.radian));

        if(x == this.x && y == this.y) {
            return;
        } else {
            // console.log(x, y);
            this.x = x;
            this.y = y;
            this.speed = nipple.distance;
            this.angle = nipple.angle.radian;
            this.direction = nipple.direction;
        }

        this.sendXY();
    }

    stop() {
        // $.getJSON('/action', {action: 'stop'}, function(res) {});
        this.socket.emit('move', {action: 'stop'});
        // console.log('STOP');
    }
}