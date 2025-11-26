from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO

import base64
import sendgrid
from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType, Disposition

from .models import Alumno
from .forms import AlumnoForm


# -------------------------------
# SendGrid: función para enviar PDF adjunto
# -------------------------------
def enviar_pdf_sendgrid(to_email, alumno, pdf_bytes):
   
    sg = sendgrid.SendGridAPIClient(api_key=settings.SENDGRID_API_KEY)

    mensaje = Mail(
        from_email=settings.DEFAULT_FROM_EMAIL,
        to_emails=to_email,
        subject=f"PDF del alumno {alumno.nombre} {alumno.apellido}",
        html_content=(
            f"<p>Adjunto PDF con los datos del alumno "
            f"<strong>{alumno.nombre} {alumno.apellido}</strong>.</p>"
        ),
    )

    # Convertir PDF a base64
    archivo_b64 = base64.b64encode(pdf_bytes).decode()

    attachment = Attachment(
        FileContent(archivo_b64),
        FileName("alumno.pdf"),
        FileType("application/pdf"),
        Disposition("attachment"),
    )

    mensaje.attachment = attachment

    sg.send(mensaje)


# -------------------------------
# Dashboard: listar + crear alumnos
# -------------------------------
@login_required
def dashboard_view(request):
    alumnos = Alumno.objects.filter(usuario=request.user)

    if request.method == "POST":
        form = AlumnoForm(request.POST)
        if form.is_valid():
            alumno = form.save(commit=False)
            alumno.usuario = request.user
            alumno.save()
            messages.success(request, "Alumno creado correctamente.")
            return redirect("alumnos:dashboard")
    else:
        form = AlumnoForm()

    return render(request, "alumnos/dashboard.html", {
        "alumnos": alumnos,
        "form": form,
    })


# -------------------------------
# Enviar PDF con datos del alumno
# -------------------------------
@login_required
def enviar_pdf_view(request, pk):
    alumno = get_object_or_404(Alumno, pk=pk, usuario=request.user)

    # Generar PDF en memoria
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)

    pdf.setFont("Helvetica", 14)
    pdf.drawString(50, 750, "Datos del alumno")

    pdf.setFont("Helvetica", 12)
    pdf.drawString(50, 720, f"Nombre: {alumno.nombre}")
    pdf.drawString(50, 700, f"Apellido: {alumno.apellido}")
    pdf.drawString(50, 680, f"Email: {alumno.email}")
    pdf.drawString(50, 660, f"Legajo: {alumno.legajo}")

    pdf.showPage()
    pdf.save()

    buffer.seek(0)
    pdf_bytes = buffer.read()

    # Enviar por SendGrid al email del usuario
    destino = request.user.email
    enviar_pdf_sendgrid(destino, alumno, pdf_bytes)

    messages.success(request, f"El PDF fue enviado por correo a {destino}.")
    return redirect("alumnos:dashboard")


# -------------------------------
# Editar alumno
# -------------------------------
@login_required
def alumno_editar_view(request, pk):
    alumno = get_object_or_404(Alumno, pk=pk, usuario=request.user)

    if request.method == "POST":
        form = AlumnoForm(request.POST, instance=alumno)
        if form.is_valid():
            form.save()
            messages.success(request, "Alumno actualizado correctamente.")
            return redirect("alumnos:dashboard")
    else:
        form = AlumnoForm(instance=alumno)

    return render(request, "alumnos/editar_alumno.html", {
        "form": form,
        "alumno": alumno,
    })


# -------------------------------
# Eliminar alumno
# -------------------------------
@login_required
def alumno_eliminar_view(request, pk):
    alumno = get_object_or_404(Alumno, pk=pk, usuario=request.user)

    if request.method == "POST":
        alumno.delete()
        messages.success(request, "Alumno eliminado correctamente.")
        return redirect("alumnos:dashboard")

    return render(request, "alumnos/confirmar_eliminar_alumno.html", {
        "alumno": alumno,
    })
