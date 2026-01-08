from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Empleado, Cargo, Asistencia
from .serializers import EmpleadoSerializer, CargoSerializer, AsistenciaSerializer
from datetime import datetime

from rest_framework.authtoken.models import Token
from .auth_serializers import LoginSerializer
from rest_framework.views import APIView

class LoginView(APIView):
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
    serializer_class = AsistenciaSerializer
    permission_classes = [IsAuthenticated]

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
