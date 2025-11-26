from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from django.conf import settings

import sendgrid
from sendgrid.helpers.mail import Mail

from .forms import RegistroForm
from django.contrib.auth.forms import AuthenticationForm


# --------------------------------------------
# Función para enviar emails reales con SendGrid
# --------------------------------------------
def enviar_sendgrid(to_email, subject, html_content):
    """Enviar email real usando SendGrid API."""
    sg = sendgrid.SendGridAPIClient(api_key=settings.SENDGRID_API_KEY)
    email = Mail(
        from_email=settings.DEFAULT_FROM_EMAIL,
        to_emails=to_email,
        subject=subject,
        html_content=html_content,
    )
    sg.send(email)


# --------------------------------------------
# Registro de usuario
# --------------------------------------------
def registro_view(request):
    if request.method == "POST":
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)

            # Establecer contraseña
            user.set_password(form.cleaned_data["password"])
            user.save()

            # Enviar email real de bienvenida
            enviar_sendgrid(
                user.email,
                "Bienvenido/a al sistema de alumnos",
                f"""
                <p>Hola <strong>{user.username}</strong>,</p>
                <p>Gracias por registrarte en el sistema de alumnos.</p>
                """
            )

            messages.success(
                request,
                f"Registro exitoso. Te enviamos un email de bienvenida a {user.email}. Ya podés iniciar sesión."
            )
            return redirect("cuentas:login")
    else:
        form = RegistroForm()

    return render(request, "cuentas/registro.html", {"form": form})


# --------------------------------------------
# Login
# --------------------------------------------
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


# --------------------------------------------
# Logout
# --------------------------------------------
def logout_view(request):
    logout(request)
    messages.info(request, "Sesión cerrada correctamente.")
    return redirect("cuentas:login")
