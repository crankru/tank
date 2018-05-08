$(function() {

    var socket = io.connect('http://' + document.domain + ':' + location.port + '/robot');
    socket.on('connection', function(msg) {
        console.log(msg.data);
    });

    // var options1 = {
    //     zone: document.getElementById('zone1'),
    //     color: '#000',
    //     mode: 'dynamic',
    // };

    var options2 = {
        zone: document.getElementById('j_zone2'),
        // zode: document.querySelector('.j_zone2'),
        color: '#000',
        mode: 'dynamic',
        // mode: 'static',
        // position: {left: '50%', top: '50%'}
    };

    // var manager1 = nipplejs.create(options1);
    var manager2 = nipplejs.create(options2);

    var rc = new RobotControl(socket);
    var camera = new CameraControl(socket);

    manager2.on('move', function(evt, nipple) {
        // console.log(nipple);
        // console.log(nipple.position);
        rc.move(nipple);
    });

    manager2.on('end', function(evt, nipple) {
        rc.stop();
    });
});
