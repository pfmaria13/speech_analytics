navigator.mediaDevices.getUserMedia({ audio: true})
    .then(stream => {
        const mediaRecorder = new MediaRecorder(stream);
        let voice = [];
        document.querySelector('#start').addEventListener('click', function(){
            mediaRecorder.start();
        });

        mediaRecorder.addEventListener("dataavailable",function(event) {
            voice.push(event.data);
        });

        document.querySelector('#stop').addEventListener('click', function(){
            mediaRecorder.stop();
        });
    });
mediaRecorder.addEventListener("stop", function() {
    const voiceBlob = new Blob(voice, {
        type: 'audio/wav'
    });