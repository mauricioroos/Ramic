from django.shortcuts import render
from .models import Produto

# Create your views here.
def produtos(request):
    produtos = Produto.objects.all()
    context = {
        'produtos' : produtos,
    }

def index(request):
    context = {
        'texto': "Olá mundo!",
    }
    return render(request, 'index.html', context)
