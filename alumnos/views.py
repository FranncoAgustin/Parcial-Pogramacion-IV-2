from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.contrib import messages
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from django.conf import settings
from io import BytesIO

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
@login_required
def enviar_pdf_view(request, pk):
    alumno = get_object_or_404(Alumno, pk=pk, usuario=request.user)

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

    email_destino = request.user.email  # ← el email con el que se registró

    email = EmailMessage(
        subject="PDF de Alumno",
        body=f"Aquí están los datos del alumno {alumno.nombre} {alumno.apellido}.",
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[email_destino],
    )
    email.attach("alumno.pdf", pdf_bytes, "application/pdf")
    email.send()

    messages.success(request, f"El PDF fue enviado por correo a {email_destino}.")
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