from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.views.decorators.http import require_POST
from django.contrib import messages  # Importe o messages
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from datetime import timedelta
from .models import Motor, LogAcionamento
from .forms import MotorForm # Importe o MotorForm do seu forms.py

# ---------------------- AUTENTICAÇÃO (Mantido como estava) ----------------------
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
    form = AuthenticationForm()
    return render(request, "core/autenticacao/entrar.html", {"form": form})


def signup_view(request):
    if request.user.is_authenticated:
        return redirect("painel")
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Conta criada com sucesso para {user.username}!')
            return redirect("painel")
    form = UserCreationForm()
    return render(request, "core/autenticacao/cadastrar.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect('login')


# ---------------------- PAINEL (Mantido como estava) ----------------------
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


# ---------------------- CRUD MOTOR (Refatorado) ----------------------
@login_required
def adicionar_motor_view(request):
    if request.method == "POST":
        form = MotorForm(request.POST, request.FILES)
        if form.is_valid():
            motor = form.save()
            # Adiciona uma mensagem de sucesso
            messages.success(request, f'O motor "{motor.nome}" foi adicionado com sucesso!')
            return redirect("painel")
        else:
            # Adiciona uma mensagem de erro se o formulário for inválido
            messages.error(request, 'Ocorreu um erro. Por favor, verifique os dados inseridos.')
    else:
        form = MotorForm()
    
    return render(request, "core/motores/adicionar_motor.html", {"form": form})


@login_required
def editar_motor_view(request, motor_id: int):
    motor = get_object_or_404(Motor, id=motor_id)
    if request.method == "POST":
        form = MotorForm(request.POST, request.FILES, instance=motor)
        if form.is_valid():
            form.save()
            # Adiciona uma mensagem de sucesso
            messages.success(request, f'O motor "{motor.nome}" foi atualizado com sucesso!')
            return redirect("painel")
        else:
            # Adiciona uma mensagem de erro se o formulário for inválido
            messages.error(request, 'Ocorreu um erro. Por favor, verifique os dados inseridos.')
    else:
        form = MotorForm(instance=motor)

    return render(request, "core/motores/editar_motor.html", {"form": form, "motor": motor})


@login_required
@require_POST # Garante que esta view só aceita requisições POST
def apagar_motor_view(request, motor_id: int):
    motor = get_object_or_404(Motor, id=motor_id)
    nome_motor = motor.nome
    motor.delete()
    messages.success(request, f'O motor "{nome_motor}" foi apagado com sucesso.')
    return redirect("painel")


# ---------------------- HISTÓRICO (Mantido como estava) ----------------------
@login_required
def historico_view(request, motor_id: int):
    motor = get_object_or_404(Motor, id=motor_id)
    logs = motor.logs.all().order_by('-timestamp')
    return render(request, "core/motores/historico.html", {"motor": motor, "logs": logs})


# ---------------------- AÇÕES (Refatorado com mensagens) ----------------------
@login_required
@require_POST
def ligar_motor(request, motor_id):
    motor = get_object_or_404(Motor, id=motor_id)
    motor.ligado = True
    motor.save()
    LogAcionamento.objects.create(motor=motor, acao="LIGADO", usuario=request.user)
    messages.info(request, f'Motor "{motor.nome}" ligado.')
    return redirect("painel")


@login_required
@require_POST
def desligar_motor(request, motor_id):
    motor = get_object_or_404(Motor, id=motor_id)
    motor.ligado = False
    motor.save()
    LogAcionamento.objects.create(motor=motor, acao="DESLIGADO", usuario=request.user)
    messages.info(request, f'Motor "{motor.nome}" desligado.')
    return redirect("painel")


@login_required
@require_POST
def iniciar_manutencao(request, motor_id):
    motor = get_object_or_404(Motor, id=motor_id)
    motor.em_manutencao = True
    motor.save()
    LogAcionamento.objects.create(motor=motor, acao="MANUTENCAO_INICIO", usuario=request.user)
    messages.warning(request, f'Motor "{motor.nome}" colocado em manutenção.')
    return redirect("painel")


@login_required
@require_POST
def finalizar_manutencao(request, motor_id):
    motor = get_object_or_404(Motor, id=motor_id)
    motor.em_manutencao = False
    motor.save()
    LogAcionamento.objects.create(motor=motor, acao="MANUTENCAO_FIM", usuario=request.user)
    messages.info(request, f'Motor "{motor.nome}" retirado da manutenção.')
    return redirect("painel")


# ---------------------- API (Mantido como estava) ----------------------
# (O resto do seu código de API pode continuar aqui sem alterações)

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