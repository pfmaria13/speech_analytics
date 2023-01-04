function start() {
    self.location.href='withoutstart'
    document.getElementById("div1").textContent = 'dfvverve';
}

var recognizer = new webkitSpeechRecognition();
recognizer.interimResults = true;
recognizer.lang = 'ru-Ru';
text = ''
recognizer.onresult = function (event) {
    var result = event.results[event.resultIndex];
    if (result.isFinal) {
        text = text +  result[0].transcript;
    }
};

navigator.mediaDevices.getUserMedia({ audio: true})
       .then(stream => {
      const mediaRecorder = new MediaRecorder(stream);

      document.querySelector('#start').addEventListener('click', function(){
        recognizer.start();
      	mediaRecorder.start();
//      	document.getElementById("start").textContent = 'Запись пошла';
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

        document.querySelector('#audio').appendChild(audio);
        audioChunks = [];
    });
    document.querySelector('#stop').addEventListener('click', function(){
      	 mediaRecorder.stop();
      	 recognizer.stop();
      	 document.getElementById("div1").textContent = text;
      });
});



let fd = new FormData();
fd.append('voice', audioBlob);
let promise = await fetch(URL, {
    method: 'POST',
    body: form});

function stop() {
    self.location.href='withoutstop'
}
