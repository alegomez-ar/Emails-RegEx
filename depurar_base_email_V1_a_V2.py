# ----------------------------------------------------------
# Alcance
# ----------------------------------------------------------

# Este archivo toma "Base mail para validar V1" y aplica los criterios 
# definidos para eliminar los emails que se consideran erroneos.
# Luego genera un nuevo archivo con el nombre "Base para Validar V2"

# ----------------------------------------------------------
# Impotar librerías
# ----------------------------------------------------------

from numpy.core.fromnumeric import sort
import pandas as pd
import re

# ----------------------------------------------------------
# Impotar csv de emails
# ----------------------------------------------------------

path = 'C:/Users/AG//Emailing/Base mail para validar V1.csv'
df = pd.read_csv(path)

df.drop_duplicates(subset='Email address', keep='first', inplace=True)

# ----------------------------------------------------------
# Reglas de validación
# ----------------------------------------------------------

# ------------ 1 ------------ PRIMER NIVEL: Verificar estructura

# Valida la longitud de caracteres del email según el estándar RFC2822.
exp0 = r"^[a-z0-9!#$%&'*+/=?^_‘{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_‘{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])$"

# Valida que se cumpla con la estructura de un email y excluye caracteres especiales como " {(/`~'? " etc
exp1 = r"^[A-Za-z0-9\._-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$"

# ------------ 2 ------------ SEGUNDO NIVEL: Eliminar combinaciones anormales

# Excluir email que empiezan con números en el nombre.
# Bueno --> 5setnidosdecoalmacen@gmail.com
# Malo  --> 007@hotmail.com
# Malo  --> 0-0-0-0@hotmail.com
exp2 = r"^[0-9]+"

# Excluir email que tienen 5 o más números en el nombre o dominio.
# 123456@hotmail.com
# 123456asdf@hotmail.com
# nombre@web123456.com
exp3 = r"\d{5,50}"

# Excluir nombres y dominios que se tienen tres caracteres iguales y consecutivos
exp4 = r"([a-zA-Z0-9])\1\1+"

# ------------ 3 ------------ TERCER NIVEL: Eliminar palabras claves

# Excluir palabras claves
term5 = ['www','root','mailer-daemon','deamon','donotreply', 'reply', 'web',
'info','robot','newsletter','postmaster','lista', 'domain', 'name', 'dmz', 'admin']
exp5 = r'(?:{})'.format('|'.join(map(re.escape, term5)))

# Excluir personas o empresas claves
term6 = ['name']
exp6 = r'(?:{})'.format('|'.join(map(re.escape, term6)))

# Excluir palabras que pudieran asociarse a algo ofensivo.
term7 = ['princesa', 'princess','king','kid','kids','sex',
'sexy','xxx','babe','porn','child','girl','boy','fuck',
'shit','sexo','sensual','bebe']
exp7 = r'(?:{})'.format('|'.join(map(re.escape, term7)))

# ------------ 4 ------------ CUARTO NIVEL: Corregir ortografía

# Corregir dominios hotmail mal escritos
term8 = ["@hot.", "@hmail.", "@htmail.", "@htmal.", 
"@hotmal.", "@hotmai.", "@homai.", "@otmail.", 
"@omail.", "@jotmail.", "@jotmal.", "@hotnail.", 
"@hotmial.", "@htomail.", "@htomial.", 
"@hotnial.", "@htonail.", "@htonial."]
exp8 = r'(?:{})'.format('|'.join(map(re.escape, term8)))

# Corregir dominos gmail mal escritos
term9 = ['@gma.','@gmi.','@gml.','@gmai.','@gmal.','@gmia.','@gmil.','@gmla.',
'@gmli.','@gami.','@gaml.','@gaim.','@gail.','@gmali.','@gmial.',
'@gmila','@gmlai.','@gmlia.','@gamil.','@gamli.','@gaiml.','@gailm.','@gimal.','@gnail.']
exp9 = r'(?:{})'.format('|'.join(map(re.escape, term9)))

