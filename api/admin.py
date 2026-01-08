from django.contrib import admin
from .models import Cargo, Empleado, Asistencia

@admin.register(Cargo)
class CargoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'valor_hora')

@admin.register(Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ('user', 'cargo', 'get_valor_hora')
    
    def get_valor_hora(self, obj):
        return obj.cargo.valor_hora
    get_valor_hora.short_description = 'Valor Hora'

@admin.register(Asistencia)
class AsistenciaAdmin(admin.ModelAdmin):
    list_display = ('empleado', 'fecha', 'hora_ingreso', 'hora_salida', 'horas_trabajadas', 'monto_total')
    list_filter = ('fecha', 'empleado__cargo')
    search_fields = ('empleado__user__username',)
    readonly_fields = ('horas_trabajadas', 'monto_total')
