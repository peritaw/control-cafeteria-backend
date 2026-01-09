from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Empleado, Cargo, Asistencia
from .serializers import EmpleadoSerializer, CargoSerializer, AsistenciaSerializer, AsistenciaAdminSerializer
from datetime import datetime

from rest_framework.authtoken.models import Token
from .auth_serializers import LoginSerializer
from rest_framework.views import APIView

class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key, "username": user.username, "is_superuser": user.is_superuser})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CargoViewSet(viewsets.ModelViewSet):
    queryset = Cargo.objects.all()
    serializer_class = CargoSerializer
    permission_classes = [IsAuthenticated]

class EmpleadoViewSet(viewsets.ModelViewSet):
    queryset = Empleado.objects.all()
    serializer_class = EmpleadoSerializer
    permission_classes = [IsAuthenticated]

class AsistenciaViewSet(viewsets.ModelViewSet):
    queryset = Asistencia.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.user.is_staff:
             return AsistenciaAdminSerializer
        return AsistenciaSerializer

    def perform_update(self, serializer):
        instance = serializer.save()
        if instance.hora_ingreso and instance.hora_salida:
             instance.calcular_pago()
        else:
             # Reset values if incomplete
             instance.horas_trabajadas = None
             instance.monto_total = None
             instance.pagado = False # Reset paid status if invalidated? User didn't ask but makes sense.
             instance.save()

    @action(detail=False, methods=['post'])
    def pagar_empleado(self, request):
        # Mark specific records as paid
        ids = request.data.get('ids', [])
        if not ids:
             return Response({"error": "Falta lista de IDs (ids)"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Security: ensure we only update unpaid ones
        count = Asistencia.objects.filter(id__in=ids, pagado=False).update(pagado=True)
        return Response({"status": "ok", "actualizados": count})

    @action(detail=False, methods=['post'])
    def registrar_scan(self, request):
        user = request.user
        # Authentication is now guaranteed by permission_classes = [IsAuthenticated]
        
        try:
            empleado = Empleado.objects.get(user=user)
        except Empleado.DoesNotExist:
             return Response({"error": "Empleado no encontrado para el usuario actual"}, status=status.HTTP_404_NOT_FOUND)


        # Check for open record today
        today = datetime.now().date()
        open_record = Asistencia.objects.filter(empleado=empleado, fecha=today, hora_salida__isnull=True).first()

        if open_record:
            # Closing the shift
            open_record.hora_salida = datetime.now().time()
            open_record.calcular_pago()
            return Response({"status": "salida", "data": AsistenciaSerializer(open_record).data})
        else:
            # Opening the shift
            # Check if there was already a shift today? Maybe multiple shifts allowed.
            new_record = Asistencia.objects.create(empleado=empleado)
            return Response({"status": "entrada", "data": AsistenciaSerializer(new_record).data})
