from django.shortcuts import render
from django.core.mail import EmailMessage
from django.contrib import messages

from .forms import ScraperForm

import requests
from bs4 import BeautifulSoup


def scraper_view(request):
    resultados = []

    if request.method == "POST":
        form = ScraperForm(request.POST)
        if form.is_valid():
            keyword = form.cleaned_data["keyword"]
            email_destino = form.cleaned_data["email"]

            try:
                # 1) Hacer la búsqueda en Wikipedia con headers de navegador
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

                # 2) Intentar obtener lista de resultados
                enlaces = soup.select(".mw-search-result-heading a")
                if not enlaces:
                    enlaces = soup.select("#mw-content-text .mw-search-result-heading a")

                # Si tampoco hay, capaz Wikipedia redirigió directo al artículo:
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

                # 3) Armar cuerpo del correo
                if resultados:
                    cuerpo = f"Resultados de búsqueda para '{keyword}':\n\n"
                    for res in resultados:
                        cuerpo += f"- {res['titulo']}: {res['link']}\n"
                else:
                    cuerpo = f"No se encontraron resultados para '{keyword}'."

                # 4) Enviar email
                email = EmailMessage(
                    subject=f"Resultados de scraping para '{keyword}'",
                    body=cuerpo,
                    to=[email_destino],
                )
                email.send()

                messages.success(request, "Scraping realizado y correo enviado correctamente.")
            except Exception as e:
                messages.error(request, f"Ocurrió un error al realizar el scraping: {e}")
    else:
        form = ScraperForm()

    return render(request, "scraper/scraper.html", {
        "form": form,
        "resultados": resultados,
    })
