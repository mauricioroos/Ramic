
from django.contrib import admin
from django.utils.html import mark_safe
from .models import Motor, LogAcionamento

@admin.register(Motor)
class MotorAdmin(admin.ModelAdmin):
    
    list_display = ('nome', 'numero_serie', 'localizacao', 'status_label', 'em_manutencao')
    
    list_filter = ('localizacao', 'ligado', 'em_manutencao')
    
    search_fields = ('nome', 'numero_serie', 'localizacao')

    @admin.display(description='Status')
    def status_label(self, obj):
        if obj.em_manutencao:
            return mark_safe('<span class="badge text-bg-warning">Em Manutenção</span>')
        elif obj.ligado:
            return mark_safe('<span class="badge text-bg-success">Ligado</span>')
        else:
            return mark_safe('<span class="badge text-bg-secondary">Desligado</span>')

@admin.register(LogAcionamento)
class LogAcionamentoAdmin(admin.ModelAdmin):
    list_display = ('motor', 'acao', 'timestamp')
    list_filter = ('motor', 'acao')