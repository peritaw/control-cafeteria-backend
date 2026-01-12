from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EmpleadoViewSet, CargoViewSet, AsistenciaViewSet, LoginView, FixDBView

router = DefaultRouter()
router.register(r'empleados', EmpleadoViewSet)
router.register(r'cargos', CargoViewSet)
router.register(r'asistencias', AsistenciaViewSet)

urlpatterns = [
    path('fix-db/', FixDBView.as_view(), name='fix-db'),
    path('login/', LoginView.as_view(), name='login'),
    path('', include(router.urls)),
]
