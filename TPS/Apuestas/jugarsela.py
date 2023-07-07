from passlib.hash import sha256_crypt
import http.client
import json
import matplotlib.pyplot as plt
import csv
import os
import random
import time

#-----------------------------
#---------respuestass---------
#-----------------------------

def procesar_datos(res)->dict:
    data = res.read()
    data.decode("utf-8")
    return json.loads(data)

def pedir_respuesta(**kwargs)->dict:
    """0 devuelve datos del partido, 1 devuelve partidos habiles, 2 devuelve la prediccion de un partido, 3 devuelve goles por minuto de un equipo
    4 devuelve la tabla de la temporada, 5 devuelve los jugadores de un equipo y 6 devuelve informacion de un equipo"""
    conn = http.client.HTTPSConnection("v3.football.api-sports.io")

    headers = {
        'x-rapidapi-host': "v3.football.api-sports.io",
        'x-rapidapi-key': ""
        }
    
    if kwargs["selector"]== 0:
        id_partido=kwargs["id_partido"]
        conn.request("GET", f"/fixtures?id={id_partido}", headers=headers)
        datos=procesar_datos(conn.getresponse())
        datos_partido = datos["response"]
        return datos_partido
    
    elif kwargs["selector"]==1:
        equipo=kwargs["equipo"]
        conn.request("GET", f"/fixtures?league=128&season=2023&team={equipo}&status=NS", headers=headers)

        datos=procesar_datos(conn.getresponse())
        datos_partido=datos["response"]
        return datos_partido 
    
    elif kwargs["selector"]== 2:
        id_partido=kwargs["id_partido"]
        conn.request("GET", f"/predictions?fixture={id_partido}", headers=headers)
        datos=procesar_datos(conn.getresponse())
        return datos["response"][0]["predictions"]["winner"]["id"]
    
    elif kwargs["selector"]== 3:
        id_equipo=kwargs["id_equipo"]
        conn.request("GET", f"/teams/statistics?season=2023&team={id_equipo}&league=128", headers=headers)
        datos=procesar_datos(conn.getresponse())
        print(datos)
        gols_x_min = datos["response"]["goals"]["for"]["minute"]
        return gols_x_min
    
    elif kwargs["selector"]== 4:
        conn.request("GET", "/standings?league=128&season=2023", headers=headers)
        datos=procesar_datos(conn.getresponse())
        posiciones = datos["response"][0]["league"]["standings"][1]
        return posiciones
    
    elif kwargs["selector"]== 5:
        key=kwargs["key"]
        conn.request("GET", f"/players/squads?team={key}", headers=headers)
        datos=procesar_datos(conn.getresponse())
        jugadores=datos["response"][0]["players"]
        return jugadores
    
    elif kwargs["selector"]== 6:
        key=kwargs["key"]
        conn.request("GET", f"/teams?id={key}", headers=headers)
        datos=procesar_datos(conn.getresponse())
        return datos

#-----------------------------
#--------validacioness--------
#-----------------------------

def verificar(tal:str,cual:int)->bool:
    """0 para verificar mails y 1 para verificar nombres"""
    with open('usuarios.csv',encoding='utf8') as f:
        reader = csv.reader(f, delimiter=";")
        for row in reader:
            if tal == row[cual]:
                return True
    return False

def ver_contra(name:str,passw:str)->bool:
    autentificador=False
    with open('usuarios.csv',encoding='utf8') as f:
        reader = csv.reader(f, delimiter=";")
        for row in reader:
            if name== row[1] and sha256_crypt.verify(passw,row[2]):    ##passw == row[2]:
                autentificador=True
    return autentificador

def validar_equipo(equipo_user:str,equipos:dict)->bool:
    for equipo in equipos:
        if equipos[equipo].lower()==equipo_user.lower():
            return True
    return False

def validar_numero_positivo_coherente(numero:str,numero_comparacion:int)->bool:
    if numero.isdigit():
        numero=int(numero)
        if numero > 0:
            if numero<=numero_comparacion:
                return True
    return False

