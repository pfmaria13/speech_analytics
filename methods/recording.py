import contextlib
import eel as eel
import librosa
import pyaudio
import wave
import speech_recognition as speech_r
import keyboard



@eel.expose
def record():
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    RECORD_SECONDS = 180
    WAVE_OUTPUT_FILENAME = "output.wav"

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
    print("* recording")

    frames = []
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
        if keyboard.is_pressed('Space'):
            break

    print("* done recording")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()


def speech_recognition():
    sample_audio = speech_r.AudioFile('output.wav')
    r = speech_r.Recognizer()
    with sample_audio as audio_file:
        r.adjust_for_ambient_noise(audio_file)
        audio_content = r.record(audio_file)
    try:
        text = r.recognize_google(audio_content, language="ru-RU")
    except speech_r.UnknownValueError:
        text = ''
    return text


def temp(text):
    with contextlib.closing(wave.open('output.wav', 'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        duration = frames / float(rate)
    words = len(text.split())
    koef = words / duration
    if 2 < koef < 3:
        return 'Темп речи нормальный'
    if koef > 3:
        return 'Темп речи слишком быстрый'
    return 'Темп речи слишком медленный'


unnecessary_words = [
    'как бы', 'собственно говоря', 'таким образом', 'буквально', 'прямо', 'как говорится', 'так далее', 'скажем', 'ведь',
    'как его', 'в натуре', 'так вот', 'короче', 'как сказать', 'видишь', 'слышишь', 'типа', 'на самом деле', 'вообще',
    'в общем-то', 'в общем', 'в некотором роде', 'на фиг', 'на хрен', 'в принципе', 'итак', 'типа того', 'только', 'вот',
    'в самом деле', 'всё такое', 'в целом', 'то есть', 'это', 'это самое', 'ешкин кот', 'ну', 'ну вот', 'ну это', 'прикинь',
    'прикол', 'значит', 'знаешь', 'так сказать', 'понимаешь', 'допустим', 'слушай', 'например', 'просто', 'конкретно',
    'да ладно', 'блин', 'походу', 'а-а-а', 'э-э-э', 'не вопрос', 'без проблем', 'практически', 'фактически', 'как-то так',
    'ничего себе', 'достаточно', 'а-а', 'э-э'
]


def word_analysis(text):
    list = []
    for word in unnecessary_words:
        if word.lower() in text.lower():
            list.append(word)
    return list


def play():
    CHUNK = 1024
    wf = wave.open("output.wav", 'rb')
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)
    data = wf.readframes(CHUNK)
    while data != '':
        stream.write(data)
        data = wf.readframes(CHUNK)
    stream.stop_stream()
    stream.close()
    p.terminate()


def frequency():
    wav_obj = wave.open('output.wav', 'rb')
    sample_freq = wav_obj.getframerate()
    n_samples = wav_obj.getnframes()
    t_audio = n_samples / sample_freq
    signal_wave = wav_obj.readframes(n_samples)
    import numpy as np
    signal_array = np.frombuffer(signal_wave, dtype=np.int16)
    l_channel = signal_array[0::2]
    times = np.linspace(0, n_samples / sample_freq, num=n_samples)
    import matplotlib.pyplot as plt
    plt.figure(figsize=(15, 5))
    plt.plot(times, l_channel)
    plt.title('Left Channel')
    plt.ylabel('Signal Value')
    plt.xlabel('Time (s)')
    plt.xlim(0, t_audio)
    plt.show()


record()
text = speech_recognition()
print(text)
print(temp(text))
print('Слова паразиты: ', word_analysis(text))
frequency()
