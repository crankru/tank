class BatteryControl
{
    constructor(socket, battery_cnt) {
        this.socket = socket;

        this.battery_cnt = battery_cnt;
        this.min_voltage = 3.1;
        this.max_voltage = 4.2;
        this.batteryIcon = null;

        this.listenEvents();
        this.requestData();

        var $this = this;

        setInterval(function() {
            $this.requestData();
        }, 1000);
    }

    listenEvents() {
        var $this = this;

        this.socket.on('battery', function(msg) {
            $this.updateData(msg);
            // console.log(msg.data);
        });
    }

    updateData(msg) {
        var battery_percent = this.getBatteryPercent(msg.data.voltage);
        this.updateBatteryIcon(battery_percent);
        var voltageTag = document.querySelector('#battery span.voltage');
        voltageTag.innerHTML = msg.data.voltage + 'V';
    }

    getBatteryPercent(voltage) {
        var max_voltage = this.max_voltage * this.battery_cnt;
        var min_voltage = this.min_voltage * this.battery_cnt;
        var one_perc = (max_voltage - min_voltage) / 100;
        var diff = voltage - min_voltage;

        return diff / one_perc;
    }

    updateBatteryIcon(percent) {
        var b_100 = 'fas fa-battery-full';
        var b_75 = 'fas fa-battery-three-quarters';
        var b_50 = 'fas fa-battery-half';
        var b_25 = 'fas fa-battery-quarter';
        var b_0 = 'fas fa-battery-empty';

        if(percent >= 80) {
            var icon = b_100;
        } else if(percent >= 60 && percent < 80) {
            var icon = b_75;
        } else if(percent >= 35 && percent < 60) {
            var icon = b_50;
        } else if(percent >= 10 && percent < 35) {
            var icon = b_25;
        } else {
            var icon = b_0;
        }

        if(this.batteryIcon != icon) {
            this.batteryIcon = icon;
            var batteryTag = document.querySelector('#battery i');
            batteryTag.className = this.batteryIcon;
        }
    }

    requestData() {
        this.socket.emit('battery', {});
    }
}
