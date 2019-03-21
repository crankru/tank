class CameraControl 
{
    constructor(socket) {
        this.socket = socket;
        this.cameraOn = false;
        
        this.bindEvents();
        this.listenEvents();

        this.activeBtn = $('#btn-camera-stop');
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
            console.log('camera: ', msg);

            if(msg.status) {
                $this.setCameraStatus(msg.status);
            }
        });
    }

    setCameraStatus(on) {
        if(on == true) {
            console.log('camera on');
            this.cameraOn = true;
            this.activeBtn.text('<i class="fas fa-video"></i>');
        } else {
            console.log('camera off');
            this.cameraOn = false;
            this.activeBtn.html('<i class="fas fa-video-slash"></i>');
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
        this.socket.emit('camera', {'action': 'take_photo'});
    }
}