from django.contrib import admin
from .models import Produto
from .models import Monitoriamento

# Register your models here.
class ProdutoAdm(admin.ModelAdmin):
    list_display = ('nome', 'modelo', 'numeroSerial', 'corrente', 'potencia', 'tensao', 'descricao', 'localizacao', 'imagem')

admin.site.register(Produto, ProdutoAdm)

class monitoramentoAdm(admin.ModelAdmin):
    list_display = ('dataHora', 'mensagem')

admin.site.register(Monitoriamento, monitoramentoAdm)