def validacion_id_partido(id:str,dict_partidos:dict)->bool:
    if id.isdigit():
        id=int(id)
        if id in dict_partidos.keys():
            return False
    return True

#-----------------------------
#--------sist.usuarios--------
#-----------------------------
def registracion()->str:
    ingreso = input("¿Tiene cuenta usted en nuestro sistema? (si/no): ").upper()
    while (ingreso !="SI") and (ingreso !="NO"):
        ingreso = input("opción inválida, por favor intente nuevamente: ").upper()
    return ingreso

def registrar(usuario_en_linea:dict)->None:
    print("para poder acceder a nuestra aplicacion, debera tener una cuenta, lo invito a registrarse.")
    with open('usuarios.csv', '+a', newline='') as f:
        print("ingrese los siguientes datos:  ")
        condicion = True
        while condicion :
            mail = input("mail:  ") ##verifico que no exista el mail en usuarios.csv
            nombre = input("nombre del usuario:  ")
            if verificar(mail,0) or verificar(nombre,1):
                print(f'el mail o username ya se encuentra registrado, intente nuevamente')
            else:    
                contra = input("ingrese una contraseña:  ")
                password = sha256_crypt.encrypt(contra)
                lista = [mail,nombre,password,0,"no se han hecho apuestas",0] # [mail,nombre,pw(encriptada),cantidad apostada hasta el momento, ulltima apuesta, dinero disponible]
                writer = csv.writer(f,delimiter=';')
                writer.writerow(lista)
                condicion = False
                print('ha sido registrado exitosamente, escriba su usuario y contraseña nuevamente para ingresar al sistema')    
            
def ingreso(usuario_en_linea:dict)->int:
    k=0
    while k < 3:
        mail = input('ingrese su mail: ')
        nombre = input('ingrese su nombre de usuario: ')
        contra = input('ingrese su contaseña: ')
        if verificar(nombre,1) and ver_contra(nombre,contra) and verificar(mail,0):
            print('ha ingresado al sistema')
            usuario_en_linea["mail"]=mail
            usuario_en_linea["usuario"]=nombre
            k = 4
        else:
            k+=1
            print(f'usuario y/o contraseña incorrectos, le quedan {(3-k)} intentos ')
    return k #si k=4 entro al sistema

def contador_dinero(mail:str)->int:
    f = open('usuarios.csv','r',newline='\n')
    reader = csv.reader(f,delimiter = ';')
    dinero = 0
    for row in reader:
        if row[0] == mail:
            dinero = int(row[5])
    f.close()
    return dinero

def ingresar_dinero(en_linea:dict)->None:
    nueva = []
    cant_str = input("Escriba la cantidad de dinero que desea ingresar: ")
    validacion = cant_str.isdigit()
    while not validacion:
        cant_str = input("Por favor, ingrese solo números. Intente de nuevo: ")
        validacion = cant_str.isdigit()
    cant = int(cant_str)
    f = open('usuarios.csv','r',newline='\n')
    reader = csv.reader(f,delimiter = ';')
    for row in reader:
        nueva.append(row)
        if en_linea["usuario"] == row[1]:
            dinero_actualizado = int(row[5]) + cant
            nueva[nueva.index(row)][5] = dinero_actualizado
    f.close()
    f = open('usuarios.csv','w',newline='\n')
    writer = csv.writer(f, delimiter = ';')
    writer.writerows(nueva)
    f.close()

    transacciones= open("transacciones.csv" , "a" , encoding="UTF-8",newline='')
    csv_writer = csv.writer(transacciones, delimiter=',',)
    aux=[en_linea["mail"],time.strftime("%d/%m/%y"),"ingreso",cant]
    csv_writer.writerow(aux)    
    transacciones.close()
    print(f"Ingreso de ${cant} exitoso.")
    
    return dinero_actualizado

#-----------------------------
#--------mostrar_cosas--------
#-----------------------------

#--equipos--

def mostrar_equipos(equipos:dict):
    print("--EQUIPOS--")
    for equipo in equipos:
        print(f"{equipos[equipo]}")

#--usuario que mas aposto--

