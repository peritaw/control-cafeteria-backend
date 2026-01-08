from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, date

class Cargo(models.Model):
    nombre = models.CharField(max_length=50)
    valor_hora = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.nombre

class Empleado(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cargo = models.ForeignKey(Cargo, on_delete=models.PROTECT)
    
    def __str__(self):
        return self.user.username

class Asistencia(models.Model):
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    fecha = models.DateField(auto_now_add=True)
    hora_ingreso = models.TimeField(auto_now_add=True)
    hora_salida = models.TimeField(null=True, blank=True)
    horas_trabajadas = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    monto_total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def calcular_pago(self):
        if self.hora_salida and self.hora_ingreso:
            # Simple calculation assuming same day
            # If across midnight, logic needs to be robust, but for cafeteria likely same day.
            # Convert to datetime objects
            fmt = '%H:%M:%S'
            # We use dummy date
            d = date.today()
            dt_in = datetime.combine(d, self.hora_ingreso)
            dt_out = datetime.combine(d, self.hora_salida)
            
            diff = dt_out - dt_in
            hours = diff.total_seconds() / 3600
            self.horas_trabajadas = round(hours, 2)
            self.monto_total = self.horas_trabajadas * float(self.empleado.cargo.valor_hora)
            self.save()
