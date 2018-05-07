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
        this.repeatTimeout = 300;
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
        console.log(data);

        $.get('/action', data, function(data) {
            // console.log(data);
        });
    }

    resetDataFlag() {
        this.dataSend = false;
        // this.sendXY();
        console.log('reset dataSend', this.dataSend);

        this.sendXY();
    }

    move(nipple) {
        // console.log(nipple.distance, nipple.angle.degree)
        var x = Math.round(nipple.distance * Math.cos(nipple.angle.degree));
        var y = Math.round(nipple.distance * Math.sin(nipple.angle.degree));

        if(x == this.x && y == this.y) {
            return;
        } else {
            this.x = x;
            this.y = y;
        }

        // console.log(this.x, this.y);

        if(this.dataSend == true) {
            var $this = this;
            
            setTimeout(function() {
                $this.resetDataFlag();
            }, this.repeatTimeout);

            return;
        }

        this.sendXY();
        this.dataSend = true;
    }

    stop() {
        $.getJSON('/action', {action: 'stop'}, function(res) {
            console.log('STOP');
        });
    }
}