def usuario_mas_timbero()->None:
    with open('usuarios.csv') as f:
            reader = csv.reader(f,delimiter= ';')
            comparador = 0
            usuarios_mas_timberos=list()
            usuario_apostador = 'nombre'
            for row in reader:
                row[3]= int(row[3])
                if row[3] >= comparador:
                        comparador = row[3]
                        usuario_apostador = row[1]
                        if usuario_apostador not in usuarios_mas_timberos:
                            usuarios_mas_timberos.append(usuario_apostador)
            if comparador != 0 and len(usuarios_mas_timberos) == 1:
                print(f'el usuario que más apostó fue {usuario_apostador} con un total de ${comparador}')
            elif comparador != 0 and len(usuarios_mas_timberos) > 1:
                print(f"los usuarios con mas apuestas hechas fueron (${comparador}):")
                for usuario in usuarios_mas_timberos:
                    print(usuario)
            elif comparador==0:
                print('aun no hubieron apuestas')

#--tabla de temporada 2023--

def mostrar_tabla()->None:
    posiciones=pedir_respuesta(selector=4)
    cont = 0
    for i in range(len(posiciones)):
        cont +=1
        print(f' {cont} - {posiciones[i]["team"]["name"]}')

#--plantel x equipo--

def mostrar_plantel_equipo(equipos:dict)->None:
    mostrar_equipos(equipos)
    user = input("Ingrese el nombre de un equipo para obtener su plantel: ")
    while not validar_equipo(user,equipos):
        user = input("Ingrese un equipo valido: ")

    for equipo in equipos:
        if equipos[equipo].lower()==user.lower():
            key=equipo
    
    datos = pedir_respuesta(selector=5,key=key)
    
    for dic in datos:
        nombre = dic["name"]
        posicion = dic["position"]
        numero = dic["number"]
        edad = dic ["age"]
        print(f"{numero} - {nombre} - {posicion} - {edad} años de edad")

#--info x equipo--

def mostrar_info_equipo(equipos:dict)->None:
    mostrar_equipos(equipos)
    user = input("Ingrese el nombre de un equipo para obtener su informacion: ")
    while not validar_equipo(user,equipos):
        user = input("Ingrese un equipo valido: ")

    for equipo in equipos:
        if equipos[equipo].lower()==user.lower():
            key=equipo
            
    datos=pedir_respuesta(selector=6,key=key)

    id = datos["response"][0]["team"]["id"]
    name = datos["response"][0]["team"]["name"]
    code = datos["response"][0]["team"]["code"]
    country = datos["response"][0]["team"]["country"]
    founded = datos["response"][0]["team"]["founded"]
    logo = datos["response"][0]["team"]["logo"]
    estadio = datos["response"][0]["venue"]["name"]
    direccion = datos["response"][0]["venue"]["address"]
    ciudad = datos["response"][0]["venue"]["city"]
    capacidad = datos["response"][0]["venue"]["capacity"]
    imagen_estadio = datos["response"][0]["venue"]["image"]
    print(f"PLANTILLA DE {user}")
    print(f"Id del Equipo: {id}")
    print(f"Nombre del Equipo: {name}")
    print(f"Codigo del Equipo: {code}")
    print(f"Pais del Equipo: {country}")
    print(f"Fecha de fundacion del Equipo: {founded}")
    print(f"Logo del Equipo: {logo}")
    print(f"Estadio del Equipo: {estadio}")
    print(f"Direccion del Estadio: {direccion}")
    print(f"Ciudad del Estadio: {ciudad}")
    print(f"Capacidad del Estadio: {capacidad}")
    print(f"Imagen del Estadio: {imagen_estadio}")
    
#--usuario q' mas veces gano--

