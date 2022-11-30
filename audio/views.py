from django.shortcuts import render
from .models import Recordings
from .forms import RecordingForm
from django.http import HttpResponseRedirect, HttpResponseNotFound

def without(request):
    return render(request, 'audio/without.html')
def readytext(request):
    return render(request, 'audio/readytext.html')
def minetext(request):
    return render(request, 'audio/minetext.html')

# получение данных из бд
def tips(request):
    records = Recordings.objects.all()
    return render(request, 'audio/tips.html', {'records': records})

# сохранение данных в бд
# def create(request):
#     form = RecordingForm()
#     return render(request, 'audio/tips.html', {'form': form})
def create(request):
    if request.method == "POST":
        form = RecordingForm()
        form.name = request.POST.get("speed")
        form.age = request.POST.get("text")
        form.save()
    return render(request, 'audio/tips.html', {'form': form})
