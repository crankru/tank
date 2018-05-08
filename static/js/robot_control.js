class RobotControl {
    constructor(socket) {
        this.repeatTimeout = 300;
        this.x = 0;
        this.y = 0;
        this.dataSend = false;
        
        this.socket = socket;
    }

    sendXY() {
        var data = {
            x: this.x,
            y: this.y,
            action: 'move',
        }
        // $.getJSON('/action', data, function(res) {
        //     console.log(res);
        // });

        // this.socket.emit('action', data);
    }

    resetDataFlag() {
        if(this.dataSend == false) {
            return;
        } else {
            this.dataSend = false;
            this.sendXY();
        }
        // console.log('reset dataSend', this.dataSend);
    }

    move(nipple) {
        var x = Math.round(nipple.instance.frontPosition.x);
        var y = Math.round(nipple.instance.frontPosition.y * -1);

        // console.log();

        if(x == this.x && y == this.y) {
            return;
        } else {
            // console.log(x, y);
            this.x = x;
            this.y = y;
        }

        var data = {
            x: this.x,
            y: this.y,
            action: 'move',
        }

        // TODO set update delay
        this.socket.emit('action', data);

        // console.log(this.x, this.y);

        // if(this.dataSend == true) {
        //     var $this = this;
            
        //     // setTimeout(function() {
        //     //    $this.resetDataFlag();
        //     // }, this.repeatTimeout);

        //     return;
        // }

        // this.sendXY();
        // this.dataSend = true;
    }

    stop() {
        // $.getJSON('/action', {action: 'stop'}, function(res) {
        //     console.log('STOP');
        // });
        this.socket.emit('action', {action: 'stop'})
    }
}