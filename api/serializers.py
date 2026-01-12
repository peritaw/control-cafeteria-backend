from rest_framework import serializers
from .models import Empleado, Cargo, Asistencia
from django.contrib.auth.models import User

class CargoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cargo
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']

class EmpleadoSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    first_name = serializers.CharField(write_only=True, required=False)
    last_name = serializers.CharField(write_only=True, required=False)
    
    user = UserSerializer(read_only=True)
    cargo_nombre = serializers.CharField(source='cargo.nombre', read_only=True)
    
    class Meta:
        model = Empleado
        fields = ['id', 'user', 'cargo', 'cargo_nombre', 'username', 'password', 'first_name', 'last_name', 'frecuencia_pago']

    def create(self, validated_data):
        user_data = {
            'username': validated_data.pop('username'),
            'password': validated_data.pop('password'),
            'first_name': validated_data.pop('first_name', ''),
            'last_name': validated_data.pop('last_name', '')
        }
        user = User.objects.create_user(**user_data)
        empleado = Empleado.objects.create(user=user, **validated_data)
        return empleado

    def update(self, instance, validated_data):
        # We generally won't update username/password here for simplicity in this demo,
        # but we can update the Cargo.
        if 'cargo' in validated_data:
            instance.cargo = validated_data['cargo']
        instance.save()
        return instance

class AsistenciaSerializer(serializers.ModelSerializer):
    empleado_nombre = serializers.SerializerMethodField()
    
    class Meta:
        model = Asistencia
        fields = '__all__'
        read_only_fields = ['horas_trabajadas', 'monto_total', 'fecha', 'hora_ingreso']

    def get_empleado_nombre(self, obj):
        return obj.empleado.user.first_name or obj.empleado.user.username

class AsistenciaAdminSerializer(serializers.ModelSerializer):
    empleado_nombre = serializers.SerializerMethodField()
    
    class Meta:
        model = Asistencia
        fields = '__all__'
        read_only_fields = ['horas_trabajadas', 'monto_total']  # Admin can edit times and dates

    def get_empleado_nombre(self, obj):
        return obj.empleado.user.first_name or obj.empleado.user.username

