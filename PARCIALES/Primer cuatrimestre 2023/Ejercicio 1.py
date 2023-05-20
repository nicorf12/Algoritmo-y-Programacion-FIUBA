def cargar_asistencia_nueva(asistencias,moviles_disp):
    fecha=input("Ingrese fecha de llamado: ")
    dominio=input("Ingrese dominio del vehiculo a asistir: ")
    tipo_vehiculo=input("Ingrese el tipo de dicho vehiculo: ")
    origen=input("Ingrese la direccion de origen: ")
    tipo_asistencia=input("Ingrese el tipo de asistencia: ")
    prioridad=input("Ingrese prioridad: ")
    #mostrar lista de moviles disponiles
    moviles_posibles=[]
    for movil in moviles_disp:
        if movil[1]==tipo_asistencia.lower():
            moviles_posibles.append(movil[0])
    print(moviles_posibles)
    movil_rescate=input("Ingrese que movil ira a sistirlo: ")
    if tipo_asistencia.upper()=="REMOLQUE":
        destino=input("Ingrese la direccion de destino: ")
    else:
        destino=origen
    tiempo=input("Ingrese tiempo estimado de servicio: ")
    valor=input("Ingrese el valor del servicio: ")

    moviles_disp[int(movil_rescate)-1][2]+=1

    if dominio not in asistencias.keys():
        asistencias[dominio]=(fecha,tipo_vehiculo,origen,destino,tipo_asistencia,tiempo,prioridad,movil_rescate,valor)
        #(0 fecha , 1 tipo de vehiculo , 2 origen , 3 destino , 4 tipo de asistencia , 5 tiempo estimado , 6 prioridad , 7 movil que ira , 8 valor)

def finalizar_servicio(asistencias_totales,finalizados):
    dominio_finalizado=input("indique el dominio del vehiculo que iba a ser asistido: ")
    if dominio_finalizado in asistencias_totales.keys():
        finalizados[dominio_finalizado]=asistencias_totales[dominio_finalizado]
    
def agregar_movil(moviles):
    tipo_asistencia=input("Ingrese que tipo de asistencia debe el nuevo movil: ")
    moviles.append([str(len(moviles)+1),tipo_asistencia.lower()])
    print(moviles)

def listado_finalizados(finalizados):
    fecha=input("ingrese la fecha del dia que quiere la lista: ")
    movil=input("ingrese el movil que quiere la lista: ")
    valor=0
    veces=0
    for asistencia in finalizados:
        if finalizados[asistencia][0]==fecha and finalizados[asistencia][7]==movil:
            print(f" el movil {asistencia} realizo {finalizados[asistencia]}")
            valor+=finalizados[asistencia][8]
            veces+=1
    print(f"el movil {movil} presto {veces} servicios en el dia {fecha} y su valor en ese dia fue de {valor}$")

def tiempo_promedio(asistencias_totales):
    contador=0
    n=len(asistencias_totales)
    for asistencia in asistencias_totales:
        contador+=int(asistencias_totales[asistencia][5])
    
    if contador != 0:
        print(f"el promedio en minutos es: {contador/n}")
    else:
        print("no hubieron asistencias hasta el momento")

def movil_mas_servicios(moviles):
    max=moviles[0][2]
    for movil in moviles:
        if movil[2]>=max:
            max=movil[2]
            aux=movil
    print(f"el movil que mas servicios presto fue {aux}")

def porcentaje_asistencia(finalizados): #4
    n_remolque=0
    n_mecanica=0
    n=len(finalizados.items())
    for asistencia in finalizados:
        if finalizados[asistencia][4].lower()=="remolque":
            n_remolque+=1
        elif finalizados[asistencia][4].lower()=="mecanica":
            n_mecanica+=1
    print(f"el promedio de remolque fue: {(n_remolque*100)/n}%")
    print(f"el promedio de mecanica fue: {(n_mecanica*100)/n}%")

def porcentaje_tipo_vehiculo(asistencias_totales): #1
    n_auto=0
    n_camion=0
    n_moto=0
    n_camioneta=0
    n=len(asistencias_totales.items())

    for asistencia in asistencias_totales:
        if asistencias_totales[asistencia][1].lower()=="auto":
            n_auto+=1
        elif asistencias_totales[asistencia][1].lower()=="camion":
            n_camion+=1
        elif asistencias_totales[asistencia][1].lower()=="moto":
            n_moto+=1
        elif asistencias_totales[asistencia][1].lower()=="camioneta":
            n_camioneta+=1

    print(f"El promedio de autos es de: {(n_auto*100)/n}%")
    print(f"El promedio de camiones es de: {(n_camion*100)/n}%")
    print(f"El promedio de motos es de: {(n_moto*100)/n}%")
    print(f"El promedio de camionetas es de: {(n_camioneta*100)/n}%")

def main():

    moviles_disponiles=[["1","mecanica",0],["2","mecanica",0],["3","remolque",0],["4","remolque",0]]
    asistencias_totales={}
    finalizados={}
    print("~~Menu~~ \n a -> Cargar nueva asistencia")
    condicion=True
    while condicion:
        eleccion=input("que desea hacer?")
        if eleccion=="a":

            # Está OK, se podría haber sumado la validación de que el usuario no ingrese
            # un móvil inexistente
            #
            # @author Leonel Abel Chaves

            cargar_asistencia_nueva(asistencias_totales,moviles_disponiles)
        elif eleccion=="b":

            # Está OK
            #
            # @author Leonel Abel Chaves

            finalizar_servicio(asistencias_totales,finalizados)
        elif eleccion=="c":

            # Está OK
            #
            # @author Leonel Abel Chaves

            agregar_movil(moviles_disponiles)
        elif eleccion=="d":

            # Está OK
            #
            # @author Leonel Abel Chaves

            listado_finalizados(finalizados)
        elif eleccion=="e":

            # El planteo está OK, pero se está generando un error al intentar
            # recorrer el diccionario, ya que 'asistencia' termina siendo la llave
            # del diccionario
            #
            # @author Leonel Abel Chaves

            tiempo_promedio(asistencias_totales)
        elif eleccion=="f":

            # Esta OK, la única sugerencia vendría a ser en que en vez de usar un número
            # absurdamente grande o pequeño para hacer las comparaciones, se use un valor 
            # perteneciente al set de datos, para evitar falsos positivos
            #
            # @author Leonel Abel Chaves

            movil_mas_servicios(moviles_disponiles)
        elif eleccion=="g":

            # Idem punto e)
            #
            # @author Leonel Abel Chaves

            porcentaje_asistencia(finalizados)
        elif eleccion=="h":

            # Idem punto e)
            #
            # @author Leonel Abel Chaves

            porcentaje_tipo_vehiculo(asistencias_totales)
        elif eleccion=="i":
            condicion=False

main()


# Python - E1 a) OK (1.0 pts)
#             b) OK (0.5 pts)
#             c) OK (1.0 pts)
#             d) OK (1.0 pts)
#             e) OK- (0.25 pts)
#             f) OK (1.0 pts)
#             g) OK- (0.75 pts)
#             h) OK- (0.75 pts)
#
#          E2 a) OK (1.0 pts)
#             b) No se llegó a plantear (0.0 pts)
#             c) OK- (0.75 pts)
#
#          Acumulado: 8.0 - Apreciación general: 8.5
#
# Observaciones: - Faltó definir el typing en las firmas de las funciones
#
# @author Leonel Abel Chaves 