def mostrar_suertudo()->None:
    listado=dict() #{mail : veces que gano}
    if os.path.exists('transacciones.csv'):
        transcciones = open("transacciones.csv","r",newline='', encoding="UTF-8")
        csv_reader = csv.reader(transcciones, delimiter=',')
        for linea in csv_reader:
            if linea[0] not in listado.keys() and linea[2]=="gano":
                listado[linea[0]]=1
            elif linea[0] in listado.keys() and linea[2]=="gano":
                listado[linea[0]]+=1
        transcciones.close()
        max=-1
        for key in listado:
            if listado[key] > max:
                max = listado[key]
                mail_suertudo=key
            
        if len(listado.keys()) == 0:
            print(f"no hubo ningun usuario ganador hasta el momento")
        else:
            print(f"el usuario que mas gano fue {mail_suertudo}")
    else:
        print("Aun no hubieron apuestas de ningun usuario")
  
#-----------grafico-----------

def mostrar_grafico(equipos:dict)->None:
    mostrar_equipos(equipos)
    equipo_nombre=input("¿De cual equipo deseas ver el grafico?: ")
    while not validar_equipo(equipo_nombre,equipos):
        equipo_nombre=input("Ingresa un equipo valido: ")

    for equipo in equipos:
        if equipos[equipo].lower()==equipo_nombre.lower():
            id_equipo=equipo

    gols_x_min = pedir_respuesta(selector=3,id_equipo=id_equipo)
    gols_dict = dict()
    for key in gols_x_min:
        goals= gols_x_min[key]["total"]
        if gols_x_min[key]["total"] == None:
            goals = 0
        gols_dict[key]= goals
        #print(f"minuto - {key} ; {goals} goals")

    goles = list(gols_dict.values())
    minutos = list(gols_dict.keys())
    plt.bar(minutos,goles)
    plt.show()

#-----------------------------
#----------apuestass----------
#-----------------------------

def empezar_apuesta(equipos:dict,en_linea:dict,transacciones:list=[],usuario:list=[0,""])->list:
    monto_disponible = en_linea["monto_disponible"]
    
    #######esto sirve para obtener la id del equipo que quiere apostar el usuario
    mostrar_equipos(equipos)
    equipo=input("¿Por que equipo deseas apostar?: ")
    while not validar_equipo(equipo,equipos):
        equipo=input("Ingresa un equipo valido: ")
    print("\n~~~~~~~~~~~~~~~~~~~~~~~~\n")
    for item in equipos:
        if equipos[item].lower()==equipo.lower():
            equipo_id=item
    
    #######esto sirve para obtener la id del partido en donde el usuario desea apostar y algunas variables importantes
    id_partido, dado_porcentaje,w_o_d,not_w_o_d=mostrar_fixture(equipo_id,equipos)
    partido = pedir_respuesta(selector=0, id_partido=id_partido)
    
    local = partido[0]["teams"]["home"]["name"]
    visitante = partido[0]["teams"]["away"]["name"]
    fecha = partido[0]["fixture"]["date"]
    
    print(f"{local} (L) vs {visitante} (V)")
    print(f"              -- UTC: -- \n Fecha: {fecha[0:10]} -- Hora: {fecha[11::]} ")
    print(f"Pago de apuestas para este partido:\nSi gana {equipos[w_o_d]}, ganaras {dado_porcentaje/10} veces lo apostado")
    print(f"Si gana {equipos[not_w_o_d]}, ganaras {dado_porcentaje} veces lo apostado")
    print(f"Si empatan ganaras 0.5 veces lo apostado")
    
    #######esto sirve para darle a elegir su prediccion al usuario y la cantidad que esta dispuesto a perder
    
    eleccion_usuario = input("¿Quien ganara el partido?¿O sera un empate? (1:Gana L, 2:EMPATE, 3: Gana V) -> ")
    while (not validar_numero_positivo_coherente(eleccion_usuario,3)) or ((eleccion_usuario!="1") and (eleccion_usuario!="2") and (eleccion_usuario!="3")):
        eleccion_usuario = input("Por favor ingrese una opccion valida (1:Gana L, 2:EMPATE, 3: Gana V) -> ")
    eleccion_usuario = int(eleccion_usuario)

    print(f"monto disponible: ${monto_disponible}")
    monto_apostado = input("¿Que monto ingresaras?: ")
    while not validar_numero_positivo_coherente(monto_apostado,monto_disponible):
        monto_apostado=input("Por favor ingrese un monto valido:")
    monto_apostado=int(monto_apostado)
    
    #######esto sirve para simular el resultado del partido
    
    
    ganador = simulacion(local,visitante)
    operacion,monto_ganado = comprobacion(eleccion_usuario,ganador,local,visitante,monto_apostado,w_o_d,not_w_o_d,dado_porcentaje,equipos)
    
    if ganador != "empate":
        print(f"Como gano {ganador}, usted {operacion} {monto_ganado}$")
    else:
        print(f"Como fue un empate, usted {operacion} {monto_ganado}$")
    
    #######esto sirve para brindarle la oportunidad al usuario de realizar apuestas seguidas y cargar los datos todos juntos ( asi no reescribimos los archivos en cada apuesta )
    
    en_linea["monto_disponible"] += monto_ganado
    
    pregunta=input("¿Desea hacer otra apuestas?: ")
    aux = [en_linea["mail"],time.strftime("%d/%m/%y"),operacion,monto_ganado]
    transacciones.append(aux)
    usuario[0]+=monto_apostado             #usuario=[cantidad total apostada , fecha de la ultima apuesta]
    usuario[1]=time.strftime("%d/%m/%y")
    if pregunta.upper()=="SI":
        empezar_apuesta(equipos,en_linea,transacciones,usuario)

    
    return transacciones, usuario          

