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

    # El planteo viene encaminado, faltó filtrar por número de CUIL y
    # había que tener en cuenta que un empleado puede tener más de un
    # registro, por lo tanto, se deberá mostrar esa N cantidad de 
    # registros
    #
    # @author Leonel Abel Chaves

    dic={}
    trabajadores=cadena.split("||")
    trabajadores_list=[]
    for trabajador in trabajadores:
        trabajadores_list.append(trabajador.split(","))
    for trabajador2 in trabajadores_list:
        if trabajador2[0] not in dic.keys():
            dic[trabajador2[0]]=",".join(trabajador2[1:len(trabajador2)])
        else:
            dic[trabajador2[0]]+=","+",".join(trabajador2[3:len(trabajador2)])
    return dic  #llegue hacerlo con diccionarios, por el tiempo no lo pude hacer con listas


# Sumo el siguiente bloque de código, para realizar pruebas
#
# @author Leonel Abel Chaves

def main() -> None:
    cadena: str = '20392194691, Leonel, Chaves, 0800, 1100||19392194602, Ramiro, Esperon, 0800, 1300||20392194691, Leonel, Chaves, 1200, 1700||18288658790, Guido, Costa, 0900, 1500'

    cantidad_de_salidas: dict = cantidad_salidas(cadena)

    datos: dict = datos_x_cuil(cadena)

    print()


main()