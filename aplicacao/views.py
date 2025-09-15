from django.shortcuts import render
from .models import Produto
from .models import Monitoriamento

# Create your views here.
def produtos(request):
    produtos = Produto.objects.all()
    context = {
        'produtos' : produtos,
    }

def monitoramento(request):
    monitoramento = Monitoriamento.objects.all()
    context = {
        'monitoramento' : monitoramento,
    }

def index(request):
    context = {
        'texto': "Olá mundo!",
    }
    return render(request, 'index.html', context)
