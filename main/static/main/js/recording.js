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
function recording() {
     recognizer.start();
}
function stoprecording() {
    recognizer.stop();
    document.getElementById("div1").textContent = text;
}
