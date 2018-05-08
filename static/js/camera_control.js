class CameraControl {
    constructor(socket) {
        this.socket = socket
        
        this.initEvents();
    }

    initEvents() {
        $('#btn-take-photo').on('click', function() {
            console.log('take photo');
        });
    }
}