
"""
Este script obtiene las direcciones IP de una lista de sitios, esto para ponerlos en lista blanca del firewall

El archivo de URLS debe ser una url por linea, cada url debe llevar protocolo 
"""

import urllib.request as rq
from urllib.error import HTTPError
import re
import sys
import subprocess


BAD_LIST = ['facebook', 'whatsapp', 'telegram', 'twitter', 'skype', 'plus.google']

def limpio(elemento):
    for malo in BAD_LIST:
        if malo in elemento:
            return False
    return True


def filtrarMalos(lista):
    return [ele for ele in lista if limpio(ele)]
    

def quitarExtra(elemento):
    """
    Para limpiar un poco más algunos resultados de regx
    """
    if '"' in elemento:
        return elemento.split('"')[0]
    if "'" in elemento:
        return elemento.split("'")[0]
    return elemento


def extraerReferenciasURL(url):
    """
    Dada una url regresa aquellas referencias completas (con protocolo)
    de elementos src y href
    """
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'}

    patronSrc = r"src=[\"'].*?//(.*?)/.*?[\"']"
    patronHref = r"href=[\"'].*?//(.*?)/.*?[\"']"

    c1 = re.compile(patronSrc, re.DOTALL)
    c2 = re.compile(patronHref, re.DOTALL)
    request = rq.Request(url, headers=headers)
    try:
        response = rq.urlopen(request)
        contenido = response.read().decode('utf-8')
        m1 = c1.findall(contenido)
        m2 = c2.findall(contenido)
        limpios = filtrarMalos(m1 + m2)
        limpios = list(map(quitarExtra, limpios))
        return set(limpios)

    except HTTPError as error:
        print('Hubo un error al obtener datos de URL: %s' % url)
        return []

def regresarDominio(url):
    patron = r".*?//(.*?)/.*?"
    c = re.compile(patron, re.DOTALL)
    res = c.findall(url)
    if res:
        return res[0]
    return ''
    


def obtenerIP(dominio):
    result = subprocess.run(['dig', dominio], stdout=subprocess.PIPE)
    result = result.stdout.decode('utf-8')
    respuesta = result.split('ANSWER SECTION')
    if len(respuesta) == 1: #no se encontro
        print('No se encontro ip de %s' % dominio)
        return ''
    respuesta = respuesta[1]
    respuesta = respuesta.split('Query')[0]
    patron = r"(\d+?\.\d+?\.\d+?\.\d+)"
    c = re.compile(patron)
    res = c.findall(respuesta)
    return res


def hacerDig(conjuntoURLs):
    res = []
    for elemento in conjuntoURLs:
        res += obtenerIP(elemento)
    return set(res)


def sacarReglaIPTables(ip):
    print('iptables -A FORWARD -p tcp -d %s -j ACCEPT' % ip)
    print('iptables -A FORWARD -p tcp -s %s -j ACCEPT' % ip)


def procesarUrls(archivo):
    urls = []
    with open(archivo) as paginas:
        for linea in paginas:
            limpia = linea.strip()            
            while limpia.endswith('/'):
                limpia = limpia[:-1]
            urls.append(regresarDominio(limpia))
            urls += extraerReferenciasURL(limpia)
    #ips = hacerDig(set(urls))
    ips = set(urls)
    for ip in ips:
        sacarReglaIPTables(ip)

        
procesarUrls(sys.argv[1])

    

