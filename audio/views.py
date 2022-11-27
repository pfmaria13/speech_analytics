from django.shortcuts import render


def audio(request):
    return render(request, 'audio/audio.html')
