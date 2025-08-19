from django.contrib import admin
from .models import Produto

# Register your models here.
class ProdutoAdm(admin.ModelAdmin):
    list_display = ('nome', 'modelo', 'numeroSerial', 'corrente', 'potencia', 'tensao', 'descricao', 'localizacao', 'imagem')

admin.site.register(Produto, ProdutoAdm)