def mostrar_fixture(id_equipo:int,equipos:dict)->tuple:
    response=pedir_respuesta(selector=1,equipo=id_equipo)
    info_fixture={} # {[(dado),win_of_drawn,not_win_of_draw]} la funcion de este diccionario es guardar la informacion del fixture que elija el usuario
    for partido in response:
        #guardamos variables importantes
        id=partido["fixture"]["id"]
        fecha=partido["fixture"]["date"]
        estadio=partido["fixture"]["venue"]["name"]
        ciudad=partido["fixture"]["venue"]["city"]
        liga=partido["league"]["name"]
        round=partido["league"]["round"]
        local=partido["teams"]["home"]["name"]
        visitante=partido["teams"]["away"]["name"]
        win_of_draw=pedir_respuesta(selector=2,id_partido=id) #win of draw posee la id del team que posee esta propiedad
        
        #obtenermos las id's correspondientes a local y visitante
        for id_team in equipos:
            if equipos[id_team]==local:
                local_id=id_team
            if equipos[id_team]==visitante:
                visitante_id=id_team
        #obtenemos la id del not_w_o_d
        if win_of_draw == local_id:
            not_win_of_draw=visitante_id
        elif win_of_draw == visitante_id:
            not_win_of_draw=local_id
        

        info_fixture[id]=[random.randint(1,4),win_of_draw,not_win_of_draw] #el diccionario tendra la informacion de cada partido mostrado en pantalla

        print(f"Partido {round} de la liga {liga} con la id {id} juega el dia {fecha[0:10]} a las {fecha[11::]} (Horario UTC) \n {local}(L) y {visitante}(V) \n Estadio {estadio} / {ciudad}\n")
        print(f"Pago de apuestas para este partido\n Si gana  {equipos[not_win_of_draw]}, ganaras {info_fixture[id][0]} veces lo apostado\n")
        print(f"Pago de apuestas para este partido\n Si gana {equipos[win_of_draw]}, ganaras {info_fixture[id][0]/10} veces lo apostado\n")
    
    print(f"ID'S VALIDAS ")
    for id in info_fixture:
        print(id)
    
    id_partido=input("Ingrese la ID del partido: ")
    while validacion_id_partido(id_partido,info_fixture):
        id_partido=input("Ingrese una ID valida: ") 
    id_partido=int(id_partido)

    dado_porcentaje=info_fixture[id_partido][0]
    w_o_d=info_fixture[id_partido][1]
    not_w_o_d=info_fixture[id_partido][2]
    
    return id_partido, dado_porcentaje,w_o_d,not_w_o_d

