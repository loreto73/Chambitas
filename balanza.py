import pandas as pd
import numpy as np
import os

def imp_a(num, mes):
    A = pd.read_csv(f'/home/luis-loreto/Documentos/Trabajo/Balanza2024_ANAM/{num}{mes}2024/t_501.txt', 
        sep = '|', header=None, usecols=[0, 1, 2, 3, 4], 
        names=['Patente aduanal', 'Numero de pedimento', 'Seccion aduanera', 
               'Tipo de operacion', 'Clave de documento'])
    
    A = A[(A['Tipo de operacion'] == 1) & (A['Clave de documento'] == 'T1')]
    
    return A

def imp_b(num, mes):
    files = [
        f'/home/luis-loreto/Documentos/Trabajo/Balanza2024_ANAM/{num}{mes}2024/t_551_01.txt',
        f'/home/luis-loreto/Documentos/Trabajo/Balanza2024_ANAM/{num}{mes}2024/t_551_02.txt',
        f'/home/luis-loreto/Documentos/Trabajo/Balanza2024_ANAM/{num}{mes}2024/t_551_03.txt'
    ]

    dataframes = []
    for file in files:
        if os.path.exists(file):
            df = pd.read_csv(file, sep='|', header=None, usecols=[0, 1, 2, 8, 10, 21], 
                             names=['Patente aduanal', 'Numero de pedimento', 'Seccion aduanera', 
                                    'Valor en aduana', 'Valor en dólares', 'Pais de origen'])
            dataframes.append(df)

    if dataframes:
        B = pd.concat(dataframes, axis=0)
        return B
    else:
        return None
    
def cruce(num, mes):
    A = imp_a(num, mes) 
    B = imp_b(num, mes)
    C = pd.merge(A, B, on = ['Patente aduanal', 'Numero de pedimento', 'Seccion aduanera'], how='left')
    del A, B
    return C

def condiciones(mes):
    mes.dropna(inplace=True)
    conditions = [
        mes['Valor en dólares'] < 1,
        (mes['Valor en dólares'] >= 1) & (mes['Valor en dólares'] < 7),
        (mes['Valor en dólares'] >= 7) & (mes['Valor en dólares'] < 10),
        (mes['Valor en dólares'] >= 10) & (mes['Valor en dólares'] < 20),
        (mes['Valor en dólares'] >= 20) & (mes['Valor en dólares'] < 30),
        (mes['Valor en dólares'] >= 30) & (mes['Valor en dólares'] < 40),
        (mes['Valor en dólares'] >= 40) & (mes['Valor en dólares'] < 50),
        (mes['Valor en dólares'] >= 50) & (mes['Valor en dólares'] < 1000),
        (mes['Valor en dólares'] >= 1000) & (mes['Valor en dólares'] < 2500),
        (mes['Valor en dólares'] >= 2500) & (mes['Valor en dólares'] < 5000),
        mes['Valor en dólares'] >= 5000
    ]
    choices = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11']
    mes['Rango USD'] = np.select(conditions, choices)
    return mes

Enero = cruce("01", "Enero")
Febrero = cruce("02", "Febrero")
Marzo = cruce("03", "Marzo")
Abril = cruce("04", "Abril")
Mayo = cruce("05", "Mayo")
Junio = cruce("06", "Junio")
Julio = cruce("07", "Julio")
Agosto = cruce("08", "Agosto")
Septiembre = cruce("09", "Septiembre")

Enero["Mes"] = "Enero"
Febrero["Mes"] = "Febrero"
Marzo["Mes"] = "Marzo"
Abril["Mes"] = "Abril"
Mayo["Mes"] = "Mayo"
Junio["Mes"] = "Junio"
Julio["Mes"] = "Julio"
Agosto["Mes"] = "Agosto"
Septiembre["Mes"] = "Septiembre"

T12024 = pd.concat([Enero, Febrero], axis=0)
del Enero, Febrero
T12024 = pd.concat([T12024, Marzo], axis=0)
del Marzo
T12024 = pd.concat([T12024, Abril], axis=0)
del Abril
T12024 = pd.concat([T12024, Mayo], axis=0)
del Mayo
T12024 = pd.concat([T12024, Junio], axis=0)
del Junio
T12024 = pd.concat([T12024, Julio], axis=0)
del Julio
T12024 = pd.concat([T12024, Agosto], axis=0)
del Agosto
T12024 = pd.concat([T12024, Septiembre], axis=0)
del Septiembre

conteo_por_mes = T12024.groupby('Mes').size().reset_index(name='Conteo')
suma_por_mes = T12024.groupby('Mes')['Valor en dólares'].sum().reset_index(name='Suma')
resultado_final = pd.merge(conteo_por_mes, suma_por_mes, on='Mes')

print(resultado_final)