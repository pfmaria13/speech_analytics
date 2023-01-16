from django.shortcuts import render
import numpy as np
import contextlib
import pyaudio
import wave
import speech_recognition as speech_r


def ready(request):
    return render(request, 'audio/ready.html')


def mine(request):
    return render(request, 'audio/mine.html')


def without(request):
    return render(request, 'audio/without.html')


def advices(request):
    return render(request, 'audio/advices.html')


def start(request):
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    RECORD_SECONDS = 180
    swidth = 2
    window = np.blackman(CHUNK)
    global p
    p = pyaudio.PyAudio()
    global stream
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
    global frames
    frames = []
    global list_freq
    list_freq = []
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        if stream.is_stopped():
            continue
        data = stream.read(CHUNK)
        frames.append(data)
        indata = np.array(wave.struct.unpack("%dh" % (len(data) / swidth), data)) * window
        fftData = abs(np.fft.rfft(indata)) ** 2
        which = fftData[1:].argmax() + 1
        if which != len(fftData) - 1:
            y0, y1, y2 = np.log(fftData[which - 1:which + 2:])
            x1 = (y2 - y0) * .5 / (2 * y1 - y2 - y0)
            thefreq = (which + x1) * RATE / CHUNK
            list_freq.append(thefreq)
        else:
            thefreq = which * RATE / CHUNK
            list_freq.append(thefreq)
    stream.stop_stream()
    stream.close()
    p.terminate()
    wf = wave.open("output.wav", 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
    wf.setframerate(44100)
    wf.writeframes(b''.join(frames))
    wf.close()
    global audio
    audio = 'output.wav'
    global text
    text = speech_recognition(audio)
    a = word_analysis(text)
    global words
    words = a[0]
    global tip_words
    tip_words = a[1]
    global temp_analysis
    temp_analysis = temp(text, audio)
    global timing
    timing = time(audio)
    global frequency_value
    frequency_value = np.mean(list_freq)
    if (frequency_value > 500):
        tip_freq = 'Ваш голос слишком высокий'
    else:
        tip_freq = ''
    data = {'text': text, 'unnecessary_words': words,
            'temp': temp_analysis, 'time': timing, 'freq': frequency_value,
            'tip_words': tip_words, 'tip_freq': tip_freq}
    return render(request, 'audio/advices.html', data)


def stop(request):
    stream.stop_stream()
    stream.close()
    p.terminate()
    wf = wave.open("output.wav", 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
    wf.setframerate(44100)
    wf.writeframes(b''.join(frames))
    wf.close()
    global audio
    audio = 'output.wav'
    global text
    text = speech_recognition(audio)
    a = word_analysis(text)
    global words
    words = a[0]
    global tip_words
    tip_words = a[1]
    global temp_analysis
    temp_analysis = temp(text, audio)
    global timing
    timing = time(audio)
    global frequency_value
    frequency_value = np.mean(list_freq)
    if (frequency_value > 500):
        tip_freq = 'Ваш голос слишком высокий'
    else:
        tip_freq = ''
    data = {'text': text, 'unnecessary_words': words,
            'temp': temp_analysis, 'time': timing, 'freq': frequency_value,
            'tip_words': tip_words, 'tip_freq': tip_freq}
    return render(request, 'audio/advices.html', data)


def speech_recognition(record_file):
    global audio
    audio = record_file
    sample_audio = speech_r.AudioFile(audio)
    r = speech_r.Recognizer()
    with sample_audio as audio_file:
        r.adjust_for_ambient_noise(audio_file)
        audio_content = r.record(audio_file)
    try:
        text = r.recognize_google(audio_content, language="ru-RU")
    except speech_r.UnknownValueError:
        text = ''
    return text


def time(record_file):
    with contextlib.closing(wave.open(record_file, 'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        duration = frames / float(rate)
    duration = round(duration)
    return duration


def temp(text, record_file):
    with contextlib.closing(wave.open(record_file, 'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        duration = frames / float(rate)
    words = len(text.split())
    koef = words / duration
    if 1.2 < koef < 2:
        return 'Темп речи нормальный'
    if koef > 2:
        return 'Вы говорите слишком быстро! Как это исправить? Произносите каждое слово более четко. Не пропускайте ни одного слова, даже самого маленького. Произносите каждый слог каждого слова; Тренируйтесь произносить скороговорки. Скажите любую скороговорку. Произносите четко каждое слово. Повторяйте фразу снова и снова; Растягивайте гласные звуки. Сначала выделяйте слово, а потом добавляйте короткую паузу между каждым из них. Со временем вы научитесь не склеивать слова вместе и при этом будете четко их произносить; Разрешайте себе время от времени использовать слова-паразиты. Используйте их в умеренном количестве и только для того, чтобы замедлить свою речь, или может показаться, что вы плохо знаете материал и пытаетесь подбирать слова; Прочитайте текст вслух с разной скоростью. Попробуйте прочесть отрывок вслух на своей привычной скорости, а затем — быстрее обычного. Так любой другой темп будет казаться более медленным. Затем перечитайте текст, сознательно замедляя речь. И продолжайте замедляться до тех пор, пока темп не покажется преувеличенно медленным; Читайте текст вслух с разной громкостью. Постарайтесь сделать глубокий вдох, а потом выдыхайте весь воздух, заканчивая одну фразу. Делайте паузы между фразами.'
    return 'Вы говорите слишком медленно! Вот упражнения, которые помогут тебе говорить быстрее! Возьмите в рот карандаш и зажмите его зубами. Затем практикуйтесь говорить таким образом. Это поможет вам ускорить работу языка путем снижения пространства для произношения; Прочитайте что-нибудь наоборот. Хотя это может и показаться вам очень раздражительным и неприятным, такая методика поможет вам обрабатывать слова быстрее, что в итоге ускорит темп вашей речи; Прочитайте страницу книги, вставляя слово между каждым словом. Например: “Собака шла по улице” можно прочитать как “Курица собака курица шла курица по курица улице курица”. Если вы хотите что-то посложнее, то попробуйте слово с большим количеством слогов; Используйте простые и насыщенные слогами слова в обычной речи; Повторяйте те слова, которые трудно произнести.'


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
    tip = ''
    for word in unnecessary_words:
        if word.lower() in text.lower():
            list.append(word)
    if len(list) >= 3:
        tip = 'Как избавиться от слов-паразитов в речи? Читайте много литературы вслух. Благодаря чтению вслух вы сможете быстро строить свою речь и усовершенствуете дикцию, подкорректируете стилистику, научитесь правильно разговаривать; Научитесь себя контролировать. Самообладание – великая сила. Преодолев волнение, страх, излишнюю возбужденность, вы сможете и контролировать озвучку своих мыслей; Занимайтесь творчеством – сочиняйте. Сочинения помогают конструктивно излагать мысль, отшлифовывать изречение. Так мозг сможет насытиться новыми словами, которыми в последующем будет пользоваться; Не стоит торопиться. Торопливость только усугубляет. Лучше говорить постепенно, без спешки. Тогда ваш разговор не будет переполнен «мычанием» и различными сленгами; Анализ. Анализируя свою речь, вы сможете вовремя себя остановить, когда хочется сказать запретное слово, найти причину использования'
    return list, tip


def play(request):
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
    data = {'text': text, 'unnecessary_words': words, 'temp': temp_analysis, 'time': timing, 'freq': frequency_value, 'tip_words': tip_words}
    return render(request, 'audio/advices.html', data)


def getFreq(audio):
    chunk = 1024
    wf = wave.open(audio, 'rb')
    swidth = wf.getsampwidth()
    RATE = wf.getframerate()
    # use a Blackman window
    window = np.blackman(chunk)
    # open stream
    p = pyaudio.PyAudio()
    stream = p.open(format=
                    p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=RATE,
                    output=True)

    # read some data
    data = wf.readframes(chunk)
    # play stream and find the frequency of each chunk
    list_freq = []
    while len(data) == chunk * swidth:
        
        # write data out to the audio stream
        # unpack the data and times by the hamming window
        indata = np.array(wave.struct.unpack("%dh" % (len(data) / swidth), data)) * window
        # Take the fft and square each value
        fftData = abs(np.fft.rfft(indata)) ** 2
        # find the maximum
        which = fftData[1:].argmax() + 1
        # use quadratic interpolation around the max
        if which != len(fftData) - 1:
            y0, y1, y2 = np.log(fftData[which - 1:which + 2:])
            x1 = (y2 - y0) * .5 / (2 * y1 - y2 - y0)
            # find the frequency and output it
            thefreq = (which + x1) * RATE / chunk
            list_freq.append(thefreq)
        else:
            thefreq = which * RATE / chunk
            list_freq.append(thefreq)
        # read some more data
        data = wf.readframes(chunk)
    if data:
        stream.write(data)
    stream.close()
    p.terminate()
    result = np.mean(list_freq)
    return result

