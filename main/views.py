from django.shortcuts import render

# Create your views here.


def main(request):
    data = {
        'title': 'прив',
        'values': ['1', '2', '3']
    }
    return render(request, 'main/main.html', data)


def ready(request):
    return render(request, 'audio/ready.html')


def mine(request):
    return render(request, 'audio/mine.html')


def without(request):
    return render(request, 'audio/without.html')


