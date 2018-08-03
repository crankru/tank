class TemperatureControl
{
    constructor(socket) {
        // this.socket = socket;
        this.min_temp = 40;
        this.max_temp = 80;
        this.icons = [
            'thermometer-full',
            'thermometer-three-quarters',
            'thermometer-half',
            'thermometer-quarter',
            'thermometer-empty', 
        ];
        this.icon = null;
        var $this = this;

        socket.on('temperature', function(msg) {
            $this.updateTempIcon(msg.temperature);
        });
    
        setInterval(function() {
            socket.emit('temperature', {});
        }, 5000);
    }

    updateTempIcon(temperature) {
        // console.log(temperature);
        var k = (this.max_temp - this.min_temp) / 5;
        var diff = this.max_temp - temperature;
        var tempIcon = document.querySelector('#temperature svg');
        var tempText = document.querySelector('#temperature span');
        tempText.innerHTML = temperature + 'C';
        var index = Math.floor(diff / k);
        if(this.icons[index]) {
            tempIcon.setAttribute('data-icon', this.icons[index]);
            if(index < 1) {
                tempIcon.style.color = 'red';
            } else if(index <= 2) {
                tempIcon.style.color = 'orange';
            } else {
                tempIcon.style.color = 'black';
            }
        }
    }
}