"""
Script para rellenar template de settings con configuracion de script bash
"""

import sys


snh = sys.argv[1]
snp = sys.argv[2]
resDir = sys.argv[3]
examenTemplate = sys.argv[4]

archivoTempalte = open('examen/settingsTemplate.py')
contenido = archivoTempalte.read()
archivoTempalte.close()

with open('examen/settings.py', 'w') as salida:
    salida.write(contenido % (resDir, snh, snp, examenTemplate))

