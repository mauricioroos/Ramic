
from django.apps import AppConfig
from django.conf import settings

class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "core"

    # INICIAR O CLIENTE MQTT QUANDO O DJANGO INICIAR: DAVI
    def ready(self):
        #if not settings.DEBUG:  # Opcional: só iniciar em produção? Ou sempre?
        if settings.DEBUG:
            from .mqtt_client import MqttClient
            import threading

            # Inicia o cliente MQTT em uma thread separada
            client = MqttClient()
            thread = threading.Thread(target=client.connect, daemon=True)
            thread.start()