# Corrgir dominios .com mal escritos.
term10 = ['@con.']
exp10 = r'(?:{})'.format('|'.join(map(re.escape, term10)))

#Ejecutar Nivel 4 - Corrección de Ortografías
df['Email address'].replace(regex=exp8,value='@hotmail.', inplace=True)
df['Email address'].replace(regex=exp9,value='@gmail.', inplace=True)
df['Email address'].replace(regex=exp10,value='@com.', inplace=True)

# Dominios .com con dominio internacional mal escritos

# ------------ 5 ------------ QUINTO NIVEL: Corregir parte del nombre



# ------------ 6 ------------ SEXTO NIVEL: Eliminar casos para reducir la base

# Excluir emails que tienen '- _' en el nombre del mail o dominio.
exp = r"^[A-Za-z0-9\.]+@[A-Za-z0-9\.]+\.[a-zA-Z]*$"

# Regla que excluye emails que tienen algún número en su nombre o dominio.
exp = r"^\w+@[a-zA-Z_]+?\.[a-zA-Z]{2,3}$"

# Eliminar dominios con menos de X emails.

# ----------------------------------------------------------
# Crea permutaciones de letras a partir de una palabra o conjunto de letras.
# ----------------------------------------------------------

""" from itertools import permutations
palabra = "hotmail"
def words(letters):
    for n in range(4,7):
        yield from map(''.join, permutations(letters, n))
variaciones = list(words(palabra))
 """

# ----------------------------------------------------------
# Funciones y procesos
# ----------------------------------------------------------

# ----------------------------------------------------------
# Conteo Incial por Grupos
# ----------------------------------------------------------

cg_origen = pd.DataFrame(df['filename'].value_counts()).sort_index()

# ----------------------------------------------------------
# Parametrizar la cantidad de RegEx a procesar
# ----------------------------------------------------------

# Lista de RegEx a procesar
reg_ex = [exp0,exp1,exp2,exp3,exp4,exp5,exp6,exp7]
#reg_ex = [exp0,exp1,exp2,exp3,exp4,exp5,exp6,exp7, exp8, exp9, exp10]

# Crear el nombre de las columnas a incorporar al df para guardar los valores bool
col_exp = []
nro = len(reg_ex)
for i in range(nro):
    col_exp.append(f"exp{i}")


# Ejecutar las RegEx. Itera la lista de "expresion", agrega la columna "exp(i)" y valida las exp.

for exp,valid in zip(reg_ex,col_exp):
    criterio = (df["Email address"].str.contains(exp))
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

# Eliminar duplicados
df.drop_duplicates(subset='Email address', keep='first', inplace=True)

# ----------------------------------------------------------
# Sumarización de df para contabilizar cantidades perdidas 
# ----------------------------------------------------------

# Cuenta los email por el grupo Filename 
cg_final = pd.DataFrame(df['filename'].value_counts()).sort_index()

# Merge de DF cg_ para comparar los casos perdidos
cg_global = cg_origen.merge(cg_final, left_index=True, right_index=True)

# Contiene Kupferman
df1 = df[df["Email address"].str.contains('solution-latam')]

# ----------------------------------------------------------
# exportar csv 
# ----------------------------------------------------------

path2 = 'C:/Users/AG/Documents/00 - Personales/solution/Emailing/Base Mail para Validar V2.csv'
df.to_csv(path2, index=False)

# ----------------------------------------------------------
# Renombrar columnas y dividir por caracter
# ----------------------------------------------------------
""" 
# Dividir por caracter
df['nombre'] = [x.split('@')[-0] for x in df['Email address']]

# Definir el orden de las columnas
df = df[['Email address', 'filename', 'nombre', 'domain', 'COD-1', 'COD-2', 'COD-3', 'COD-4']]

# Renombrar columna
df.rename(columns={'Email Address': 'email'}, inplace=True)

# Describir el df
df.describe()
 """