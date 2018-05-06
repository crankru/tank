$(document).ready(function() {
    var options = {
        zone: document.getElementById('zone_joystick'),
    };
    var manager = nipplejs.create(options);

    manager.on('move', function(evt, nipple) {
        $.getJSON('/action', function(res) {
            console.log(res);
        });
    });
});