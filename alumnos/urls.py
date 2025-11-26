from django.urls import path
from . import views

app_name = "alumnos"

urlpatterns = [
    path("", views.dashboard_view, name="dashboard"),
    path("<int:pk>/enviar_pdf/", views.enviar_pdf_view, name="enviar_pdf"),
    path("<int:pk>/editar/", views.alumno_editar_view, name="alumno_editar"),
    path("<int:pk>/eliminar/", views.alumno_eliminar_view, name="alumno_eliminar"),
]
