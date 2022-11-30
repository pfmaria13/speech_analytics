////    recording = eel.recording()
function recording(ev) {
    if(ev.getAttribute('data-show') === "true") {
        ev.innerText = "Закончить запись";
        ev.setAttribute('data-show', "false");
        let test = eel.test()
        document.getElementById("min").innerHTML = test;
        self.location.href='tips'
        let recording = eel.record();

        let text = speech_recognition(recording)

        let temp = temp(text, recording);

        let words = word_analysis(text);
        document.getElementById("min").innerHTML = words;

        self.location.href='tips'

    }
    else {
        ev.innerText = "Начать запись"
        ev.setAttribute('data-show', "true");
        self.location.href='tips'

    }

}

