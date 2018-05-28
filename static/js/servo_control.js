class ServoControl 
{
    constructor(socket) {
        this.socket = socket;
        this.x = 0;
        this.y = 0;

        this.bindEvents();
        this.listenEvents();
    }

    bindEvents() {

    }

    listenEvents() {
        this.socket.on('servo', function(msg) {
            console.log(msg);
        });
    }

    move(nipple) {
        var x = Math.round(nipple.instance.frontPosition.x);
        var y = Math.round(nipple.instance.frontPosition.y * -1);
        // console.log('move', nipple);

        if(x != this.x || y != this.y) {
            this.x = x;
            this.y = y;
            var data = {action: 'move', x: x, y: y};
            console.log(data);
            this.socket.emit('servo', data);
        }
    }

    stop() {
        console.log('stop');
        this.socket.emit('servo', {action: 'stop'});
    }
}