def simulacion(local:str,visitante:str)->str: 
    
    dado_simulacion=random.randint(1,3)

    if dado_simulacion == 1:
        ganador=local
    elif dado_simulacion == 2:
        ganador="empate"
    elif dado_simulacion == 3:
        ganador=visitante
    
    return ganador
    
def comprobacion(eleccion_usuario:int,ganador:str,local:str,visitante:str,monto_apostado:int,w_o_d:int,not_w_o_d:int,dado_porcentaje:int,equipos:dict)->tuple:
    
    if (eleccion_usuario == 1 and ganador == local) or (eleccion_usuario == 2 and ganador == "empate") or (eleccion_usuario== 3 and ganador == visitante) :
        operacion="gano"
        if ganador==equipos[w_o_d]:#win_of_draw
            monto_ganado=monto_apostado*dado_porcentaje/10
        elif ganador==equipos[not_w_o_d]:#not_win_of_draw
            monto_ganado=monto_apostado*dado_porcentaje
        elif ganador=="empate":
            monto_ganado= monto_apostado/2
    else:
        operacion="perdio"
        monto_ganado=-monto_apostado
    return operacion, int(monto_ganado)

def cargar_datos(apuestas:list,data_usuario:list,en_linea:dict)->None:
    if not os.path.exists('transacciones.csv'):
        transacciones=open('transacciones.csv',"w",encoding="UTF-8",newline='')
        csv_writer = csv.writer(transacciones, delimiter=',',)
        for i in range(len(apuestas)):
            csv_writer.writerow(apuestas[i])
        transacciones.close()
    else:
        datos_t=list()
        lector=open("transacciones.csv","r",encoding="UTF-8",newline='')
        csv_reader=csv.reader(lector,delimiter=',')
        for linea in csv_reader:
            datos_t.append(linea)
        lector.close()
        transacciones=open('transacciones.csv',"w",encoding="UTF-8",newline='')
        csv_writer = csv.writer(transacciones, delimiter=',',)
        for j in range(len(datos_t)):
            csv_writer.writerow(datos_t[j])
        
        for i in range(len(apuestas)):
            csv_writer.writerow(apuestas[i])
        transacciones.close()
    
    datos_u=list()
    lector=open("usuarios.csv","r",encoding="UTF-8",newline='')
    csv_reader=csv.reader(lector,delimiter=';')
    for linea in csv_reader:
        if linea[0]==en_linea["mail"]: #data_usuario[0]:
            linea[3]=int(linea[3])+data_usuario[0]
            linea[4]=data_usuario[1]
            linea[5]=en_linea["monto_disponible"]
        datos_u.append(linea)
    lector.close()
    usuarios=open('usuarios.csv',"w",encoding="UTF-8",newline='')
    csv_writer = csv.writer(usuarios, delimiter=';',)
    for k in range(len(datos_u)):
        csv_writer.writerow(datos_u[k])
    usuarios.close()

