from django.shortcuts import render
from django.contrib import messages
from django.conf import settings

from .forms import ScraperForm

import requests
from bs4 import BeautifulSoup

import sendgrid
from sendgrid.helpers.mail import Mail


# -------------------------------
# SendGrid helper
# -------------------------------
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


# -------------------------------
# Vista principal del scraper
# -------------------------------
def scraper_view(request):
    resultados = []

    if request.method == "POST":
        form = ScraperForm(request.POST)
        if form.is_valid():
            keyword = form.cleaned_data["keyword"]
            email_destino = form.cleaned_data["email"]

            try:
                # 1) Búsqueda en Wikipedia
                url = "https://es.wikipedia.org/w/index.php"
                params = {"search": keyword}
                headers = {
                    "User-Agent": (
                        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                        "AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Chrome/120.0.0.0 Safari/537.36"
                    ),
                    "Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
                }

                resp = requests.get(url, params=params, headers=headers, timeout=10)
                resp.raise_for_status()

                soup = BeautifulSoup(resp.text, "html.parser")

                # 2) Extraer resultados
                enlaces = soup.select(".mw-search-result-heading a")
                if not enlaces:
                    enlaces = soup.select("#mw-content-text .mw-search-result-heading a")

                # Redirección a artículo único
                if not enlaces:
                    titulo_unico = soup.select_one("#firstHeading")
                    if titulo_unico:
                        resultados.append({
                            "titulo": titulo_unico.get_text(strip=True),
                            "link": resp.url,
                        })
                else:
                    for a in enlaces[:10]:
                        titulo = a.get_text(strip=True)
                        link = "https://es.wikipedia.org" + a.get("href")
                        resultados.append({"titulo": titulo, "link": link})

                # 3) Formar HTML del correo
                if resultados:
                    cuerpo_html = f"<h3>Resultados de búsqueda para '{keyword}':</h3><ul>"
                    for res in resultados:
                        cuerpo_html += f"<li><a href='{res['link']}'>{res['titulo']}</a></li>"
                    cuerpo_html += "</ul>"
                else:
                    cuerpo_html = f"<p>No se encontraron resultados para '{keyword}'.</p>"

                # 4) Enviar email con SendGrid (Render-friendly)
                enviar_sendgrid(
                    email_destino,
                    f"Resultados de scraping para '{keyword}'",
                    cuerpo_html
                )

                messages.success(request, f"Scraping realizado y correo enviado a {email_destino} exitosamente.")

            except Exception as e:
                messages.error(request, f"Ocurrió un error al realizar el scraping: {e}")

    else:
        form = ScraperForm()

    return render(request, "scraper/scraper.html", {
        "form": form,
        "resultados": resultados,
    })
