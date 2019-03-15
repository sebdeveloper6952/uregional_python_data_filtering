import csv
from difflib import SequenceMatcher
import sys

"""
Programa para asociar pagos a estudiante, utilizando los reportes diarios que envia Banrural y la base de datos oficial de la
Universidad.

El reporte que envia el banco contiene errores, por ejemplo, puede aparecer el mismo estudiante una vez como "Jose Galvez" y
luego como "Jose Estuardo Galvez", por lo que debemos definir un criterio para decidir cuando dos nombres similares apuntan
al mismo estudiante.

Los datos que tenemos de cada estudiante son carnet y sus nombres y apellidos.
"""

# # revisar parametros de consola
# if len(sys.argv) < 4:
#     sys.exit("usage: prueba_leer_csv.py <official_data.csv> <payments.csv> <out_filename>")

# data_filename = sys.argv[1]
# payments_filename = sys.argv[2]
# out_filename = sys.argv[3]

"""
Retorna un numero entre 0 y 1, que representa la similitud entre las
cadenas de caracteres que se pasan como parametro.
"""
def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()
 
names_to_carnets = {}
names_to_payments = {}


def analyze(names_filename, payments_filename, out_filename):
    # leer nombres que tengan carnet valido de base de datos oficial
    with open(names_filename, newline='') as File:
        reader = csv.reader(File)
        for row in reader:
            try:
                int(row[2])
                name = row[4] + ' ' + row[5] + ' ' + row[6] + ' ' + row[7]
                names_to_carnets[name] = {'carnet':row[2], 'list': []}
            except:
                continue
    
    # leer archivo de pagos y asociar pagos a estudiante
    with open(payments_filename, newline='') as File:
        reader = csv.reader(File)
        for row in reader:
            if len(row[2]):
                if not names_to_payments.__contains__(row[9]):
                    names_to_payments[row[9]] = []
                names_to_payments[row[9]].append(row[13])

    # comparar nombres de archivo de pagos contra nombres oficiales, si el nombre
    # coincide en un 75% (por los errores humanos generados por el banco), entonces
    # se le agrega el cobro al estudiante.
    for k0, v0 in names_to_payments.items():
        for k1, v1 in names_to_carnets.items():
            s = similar(k0, k1)
            if s >= 0.75:
                names_to_carnets[k1]['list'] = names_to_payments[k0]
            # elif s < 0.05:
            #     print(k0, ' is not similar to: ', k1)

    with open(out_filename, 'w') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=['Carnet', 'Nombre', 'Cobro 1', 'Cobro 2', 'Cobro 3', 'Cobro 4', 'Cobro 5'])
        writer.writeheader()
        for k0, v0 in names_to_carnets.items():
            d = {'Carnet':names_to_carnets[k0]['carnet'], 'Nombre':k0}
            for i in range(len(names_to_carnets[k0]['list'])):
                d['Cobro ' + str(i + 1)] = names_to_carnets[k0]['list'][i]
            
            writer.writerow(d)