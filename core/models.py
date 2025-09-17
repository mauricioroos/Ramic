from django.db import models
from django.contrib.auth.models import User, Group


class Motor(models.Model):
    grupos = models.ManyToManyField(Group, related_name="motores")
    nome = models.CharField(max_length=100)
    numero_serie = models.CharField(max_length=50, unique=True)
    descricao = models.TextField(blank=True, null=True)
    imagem = models.ImageField(upload_to="motores/", blank=True, null=True)
    localizacao = models.CharField(max_length=100, blank=True)
    modelo = models.CharField(max_length=100, blank=True)
    corrente = models.FloatField(null=True, blank=True, help_text="Corrente em Ampères (A)")
    potencia = models.FloatField(null=True, blank=True, help_text="Potência em Watts (W)")
    tensao = models.CharField(max_length=50, blank=True, help_text="Ex: 110V, 220V")
    ligado = models.BooleanField(default=False)
    em_manutencao = models.BooleanField(default=False)
    last_heartbeat = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.nome


class LogAcionamento(models.Model):
    ACOES = [
        ("LIGADO", "Ligado"),
        ("DESLIGADO", "Desligado"),
        ("MANUTENCAO_INICIO", "Manutenção Iniciada"),
        ("MANUTENCAO_FIM", "Manutenção Finalizada"),
    ]

    motor = models.ForeignKey(Motor, related_name="logs", on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    acao = models.CharField(max_length=20, choices=ACOES)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.motor.nome} - {self.get_acao_display()} em {self.timestamp.strftime('%d/%m/%Y %H:%M:%S')}"