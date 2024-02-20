from django.shortcuts import render
from django.http import JsonResponse
import time
import random


# Create your views here.
def index(request):
    initial_data = []

    return render(request, 'spacechart/index.html', {'data': initial_data})

def send_data(request):
    x = random.randint(1,10)
    y = random.randint(0, 100)
    print(f"Sending: x:{x} - y:{y}")
    return JsonResponse({'x': x, 'y': y})