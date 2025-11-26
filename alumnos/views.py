from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.contrib import messages
from reportlab.pdfgen import canvas
from django.conf import settings
import io

from .models import Alumno
from .forms import AlumnoForm

@login_required
def dashboard_view(request):
    alumnos = Alumno.objects.filter(usuario=request.user)
    if request.method == "POST":
        form = AlumnoForm(request.POST)
        if form.is_valid():
            alumno = form.save(commit=False)
            alumno.usuario = request.user
            alumno.save()
            return redirect("alumnos:dashboard")
    else:
        form = AlumnoForm()

    return render(request, "alumnos/dashboard.html", {
        "alumnos": alumnos,
        "form": form,
    })

@login_required
def enviar_pdf_view(request, pk):
    alumno = get_object_or_404(Alumno, pk=pk, usuario=request.user)

    # 1) Generar PDF en memoria
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)
    p.setFont("Helvetica", 14)
    p.drawString(100, 800, "Datos del Alumno")
    p.setFont("Helvetica", 12)
    p.drawString(100, 770, f"Nombre: {alumno.nombre}")
    p.drawString(100, 750, f"Apellido: {alumno.apellido}")
    p.drawString(100, 730, f"Email: {alumno.email}")
    p.drawString(100, 710, f"Legajo: {alumno.legajo}")
    p.showPage()
    p.save()

    buffer.seek(0)
    pdf_bytes = buffer.getvalue()

    # 2) Enviar por correo (al docente o al propio usuario)
    destinatario = request.user.email  # o un EMAIL_DOCENTE fijo en settings
    email = EmailMessage(
        subject="PDF de Alumno",
        body=f"Envío PDF con los datos del alumno {alumno}.",
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[destinatario],
    )
    email.attach("alumno.pdf", pdf_bytes, "application/pdf")
    email.send()

    # Podés devolver un mensaje o redirigir:
    from django.contrib import messages
    messages.success(request, "PDF enviado por correo.")
    return redirect("alumnos:dashboard")

@login_required
def alumno_editar_view(request, pk):
    """
    Editar datos de un alumno propio.
    """
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


@login_required
def alumno_eliminar_view(request, pk):
    """
    Confirmar y eliminar un alumno propio.
    """
    alumno = get_object_or_404(Alumno, pk=pk, usuario=request.user)

    if request.method == "POST":
        alumno.delete()
        messages.success(request, "Alumno eliminado correctamente.")
        return redirect("alumnos:dashboard")

    return render(request, "alumnos/confirmar_eliminar_alumno.html", {
        "alumno": alumno,
    })