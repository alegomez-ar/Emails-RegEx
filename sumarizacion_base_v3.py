# ------------------------------------------------------------------------------
# Alcance
# ------------------------------------------------------------------------------

# Se toma el archivo "Base email para validar V3" y se depuran
# dominios y otras reglas de validación.

# ------------------------------------------------------------------------------
# Impotar librerías
# ------------------------------------------------------------------------------

from numpy.core.fromnumeric import sort
import pandas as pd
import re


# ------------------------------------------------------------------------------
# Impotar csv de emails
# ------------------------------------------------------------------------------

path = 'C:/Users/AG/Documents/01 - solution/Emailing/Base mail para validar V3 - 2022-06-02.csv'
df = pd.read_csv(path)


# df.drop_duplicates(subset='Email address', keep='first', inplace=True)

# df_1 = df[df['Email address'].str.contains("admin")==False]


grupos = df.groupby("domain").sample(n=1)


# ------------------------------------------------------------------------------
# Conteo Incial por Grupos
# ------------------------------------------------------------------------------

cg_inicial = pd.DataFrame(df['filename'].value_counts()).sort_index()

# ------------------------------------------------------------------------------
# Reglas de validación
# ------------------------------------------------------------------------------

# Excluir email que no tienen ".com" o ".ar" al final del dominio.
exp11 = r'^(com|ar)$'
df.dropna(subset=['COD-1'], inplace=True)

# Excluir dominios que empizan con números .
exp12 = r"\d"

# Excluir nombres y dominios que se tienen tres caracteres iguales y consecutivos
exp13 = r"([a-zA-Z0-9])\1\1+"

# Excluir palabras claves
term14 = []
exp14 = r'(?:{})'.format('|'.join(map(re.escape, term14)))

# Corregir palabras mal escritas. Esto se ejecuta en el mismo paso.
term15 = []
exp15 = r'(?:{})'.format('|'.join(map(re.escape, term15)))
df['Email address'].replace(regex=exp15,value='@hotmail.', inplace=True)



# ------------------------------------------------------------------------------
# Funciones y procesos
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# Parametrizar la cantidad de RegEx a procesar
# ------------------------------------------------------------------------------

# Lista de RegEx a procesar
reg_ex = [exp12]
#reg_ex = [exp0,exp1,exp2,exp3]

# Crear el nombre de las columnas a incorporar al df para guardar los valores bool
col_exp = []
nro = len(reg_ex)
for i in range(nro):
    col_exp.append(f"exp{i}")

columns = ['domain']

# Ejecutar las RegEx. Itera la lista de "expresion", agrega la columna "exp(i)" y valida las exp.

for exp,valid,column in zip(reg_ex,col_exp,columns):
    criterio = (df[column].str.contains(exp))
    df.loc[criterio, valid] = 'SI'
    df.loc[~criterio, valid] = 'NO'
    count = pd.DataFrame(df[valid].value_counts()).sort_index()
    print(count)
    print('------')
    if count.iloc[0,0] > count.iloc[1,0]:
        df.drop(df[df[valid]=='SI'].index, inplace=True)
        df.drop([valid], axis=1, inplace=True)
    else:
        df.drop(df[df[valid]=='NO'].index, inplace=True)
        df.drop([valid], axis=1, inplace=True)


conteo = df['domain'].value_counts()
series = conteo[conteo < 1].index.tolist()
df2 = pd.DataFrame(series)
df2


# Eliminar duplicados
df.drop_duplicates(subset='Email address', keep='first', inplace=True)

# ------------------------------------------------------------------------------
# Sumarización de df para contabilizar cantidades perdidas 
# ------------------------------------------------------------------------------

# Cuenta los email por el grupo Filename 
cg_final = pd.DataFrame(df['filename'].value_counts()).sort_index()

# Merge de DF cg_ para comparar los casos perdidos
cg_comparado = cg_inicial.merge(cg_final, left_index=True, right_index=True)

# Crear un df que contenga la palabra clave
df1 = df[df["Email address"].str.contains('palabra clave')]

# ------------------------------------------------------------------------------
# exportar csv 
# ------------------------------------------------------------------------------

path2 = 'C:/Users/AG/Documents/01 - solution/Emailing/base_testear_dominios.csv'
grupos.to_csv(path2, index=False)
