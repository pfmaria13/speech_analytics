from django.shortcuts import render

# Create your views here.


def main(request):
    data = {
        'title': 'прив',
        'values': ['1', '2', '3']
    }
    return render(request, 'main/main.html', data)


def readytext(request):
    return render(request, 'main/readytext.html')


def minetext(request):
    return render(request, 'main/minetext.html')


def without(request):
    return render(request, 'main/without.html')
