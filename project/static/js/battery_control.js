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
        if(voltageTag) {
            voltageTag.innerHTML = msg.data.voltage.toFixed(2) + 'V';
        }

        var percentTag = document.querySelector('#battery span.fa-layers-text');
        percentTag.innerHTML = Math.round(battery_percent) + '%';
    }

    getBatteryPercent(voltage) {
        var max_voltage = this.max_voltage * this.battery_cnt;
        var min_voltage = this.min_voltage * this.battery_cnt;
        var one_perc = (max_voltage - min_voltage) / 100;
        var diff = voltage - min_voltage;

        return diff / one_perc;
    }

    updateBatteryIcon(percent) {
        var batteryTag = document.querySelector('#battery svg');

        if(percent >= 80) {
            var icon = 'battery-full';
        } else if(percent >= 60 && percent < 80) {
            var icon = 'battery-three-quarters';
        } else if(percent >= 35 && percent < 60) {
            var icon = 'battery-half';
        } else if(percent >= 10 && percent < 35) {
            var icon = 'battery-quarter';
        } else {
            var icon = 'battery-empty';
            batteryTag.style.color = 'red';
        }

        // console.log(batteryTag);

        if(this.batteryIcon != icon && batteryTag) {
            this.batteryIcon = icon;
            // batteryTag.className = this.batteryIcon;
            batteryTag.setAttribute('data-icon', icon);
        }
    }

    requestData() {
        this.socket.emit('battery', {});
    }
}
