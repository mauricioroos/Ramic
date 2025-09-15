from django.db import models
from django.db import models

# Classes banco de dados----------
class Produto(models.Model):
    nome = models.CharField('Nome', max_length=100, null=True)
    modelo = models.CharField('Modelo', max_length=10000, null=True)
    numeroSerial = models.DecimalField('Numero Serial', decimal_places=2, max_digits=8, null=True)
    corrente = models.DecimalField('Corrente', decimal_places=2, max_digits=8, null=True)
    potencia = models.DecimalField('Potencia', decimal_places=2, max_digits=8, null=True)
    tensao =models.DecimalField('Tensao', decimal_places=2, max_digits=8, null=True)
    descricao = models.CharField('Descrição',  max_length=100, null=True)
    localizacao = models.CharField('Localização',  max_length=100, null=True)
    #statusMotor = models.IntegerField('Status Motor', null=True)
    imagem = models.CharField('Imagem',  max_length=100, null=True)
    def __str__(self):
        return self.nome

class Monitoriamento(models.Model):
    dataHora = models.DateTimeField('Data e Hora', auto_now_add=True)
    #statusMotor = models.CharField('Status do Motor', max_length=20, choices=StatusMotor.choices, default=StatusMotor.DESLIGADO,)
    mensagem = models.CharField('Mensagem', max_length=100, null=True)
    def __str__(self):
        return self.mensagem
