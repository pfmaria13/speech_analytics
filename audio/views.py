from django.shortcuts import render
from .models import Recordings
from .forms import RecordingForm
from django.http import HttpResponseRedirect, HttpResponseNotFound

def without(request):
    return render(request, 'audio/without.html')
def ready(request):
    return render(request, 'audio/ready.html')
def mine(request):
    return render(request, 'audio/mine.html')

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
