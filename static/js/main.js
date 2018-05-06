$(document).ready(function() {
    var options = {
        zone: document.getElementById('zone_joystick'),
    };
    var manager = nipplejs.create(options);
    var rc = new RobotControl();

    manager.on('move', function(evt, nipple) {
        // console.log(nipple);
        // console.log(nipple.position);
        rc.move(nipple);
    });

    manager.on('end', function(evt, nipple) {
        rc.stop();
    });
});

class RobotControl {
    constructor() {
        this.x = 0;
        this.y = 0;
        this.dataSend = false;
    }

    sendXY() {
        var data = {
            x: this.x,
            y: this.y,
            action: 'move',
        }
        // $.getJSON('/action', nipple, function(res) {
        //     console.log(res);
        // });

        $.get('/action', data, function(data) {
            // console.log(data);
        });
    }

    resetDataFlag() {
        this.dataSend = false;
        this.sendXY();
    }

    move(nipple) {
        // console.log(nipple.distance, nipple.angle.degree)
        this.x = Math.round(nipple.distance * Math.cos(nipple.angle.degree));
        this.y = Math.round(nipple.distance * Math.sin(nipple.angle.degree));
        // console.log(this.x, this.y);

        if(this.dataSend) {
            return;
        }

        this.sendXY();

        this.dataSend = true;
        setTimeout(this.resetDataFlag, 300);
    }

    stop() {
        $.getJSON('/action', {action: 'stop'}, function(res) {
            console.log('STOP');
        });
    }
}