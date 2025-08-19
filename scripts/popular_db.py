import os
import django
import random
import sys

# Caminho absoluto até a pasta raiz do projeto (onde está manage.py)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

# Configuração do Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pjramic.settings")
django.setup()

from aplicacao.models import Produto, Monitoriamento


def popular_produtos():
    produtos = [
        {
            "nome": "Motor Trifásico",
            "modelo": "MTX-200",
            "numeroSerial": 123456.00,
            "corrente": 10.50,
            "potencia": 750.00,
            "tensao": 220.00,
            "descricao": "Motor de indução trifásico 2CV",
            "localizacao": "Fábrica - Linha 1",
            "imagem": "motor_trifasico.jpg",
        },
        {
            "nome": "Bomba Hidráulica",
            "modelo": "BHP-500",
            "numeroSerial": 789012.00,
            "corrente": 7.80,
            "potencia": 500.00,
            "tensao": 380.00,
            "descricao": "Bomba de alta pressão",
            "localizacao": "Setor Hidráulico",
            "imagem": "bomba_hidraulica.png",
        },
        {
            "nome": "Compressor de Ar",
            "modelo": "CA-80L",
            "numeroSerial": 345678.00,
            "corrente": 15.00,
            "potencia": 1500.00,
            "tensao": 220.00,
            "descricao": "Compressor de ar de 80 litros",
            "localizacao": "Manutenção - Oficina",
            "imagem": "compressor_ar.jpg",
        },
        {
            "nome": "Ventilador Industrial",
            "modelo": "VI-1200",
            "numeroSerial": 901234.00,
            "corrente": 5.20,
            "potencia": 300.00,
            "tensao": 110.00,
            "descricao": "Ventilador de exaustão para ambientes industriais",
            "localizacao": "Armazém Principal",
            "imagem": "ventilador_industrial.jpeg",
        },
        {
            "nome": "Robô Manipulador",
            "modelo": "RM-7",
            "numeroSerial": 567890.00,
            "corrente": 25.00,
            "potencia": 3000.00,
            "tensao": 440.00,
            "descricao": "Braço robótico para linha de montagem",
            "localizacao": "Fábrica - Linha 3",
            "imagem": "robo_manipulador.jpg",
        },
        {
            "nome": "Painel de Controle",
            "modelo": "PC-Série 5",
            "numeroSerial": 112233.00,
            "corrente": 2.50,
            "potencia": 150.00,
            "tensao": 24.00,
            "descricao": "Painel elétrico de controle central",
            "localizacao": "Sala de Controle",
            "imagem": "painel_controle.png",
        },
    ]

    for p in produtos:
        Produto.objects.get_or_create(**p)

    print(f"{Produto.objects.count()} produtos cadastrados.")


def popular_monitoriamento():
    mensagens = [
    "Motor ligado normalmente",
    "Motor desligado",
    "Sobrecorrente detectada",
    "Manutenção preventiva necessária",
    "Superaquecimento",
    "Vibração Anormal",
    "Falha no rolamento",
    "Queda de tensão",
    "Baixa potência de saída",
    "Nível de óleo baixo",
    "Conexão perdida",
    "Filtro de ar obstruído"
]

    for msg in mensagens:
        Monitoriamento.objects.create(mensagem=msg)

    print(f"{Monitoriamento.objects.count()} registros de monitoramento criados.")


if __name__ == "__main__":
    popular_produtos()
    popular_monitoriamento()
    print("✅ Banco populado com sucesso!")
