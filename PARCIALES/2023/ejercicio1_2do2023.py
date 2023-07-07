import sys
sys.path.append('PARCIALES')
import funciones_generales as f_g
import csv 

def opcion_1(materia:str,lista_datos:list):
    dict_pedido={'promedio': 0 , 'aprobados': [] , 'reprobados': [] } #{promedio: "..." , aprobados: "..." , reprobados: "..." }
    notas=list()
    for elemento in range(len(lista_datos)):
        print(lista_datos[elemento])
        if lista_datos[elemento][1][1::] == materia:
            nota=int(lista_datos[elemento][2])
            nombre=lista_datos[elemento][0]
            notas.append(nota)
            if nota >= 4:
                dict_pedido["aprobados"].append(nombre)
            elif 0 <= nota < 4:
                dict_pedido["reprobados"].append(nombre)

    suma_nota=0
    for nota in notas:
        suma_nota+=nota
    
    dict_pedido["promedio"]= suma_nota//len(notas)

    return dict_pedido

def intermediario_1(funcion,parametro):
    materia=input("Ingrese una materia: ")
    dict_pedido=funcion(materia,parametro)    
    print(dict_pedido)

def opcion_2(lista_datos:list):
    dict_pedido=dict()
    for elemento in lista_datos:
        if elemento[3] not in dict_pedido.keys():
            cuatrimestre=elemento[3]
            dict_pedido[cuatrimestre] = 0
    for cuatri in dict_pedido:
        acumulador=0
        for dato in lista_datos:
            nota= int(dato[2])
            c = dato[3]
            if nota >= 4 and c == cuatri :
                acumulador+=1
        dict_pedido[cuatri]=acumulador
    print(dict_pedido)

def opcion_3(lista_datos:list):
    lista_pedida_cuatri=list() # [ Materia, Cuatrimestre, Nota Promedio ]
    lista_pedida_materia=list()
    cuatris=list()
    materias=list()
    for elemento in lista_datos:
        cuatrimestre=elemento[3]
        materia=elemento[1]
        if cuatrimestre not in cuatris: 
            cuatris.append(cuatrimestre)
        if materia not in materias: 
            materias.append(materia)
    cuatris.sort()

    for cuatri in cuatris:
        for materia in materias:
            acumulador=0
            alumnos=0
            for dato in lista_datos:
                if cuatri == dato[3] and materia == dato[1]:
                    nota=int(dato[2])
                    acumulador+= nota
                    alumnos+=1
                    print(dato)
            if alumnos != 0 : promedio=acumulador//alumnos
            else : promedio=0
            print(promedio)
            lista_pedida_cuatri.append([materia,cuatri,promedio])
    
    for materia in materias:
        acumulador=0
        alumnos=0
        for cuatri in cuatris:
            for dato in lista_datos:
                if cuatri == dato[3] and materia == dato[1]:
                    nota=int(dato[2])
                    acumulador+= nota
                    alumnos+=1
                    print(dato)
            if alumnos != 0 : promedio=acumulador//alumnos
            else : promedio=0
            print(promedio)
            lista_pedida_materia.append([materia,cuatri,promedio])

    return lista_pedida_cuatri , lista_pedida_materia

def opcion_4(lista_datos:list,materia_usuario:str , materias:list):

    nombres=list()
    cuatris=list()
    for dato in lista_datos:
        cuatri=dato[3]
        if cuatri not in cuatris:
            cuatris.append(cuatri)
    cuatris.sort(reverse=False) #para al revez solamente hay que cambiar el parametro


    lista_datos_aux=list()
    for dato in lista_datos:
        lista_datos_aux.append(dato)
    for i in range(5):
        mejor_alumno=""
        nota_max=-1
        for dato in lista_datos_aux:
            nota=int(dato[2])
            alumno=dato[0]
            if dato[1][1::].lower() == materia_usuario and nota>nota_max and dato not in nombres:
                nota_max=nota
                mejor_alumno=alumno
                dato_max=dato
        nombres.append(dato_max)

    
    archive= open("PARCIALES/2023/materia.txt" , "w" , encoding="UTF-8" , newline="")
    for cuatri in cuatris:
        for nombre in nombres:
            if nombre[3] == cuatri:
                archive.write(",".join(nombre)+"\n")
    archive.close()

def intermediario_4(lista_datos:list):
    materias=list()
    for dato in lista_datos:
        materia_aux=dato[1][1::].lower()
        if materia_aux not in materias:
            materias.append(materia_aux)
    

    materia=input("Ingrese una materia: ").lower()
    while materia not in materias:
        materia=input("Ingrese una materia valida: ")

    opcion_4(lista_datos,materia,materias)

def procesar_datos():
    lista_pedida=list()
    try:
        archive = open ( "PARCIALES/2023/notas.csv" , "r" , encoding="UTF-8" , newline="")
        csv_reader = csv.reader(archive , delimiter=",")
        for linea in csv_reader:
            tupla=(linea[0],linea[1],linea[2],linea[3])
            lista_pedida.append(tupla)
        archive.close()
    except FileNotFoundError:
        print("Archivo no encontrado.")

    return lista_pedida


def main():
    lista_pedida=procesar_datos()
    menu={"a":("opcion_1", intermediario_1 , [opcion_1,lista_pedida]) , "b":("opcion_2", opcion_2 , [lista_pedida]) , "c":("opcion_3", opcion_3 , [lista_pedida]) , "d":("opcion_4", intermediario_4 , [lista_pedida])}
    f_g.ejecutar_menu(menu)

main()