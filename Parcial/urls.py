from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path("", RedirectView.as_view(pattern_name="cuentas:login", permanent=False)),
    path("admin/", admin.site.urls),
    path("cuentas/", include("cuentas.urls")),
    path("alumnos/", include("alumnos.urls")),
    path("scraper/", include("scraper.urls")),
]
