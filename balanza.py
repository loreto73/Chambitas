import pandas as pd

def imp_b(num, mes):

       B1 = pd.read_csv(f'/home/luis-loreto/Documentos/Trabajo/Balanza2024_ANAM/{num}{mes}2024/t_551_01.txt', 
                        sep = '|', header=None, usecols=[0, 1, 2, 8, 10, 21], 
                        names=['Patente aduanal', 'Numero de pedimento', 'Seccion aduanera', 'Valor en aduana', 'Valor en dólares', 'Pais de origen'])
    
       B2 = pd.read_csv(f'/home/luis-loreto/Documentos/Trabajo/Balanza2024_ANAM/{num}{mes}2024/t_551_02.txt', 
                        sep = '|', header=None, usecols=[0, 1, 2, 8, 10, 21], 
                        names=['Patente aduanal', 'Numero de pedimento', 'Seccion aduanera', 'Valor en aduana', 'Valor en dólares', 'Pais de origen'])
       
       B = pd.concat([B1, B2], axis=0)
       return B

def imp_a(num, mes):
    A = pd.read_csv(f'/home/luis-loreto/Documentos/Trabajo/Balanza2024_ANAM/{num}{mes}2024/t_501.txt', 
        sep = '|', header=None, usecols=[0, 1, 2, 3, 4], 
        names=['Patente aduanal', 'Numero de pedimento', 'Seccion aduanera', 
               'Tipo de operacion', 'Clave de documento'])
    
    A = A[(A['Tipo de operacion'] == 1) & (A['Clave de documento'] == 'T1')]
    
    return A

def cruce(num, mes):
    A = imp_a(num, mes) 
    B = imp_b(num, mes)
    C = pd.merge(A, B, on = ['Patente aduanal', 'Numero de pedimento', 'Seccion aduanera'], how='left')
    del A, B
    return C

Enero = cruce("01", "Enero")
Marzo = cruce("03", "Marzo")
Abril = cruce("04", "Abril")
Mayo = cruce("05", "Mayo")
Junio = cruce("06", "Junio")
Julio = cruce("07", "Julio")
Agosto = cruce("08", "Agosto")
Septiembre = cruce("09", "Septiembre")