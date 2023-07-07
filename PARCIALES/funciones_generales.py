import csv
import json

import os

def ejecutar_menu(opcciones:dict): #{'indice': ('frase' , 'nombre de la funcion', (parametros) )}
    for indice in opcciones.keys():
        print(f"{indice} .- {opcciones[indice][0]}")

    eleccion_usuario=input("Ingrese la opccion deseada: ").lower()
    while eleccion_usuario not in opcciones.keys():
        eleccion_usuario=input("Ingrese una opccion valida: ").lower()
    
    
    os.system("cls")

    parametros=opcciones[eleccion_usuario][2]
    if len(parametros) == 0:
        vuelta=opcciones[eleccion_usuario][1]()
    elif len(parametros) == 1:
        primer_parametro=parametros[0]
        vuelta=opcciones[eleccion_usuario][1](primer_parametro)
    elif len(parametros) == 2:
        primer_parametro=parametros[0]
        segundo_parametro=parametros[1]
        vuelta=opcciones[eleccion_usuario][1](primer_parametro,segundo_parametro)
    elif len(parametros) == 3:
        primer_parametro=parametros[0]
        segundo_parametro=parametros[1]
        tercer_parametro=parametros[2]
        vuelta=opcciones[eleccion_usuario][1](primer_parametro,segundo_parametro,tercer_parametro)
    
    
    if vuelta==None:
        vuelta=True
    
    return vuelta

#prueba de como funciona

""""
def imprimir_hola(cadena):
    print(f"{cadena}")  

prueba={"a": ( "hola" , imprimir_hola, ["funciona"] )}

ejecutar_menu(prueba)
"""

def menu_estatico(opcciones:dict):
    for indice in opcciones.keys():
        print(f"{indice} .- {opcciones[indice]}")

    eleccion_usuario=input("Ingrese la opccion deseada: ").lower()
    while eleccion_usuario not in opcciones.keys():
        eleccion_usuario=input("Ingrese una opccion valida: ").lower()
    
    return ejecutar_menu

def leer_archivo(archivo:str,tipo:str,delimitador:str=',')->list:
    try:
        archive=open(archivo,"r",encoding="UTF-8",newline='')
    except IOError:
        print("No se encontro el archivo.")
    except:
        print("Ha pasado algo inusual.")
    else:
        if tipo=="csv":
            datos=list()
            csv_reader = csv.reader(archive, delimiter=delimitador)
            next(csv_reader)
            for row in csv_reader:
                datos.append(row)
            archive.close()
            return datos
        elif tipo=="json":
            dciccionario = json.loads(archive)
            archive.close()
            return dciccionario
        elif tipo=="txt":
            datos_txt=archive.readlines()
            for dato in range(len(datos_txt)):
                datos_txt[dato]=datos_txt[dato].strip('\n').split(delimitador)
            archive.close()
            return datos_txt

def escribir_muchas_lineas_csv(archivo:str,lineas,delimitador:str=","):
    archive=open(archivo , "w" ,encoding="UTF-8",newline='')
    csv_writer=csv.writer(archive,delimiter=delimitador)
    csv_writer.writerow(lineas)
    archive.close()

def escribir_muchas_lineas_txt(archivo:str,lineas,delimitador:str=","): 
    archive=open(archivo , "w" ,encoding="UTF-8",newline='')
    for linea in lineas:
        print(linea)
        archive.write(f"{delimitador}".join(linea) + "\n")

#prueba de como se usa
#escribir_muchas_lineas_txt("hola.txt", [["hola,como,te,va"],["que,tal,co"]])

def escribir_json(archivo:str,diccionario:dict):
    predicado=json.dumps(diccionario,indent=3)
    archive=open(archivo , "w" , encoding="UTF-8" ,newline="")
    archive.write(predicado)
    archive.close()

#porueba de como se usa
#escribir_json("hola.json", {"hola":"yo" , "p" : "q"})

def filtrar(datos:list,posicion_parametro:int):
    filtro=list()
    for dato in datos:
        parametro=dato[posicion_parametro]
        if parametro not in filtro:
            filtro.append(parametro)
    return filtro

#como se usa
#muñecos=leer_archivo("muñecos.csv","csv")
#medicos=filtrar(muñecos,4)
#print(medicos)

#suma todos los elementos de una lista -> sum(lista)
#maximo de una lista -> max(lista)
#minimo de una lista -> min(lista)
#mi_texto.split(separador) -> de texto a lista
#f"{separador}".join(lista) -> de lista a texto