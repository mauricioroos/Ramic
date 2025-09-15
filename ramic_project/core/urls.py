from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard_view, name="painel"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("cadastro/", views.signup_view, name="cadastro"),

    path("motor/adicionar/", views.adicionar_motor_view, name="adicionar_motor"),
    path("motor/<int:motor_id>/editar/", views.editar_motor_view, name="editar_motor"),
    path("motor/<int:motor_id>/historico/", views.historico_view, name="historico"),
    path("motor/<int:motor_id>/ligar/", views.ligar_motor, name="ligar_motor"),
    path("motor/<int:motor_id>/desligar/", views.desligar_motor, name="desligar_motor"),
    path("motor/<int:motor_id>/apagar/", views.apagar_motor_view, name="apagar_motor"),
    path("motor/<int:motor_id>/manutencao/ativar/", views.iniciar_manutencao, name="ativar_manutencao"),
    path("motor/<int:motor_id>/manutencao/desativar/", views.finalizar_manutencao, name="desativar_manutencao"),

    path("api/motor/<int:motor_id>/heartbeat/", views.motor_heartbeat_view, name="motor_heartbeat"),
    path("api/motor/<int:motor_id>/status/", views.check_motor_status_view, name="check_motor_status"),
    path("historico/exportar/txt/", views.exportar_historico_txt_view, name="exportar_historico_txt"),
    path("api/sistema/status/", views.sistema_status_view, name="sistema_status"),
]