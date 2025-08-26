from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from datetime import timedelta
from .models import Motor, LogAcionamento
from django import forms


# ---------------------- FORMULÁRIO ----------------------
class MotorForm(forms.ModelForm):
    class Meta:
        model = Motor
        fields = [
            'nome', 'modelo', 'numero_serie', 
            'corrente', 'potencia', 'tensao', 
            'localizacao', 'descricao', 'imagem'
        ]
        
        # Define os nomes corretos com acentos
        labels = {
            'nome': 'Nome do Motor',
            'numero_serie': 'Número Serial',
            'potencia': 'Potência (W)',
            'tensao': 'Tensão (V)',
            'corrente': 'Corrente (A)',
            'localizacao': 'Localização',
            'descricao': 'Descrição',
        }

        # Adiciona exemplos (placeholders) e a classe de estilo do Bootstrap
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'modelo': forms.TextInput(attrs={'class': 'form-control'}),
            'numero_serie': forms.TextInput(attrs={'class': 'form-control'}),
            'corrente': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 6.8', 'step': '0.01'}),
            'potencia': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 1500'}),
            'tensao': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 220V'}),
            'localizacao': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'imagem': forms.FileInput(attrs={'class': 'form-control'}),
        }

    


# ---------------------- AUTENTICAÇÃO ----------------------
def login_view(request):
    if request.user.is_authenticated:
        return redirect("painel")
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data.get('username'),
                password=form.cleaned_data.get('password')
            )
            if user is not None:
                login(request, user)
                return redirect("painel")
        messages.error(request, "Usuário ou senha inválidos.")
    return render(request, "core/autenticacao/entrar.html", {"form": AuthenticationForm()})


def signup_view(request):
    if request.user.is_authenticated:
        return redirect("painel")
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("painel")
    return render(request, "core/autenticacao/cadastrar.html", {"form": UserCreationForm()})


def logout_view(request):
    logout(request)
    return redirect('login')


# ---------------------- PAINEL ----------------------
@login_required
def dashboard_view(request):
    q = request.GET.get("q", "").strip()
    motores = Motor.objects.all()
    if q:
        motores = motores.filter(
            Q(nome__icontains=q) |
            Q(numero_serie__icontains=q) |
            Q(localizacao__icontains=q)
        )
    return render(request, "core/motores/painel.html", {"motores": motores, "q": q})


# ---------------------- CRUD MOTOR ----------------------
@login_required
def adicionar_motor_view(request):
    if request.method == "POST":
        form = MotorForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("painel")
    return render(request, "core/motores/adicionar_motor.html", {"form": MotorForm()})


@login_required
def editar_motor_view(request, motor_id: int):
    motor = get_object_or_404(Motor, id=motor_id)
    if request.method == "POST":
        form = MotorForm(request.POST, request.FILES, instance=motor)
        if form.is_valid():
            form.save()
            return redirect("painel")
    return render(request, "core/motores/editar_motor.html", {"form": MotorForm(instance=motor), "motor": motor})


@login_required
def apagar_motor_view(request, motor_id: int):
    motor = get_object_or_404(Motor, id=motor_id)
    motor.delete()
    return redirect("painel")


# ---------------------- HISTÓRICO ----------------------
@login_required
def historico_view(request, motor_id: int):
    motor = get_object_or_404(Motor, id=motor_id)
    # CORREÇÃO 1: Adicionado o sinal de menos (-) para ordenar do mais novo para o mais antigo
    logs = motor.logs.all().order_by('-timestamp')

    return render(request, "core/motores/historico.html", {"motor": motor, "logs": logs})


# ---------------------- AÇÕES ----------------------
@login_required
def ligar_motor(request, motor_id):
    motor = get_object_or_404(Motor, id=motor_id)
    motor.ligado = True
    motor.save()
    LogAcionamento.objects.create(motor=motor, acao="LIGADO", usuario=request.user)
    return redirect("painel")


@login_required
def desligar_motor(request, motor_id):
    motor = get_object_or_404(Motor, id=motor_id)
    motor.ligado = False
    motor.save()
    LogAcionamento.objects.create(motor=motor, acao="DESLIGADO", usuario=request.user)
    return redirect("painel")


@login_required
def iniciar_manutencao(request, motor_id):
    motor = get_object_or_404(Motor, id=motor_id)
    motor.em_manutencao = True
    motor.save()
    LogAcionamento.objects.create(motor=motor, acao="MANUTENCAO_INICIO", usuario=request.user)
    return redirect("painel")


@login_required
def finalizar_manutencao(request, motor_id):
    motor = get_object_or_404(Motor, id=motor_id)
    motor.em_manutencao = False
    motor.save()
    LogAcionamento.objects.create(motor=motor, acao="MANUTENCAO_FIM", usuario=request.user)
    return redirect("painel")


# ---------------------- API ----------------------
@require_POST
def motor_heartbeat_view(request, motor_id: int):
    motor = get_object_or_404(Motor, id=motor_id)
    motor.last_heartbeat = timezone.now()
    motor.save(update_fields=['last_heartbeat'])
    return JsonResponse({'status': 'ok'})


@login_required
def check_motor_status_view(request, motor_id: int):
    motor = get_object_or_404(Motor, id=motor_id)
    status = 'offline'
    if motor.last_heartbeat and timezone.now() - motor.last_heartbeat < timedelta(seconds=30):
        status = 'online'
    return JsonResponse({'status': status})


@login_required
def exportar_historico_txt_view(request):
    response = HttpResponse(content_type='text/plain; charset=utf-8')
    response['Content-Disposition'] = f'attachment; filename="historico_motores_{timezone.now().strftime("%Y-%m-%d")}.txt"'
    logs = LogAcionamento.objects.all().order_by('-timestamp')
    linhas = [f"Relatório de Histórico de Motores - Gerado em: {timezone.now().strftime('%d/%m/%Y %H:%M')}\n\n"]
    for log in logs:
        linhas.append(f"{log.motor.nome} | {log.timestamp.strftime('%d/%m/%Y %H:%M')} | {log.get_acao_display()} | Usuário: {log.usuario}\n")
    response.writelines(linhas)
    return response


@login_required
def sistema_status_view(request):
    motores = Motor.objects.all()
    status_geral = "ok"
    for motor in motores:
        if motor.em_manutencao:
            status_geral = "manutencao"
    return JsonResponse({'status': status_geral})
