class CameraControl {
    constructor(socket) {
        this.socket = socket;
        this.cameraOn = false;
        
        this.bindEvents();
        this.listenEvents();
    }

    bindEvents() {
        var $this = this;
        $('#btn-camera-photo').on('click', function() {
            $this.takePhoto();
        });

        $('#btn-camera-stop').on('click', function() {
            $this.cameraOnOff();
        });
    }

    listenEvents() {
        var $this = this;
        this.socket.on('camera', function(msg) {
            if(msg.cameraOn == true) {
                $this.setCameraStatus(true);
            } else {
                $this.setCameraStatus(false);
            }
        });
    }

    setCameraStatus(on) {
        if(on == true) {
            console.log('camera on');
            this.cameraOn = true;
        } else {
            console.log('camera off');
            this.cameraOn = false;
        }
    }

    cameraOnOff() {
        if(this.cameraOn) {
            console.log('stop video');
        } else {
            console.log('start video');
        }
        
        this.socket.emit('camera', {'active': ! this.cameraOn});
    }

    takePhoto() {
        console.log('take photo');
    }
}