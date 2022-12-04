navigator.mediaDevices.getUserMedia({ audio: true})
       .then(stream => {
      const mediaRecorder = new MediaRecorder(stream);
    
      document.querySelector('#start').addEventListener('click', function(){
      	mediaRecorder.start();

      });
    var audioChunks = [];
    mediaRecorder.addEventListener("dataavailable",function(event) {
        audioChunks.push(event.data);
    });

    mediaRecorder.addEventListener("stop", function() {
        const audioBlob = new Blob(audioChunks, {
            type: 'audio/wav'
        });
    const audioUrl = URL.createObjectURL(audioBlob);
      var audio = document.createElement('audio');
      //audio.src = audioUrl;
      //audio.controls = true;
      //audio.autoplay = true;
    document.querySelector('#audio').appendChild(audio);
       audioChunks = [];
});
    document.querySelector('#stop').addEventListener('click', function(){
      	 mediaRecorder.stop();
      	 document.getElementById("div1").textContent = test()
      });
});

async function analytics(){
    let text = await eel.speech_recognition(audioBlob)();
    return text;
}


async function test() {
    let val = 'testing'
    await eel.test(val)();
}