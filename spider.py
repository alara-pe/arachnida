import os
import sys
import argparse
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import urllib.request

# Analizar las opciones de línea de comandos
parser = argparse.ArgumentParser(description="Descarga todas las imágenes de un sitio web de manera recursiva.")
parser.add_argument("url", help="URL del sitio web")
parser.add_argument("-r", "--recursive", action="store_true", help="descarga de forma recursiva las imágenes en una URL recibida como parámetro")
parser.add_argument("-l", "--level", type=int, default=5, help="indica el nivel profundidad máximo de la descarga recursiva")
parser.add_argument("-p", "--path", default="./data/", help="indica la ruta donde se guardarán los archivos descargados")
parser.add_argument("-v", "--verbose", action="store_true", help="muestra por pantalla lo que hace el programa")
args = parser.parse_args()

# Lista de extensiones de archivo a descargar
extensions = [".jpg", ".jpeg", ".png", ".gif", ".bmp"]

# Lista de imágenes descargadas
downloaded_images = []

def download_images(url, path, level, count):
    # Si la URL es un archivo local, abrir el archivo en modo lectura
    if url.startswith("file://"):
        with open(urlparse(url).path, "rb") as f:
            content = f.read()
    else:
        # Obtener el contenido HTML de la página
        response = requests.get(url)
        content = response.content

    # Convertir el contenido HTML en un objeto BeautifulSoup
    soup = BeautifulSoup(content, "html.parser")
    # Encontrar todas las etiquetas de imagen
    img_tags = soup.find_all("img")
    
    # Descargar cada imagen
    for img_tag in img_tags:
        img_url = img_tag["src"]
        if not img_url.startswith("http"):
            img_url =  urljoin(url, img_url)
        img_ext = os.path.splitext(img_url)[1]
        if img_ext in extensions and img_url not in downloaded_images:
            img_name = "imagen" + str(count) + img_ext
            img_path = os.path.join(path, img_name)
            try:
                with open(img_path, "wb") as f:
                    if img_url.startswith("file://"):
                        with open(urlparse(img_url).path, "rb") as img_file:
                            f.write(img_file.read())
                    else:
                        f.write(requests.get(img_url).content)
            
                if args.verbose:
                        print("Descargando", img_url, "como", img_name, "desde", url)
                        downloaded_images.append(img_url)
                count += 1

            except: 
                print("Se ha producido un error", " desde " , img_url)
           
    # Descargar imágenes de los subdominios
    if level > 1:
        subdomains = [link.get("href") for link in soup.find_all("a") if link.get("href") and link.get("href",).startswith(url)]
        for subdomain in subdomains:
            count = download_images(subdomain, path, level - 1, count)
    
    return count


if not os.path.exists(args.path):
    os.makedirs(args.path)
count = download_images(args.url, args.path, args.level, 1)

if args.verbose:
    print("Se han descargado", count - 1, "imágenes.")