def main():
    equipos = {434: 'Gimnasia L.P.', 435: 'River Plate', 436: 'Racing Club', 437: 'Rosario Central', 438: 'Velez Sarsfield', 439: 'Godoy Cruz', 440: 'Belgrano Cordoba', 441: 'Union Santa Fe', 442: 'Defensa Y Justicia', 445: 'Huracan', 446: 'Lanus', 448: 'Colon Santa Fe', 449: 'Banfield', 450: 'Estudiantes L.P.', 451: 'Boca Juniors', 452: 'Tigre', 453: 'Independiente', 455: 'Atletico Tucuman', 456: 'Talleres Cordoba', 457: 'Newells Old Boys', 458: 'Argentinos JRS', 459: 'Arsenal Sarandi', 460: 'San Lorenzo', 474: 'Sarmiento Junin', 478: 'Instituto Cordoba', 1064: 'Platense', 1065: 'Central Cordoba de Santiago', 2432: 'Barracas Central'}
    en_linea = {"mail":"","usuario":"","monto_disponible":0}
    cerrado = True
    print("TEMPORADA 2023 LIGA ARGENTINA")
    while cerrado:
        menu=""
        registro = registracion()
        if registro == "NO":
            registrar(en_linea)
        if ingreso(en_linea) == 4:
            input("~~ingrese una tecla cualquiera para continuar~~") #input meramente para que el usuario pueda leer
            os.system("cls")
            print("--INICIO--")
            en_linea["monto_disponible"] = contador_dinero(en_linea["mail"])
            while menu.lower() !="a":
                print(" a.- CERRAR SESION \n b.- INGRESAR DINERO \n c.- MOSTRAR AL USUARIO QUE MAS APOSTO \n d.- MOSTRAR TABLA DE EQUIPOS DE LA TEMPORADA \n e.- MOSTRAR EL PLANTEL DE UN EQUIPO \n f.- MOSTRAR LA INFORMACION DE UN EQUIPO \n g.- MOSTRAR AL USUARIO QUE MAS GANO \n h.- MOSTRAR GRAFICO DE GOLES POR MINUTO DE UN EQUIPO \n i.- APOSTAR")
                menu = input("¿Que desea hacer? ")
                if menu.lower()=="a":
                    en_linea["mail"]=""
                    en_linea["usuario"]=""
                    en_linea["monto_disponible"] = 0
                    os.system("cls")
                    print("Usted ha salido del sistema")
                elif menu.lower()=="b":
                    en_linea["monto_disponible"]=ingresar_dinero(en_linea)
                    input("~~ingrese una tecla cualquiera para continuar~~") #input meramente para que el usuario pueda leer
                    os.system("cls")
                elif menu.lower()=="c":
                    usuario_mas_timbero()
                    input("~~ingrese una tecla cualquiera para continuar~~") #input meramente para que el usuario pueda leer
                    os.system("cls")
                elif menu.lower()=="d":
                    print("~~~~~~~~~~~~~~~~~~~~~~~~")
                    mostrar_tabla()
                    print("~~~~~~~~~~~~~~~~~~~~~~~~")
                    input("~~ingrese una tecla cualquiera para continuar~~") #input meramente para que el usuario pueda leer
                    os.system("cls")
                elif menu.lower()=="e":
                    print("~~~~~~~~~~~~~~~~~~~~~~~~")
                    mostrar_plantel_equipo(equipos)
                    print("~~~~~~~~~~~~~~~~~~~~~~~~")
                    input("~~ingrese una tecla cualquiera para continuar~~") #input meramente para que el usuario pueda leer
                    os.system("cls")
                elif menu.lower()=="f":
                    print("~~~~~~~~~~~~~~~~~~~~~~~~")
                    mostrar_info_equipo(equipos)
                    print("~~~~~~~~~~~~~~~~~~~~~~~~")
                    input("~~ingrese una tecla cualquiera para continuar~~") #input meramente para que el usuario pueda leer
                    os.system("cls")
                elif menu.lower()=="g":
                    mostrar_suertudo()
                    input("~~ingrese una tecla cualquiera para continuar~~") #input meramente para que el usuario pueda leer
                    os.system("cls")
                elif menu.lower()=="h":
                    mostrar_grafico(equipos)
                    os.system("cls")
                elif menu.lower()=="i" and en_linea["monto_disponible"] > 0:
                    transacciones,data_usuario = empezar_apuesta(equipos,en_linea)
                    cargar_datos(transacciones,data_usuario,en_linea)
                    input("~~ingrese una tecla cualquiera para continuar~~") #input meramente para que el usuario pueda leer
                    os.system("cls")
                elif menu.lower()=="i" and en_linea["monto_disponible"] == 0:
                    print("no tienes dinero en cuenta para apostar, porfavor ingreselo primero.")
                    input("~~ingrese una tecla cualquiera para continuar~~") #input meramente para que el usuario pueda leer
                    os.system("cls")
                else:
                    input("Ingrese una opccion valida.") #input meramente para que el usuario pueda leer
                    os.system("cls")
        else:
            cerrado=False
        condicion_de_cierre=input("¿Deseas cerrar el programa? ('no' para mantener el programa abierto): ").upper()
        os.system("cls")
        if condicion_de_cierre != "NO":
            cerrado= False
            
main()
