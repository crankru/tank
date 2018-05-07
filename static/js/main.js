$(function() {

    var socket = io.connect('http://' + document.domain + ':' + location.port + '/socket');
    socket.on('my response', function(msg) {
        console.log(msg.data);
    });

    // var options1 = {
    //     zone: document.getElementById('zone1'),
    //     color: '#000',
    //     mode: 'dynamic',
    // };

    var options2 = {
        zone: document.getElementById('zone2'),
        color: '#000',
        // mode: 'dynamic',
        mode: 'static',
        position: {left: '50%', top: '50%'}
    };

    // var manager1 = nipplejs.create(options1);
    var manager2 = nipplejs.create(options2);
    var rc = new RobotControl(socket);

    manager2.on('move', function(evt, nipple) {
        // console.log(nipple);
        // console.log(nipple.position);
        rc.move(nipple);
    });

    manager2.on('end', function(evt, nipple) {
        rc.stop();
    });
});

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
        // var x = Math.round(nipple.distance * Math.cos(nipple.angle.degree));
        // var y = Math.round(nipple.distance * Math.sin(nipple.angle.degree));
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