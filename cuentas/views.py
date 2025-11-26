from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings

from .forms import RegistroForm
from django.contrib.auth.forms import AuthenticationForm


def registro_view(request):
    if request.method == "POST":
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # Setear la contraseña desde el campo del formulario
            user.set_password(form.cleaned_data["password"])
            user.save()

            # Enviar mail de bienvenida al email con el que se registró
            send_mail(
                "Bienvenido/a al sistema de alumnos",
                f"Hola {user.username}, gracias por registrarte.",
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
            )

            messages.success(
                request,
                f"Registro exitoso. Te enviamos un email de bienvenida a {user.email}. Ya podés iniciar sesión."
            )
            return redirect("cuentas:login")
    else:
        form = RegistroForm()

    return render(request, "cuentas/registro.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("alumnos:dashboard")
        else:
            messages.error(request, "Usuario o contraseña incorrectos.")
    else:
        form = AuthenticationForm(request)

    return render(request, "cuentas/login.html", {"form": form})


def logout_view(request):
    logout(request)
    messages.info(request, "Sesión cerrada correctamente.")
    return redirect("cuentas:login")
