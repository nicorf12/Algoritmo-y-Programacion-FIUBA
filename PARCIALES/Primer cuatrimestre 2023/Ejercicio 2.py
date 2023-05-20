def cantidad_salidas(cadena:str)->dict:
    dic={}
    trabajadores=cadena.split("||")
    trabajadores_list=[]
    for trabajador in trabajadores:
        trabajadores_list.append(trabajador.split(","))
    for trabajador2 in trabajadores_list:
        if trabajador2[0] not in dic.keys():
            dic[trabajador2[0]]=1
        else:
            dic[trabajador2[0]]+=1 
    return dic

def datos_x_cuil(cadena)->dict:

    cuil=input("Ingrese el cuil del trabajador que deseas la informacion: ")
    lista= list()
    trabajadores=cadena.split("||")
    for trabajador in range(len(trabajadores)):
        trabajadores[trabajador]=trabajadores[trabajador].split(",")
    for trabajador2 in trabajadores:
        if trabajador2[0] == cuil:
            lista.append(trabajador2)
    return lista

def no_cumple_horario(cadena):
    diccionario= dict()
    listado= list()
    trabajadores=cadena.split("||")
    for trabajador in range(len(trabajadores)):
        trabajadores[trabajador]=trabajadores[trabajador].split(",")
    for trabajador2 in trabajadores:
        if trabajador2[0] not in diccionario.keys():
            diccionario[trabajador2[0]]=[trabajador2[1],trabajador2[2], int(trabajador2[4])-int(trabajador2[3])]
        elif trabajador2[0] in diccionario.keys():
            diccionario[trabajador2[0]][2]+=int(trabajador2[4])-int(trabajador2[3])

    for trabajador3 in diccionario.keys():
        if diccionario[trabajador3][2] < 800:
            listado.append([diccionario[trabajador3][0],diccionario[trabajador3][1],diccionario[trabajador3][2]])
    return listado

# Sumo el siguiente bloque de código, para realizar pruebas
#
# @author Leonel Abel Chaves

def main() -> None:
    cadena: str = '20392194691, Leonel, Chaves, 0800, 1100||19392194602, Ramiro, Esperon, 0800, 1300||20392194691, Leonel, Chaves, 1200, 1700||18288658790, Guido, Costa, 0900, 1500'

    cantidad_de_salidas: dict = cantidad_salidas(cadena)

    
    datos: list = datos_x_cuil(cadena)

    datosv2 : dict = no_cumple_horario(cadena)

    print()


main()