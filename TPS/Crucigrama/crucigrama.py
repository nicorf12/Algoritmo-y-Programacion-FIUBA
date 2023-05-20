import random
import os

def iniciar_juego(cincuenta_palabras:dict)->None:
    """se encarga de ejecutar las preparaciones necesarias para el juego e iniciar las interacciones necesarias con el usuario hasta que finalice la partida"""
    tablero,palabras,tablero_usuario,posicion_letras_primera,celdas_vocales,palabras_insertadas=preparacion(cincuenta_palabras)
    os.system("cls")
    mostrar_tablero(tablero_usuario,palabras)   
    condicion=True
    while condicion:
        condicion=empezar_interaccion(palabras,tablero_usuario,posicion_letras_primera,tablero,celdas_vocales,cincuenta_palabras,palabras_insertadas)
    
def preparacion(cincuenta_palabras:list)->tuple: #(tablero,12 palabras,tablero del usuario , posicion de las primeras letras , celdas de las vocales , palabras insertadas)
    tablero=[]
    palabras,posicion_letras_primera,celdas_vocales,palabras_insertadas=crear_tablero(cincuenta_palabras,tablero)
    tablero_usuario=crear_tablero_usuario(tablero,posicion_letras_primera)
    return tablero , palabras , tablero_usuario , posicion_letras_primera , celdas_vocales , palabras_insertadas
    
def crear_tablero(cincuenta_palabras:list,tablero:list)->tuple:
    "crea el tablero e inserta las 12 palabras"
    palabras_insertadas=[]
    palabras=elegir_palabras(cincuenta_palabras)
    for fila in range(20):
        tablero.append([])
        for columna in range(20):
            tablero[fila].append("███")
    posicion_letras_primera,celdas_vocales=insertar_palabras_tablero(palabras,tablero)
    return palabras,posicion_letras_primera , celdas_vocales , palabras_insertadas

def elegir_palabras(cincuenta_palabras:list)->list:
    """elige de las 50 palabras, 12 de una forma random"""
    palabras=[]
    while len(palabras)<12:
        numero_random=random.randint(1,50)
        if numero_random not in palabras:
            palabras.append(numero_random)
    for i in range(len(palabras)):
        palabras[i]=cincuenta_palabras[palabras[i]]
    return palabras

def insertar_palabras_tablero(palabras:list,tablero:list)->tuple:
    """inserta las 12 palabras en el tablero de referencia"""
    palabras_insertar=[]
    for palabra in palabras:
        palabras_insertar.append(palabra[0])
    posicion_letras_primera,celdas_vocales=ajustar(tablero,palabras_insertar)
    return posicion_letras_primera , celdas_vocales

def ajustar(tablero:list,palabras:list)->tuple:
    """se encarga de verificar si entra la palabra  y la inserta"""
    posicion_letras_primera=[]
    celdas_vocales=[]
    for palabra in palabras:
        condicion=True
        while condicion:
            celda=elegir_una_celda()
            acumulador=0
            #vertical
            if palabra in palabras[0:6]:
                if len(palabra)+1 <= (19-celda[0]):
                    for posicion in range(len(palabra)):
                        if "███" == tablero[celda[0]+posicion][celda[1]] and tablero[celda[0]-1][celda[1]]=="███": #si no choca con otra palabra ejecuta esto
                            acumulador+=1
                        elif palabra[posicion] == tablero[celda[0]+posicion][celda[1]] and tablero[celda[0]-1][celda[1]]=="███":
                            acumulador+=1
                    if acumulador==len(palabra): #inserta la palabra
                        for letra in range(len(palabra)):
                            tablero[celda[0]+ letra][celda[1]]=palabra[letra]
                            if is_vocal(palabra[letra]):
                                celdas_vocales.append([celda[0]+letra,celda[1],palabra[letra]])
                        tablero[celda[0]-1][celda[1]]="*"
                        posicion_letras_primera.append(celda)
                        condicion=False

            #horizontal
            elif palabra in palabras[6:12]:
                if len(palabra)+1 <= (19-celda[1]):
                    for posicion in range(len(palabra)):
                        if "███" == tablero[celda[0]][celda[1]+posicion] and tablero[celda[0]][celda[1]-1]=="███":
                            acumulador+=1
                        elif palabra[posicion] == tablero[celda[0]][celda[1]+posicion] and tablero[celda[0]][celda[1]-1]=="███":    
                            acumulador+=1
                    if acumulador==len(palabra): #inserta la palabra
                        for letra in range(len(palabra)):
                            tablero[celda[0]][celda[1]+ letra]=palabra[letra]
                            if is_vocal(palabra[letra]):
                                celdas_vocales.append([celda[0],celda[1]+letra,palabra[letra]])
                        tablero[celda[0]][celda[1]-1]="*"
                        posicion_letras_primera.append(celda)
                        condicion=False
    return posicion_letras_primera , celdas_vocales

def crear_tablero_usuario(tablero_original:list,posicion_letras_primera:list)->list:
    """crea el tablero que le mostrare al usuario"""
    tablero_usu=[]
    for fila in tablero_original:
        tablero_usu.append(list(fila)) #con esta tecnica me aseguro de copiarla y no pasarla por referencia
    for fila in range(20):             #cambio las letras por espacios
         for columna in range(20):
                if tablero_usu[fila][columna]!= "███":
                    tablero_usu[fila][columna]=" "
    aux=0
    letras="abcdefghijkl"
    for posicion in posicion_letras_primera[0:6]:      #cambio las primeras letras de las palabras verticales por una letra especifica
        tablero_usu[posicion[0]-1][posicion[1]]= letras[aux]
        aux+=1
    aux=6
    for posicion in posicion_letras_primera[6:12]:      #cambio las primeras letras de las palabras horizontales por una letra especifica
        tablero_usu[posicion[0]][posicion[1]-1]= letras[aux]
        aux+=1
    return tablero_usu

def elegir_una_celda()->tuple:
    return random.randint(1,19) , random.randint(1,19)

def mostrar_tablero(tablero:list,palabras:list=[])->None:
    """muestra cualquier tablero"""
    for i in range(len(tablero)):
        print(end="\n")
        for j in range(len(tablero)):
            print("{:^3}".format(tablero[i][j]), end="")
    if palabras!=[]:    
        for i in range(12):
            print(f"\n {i + 1} corresponde a {palabras[i][1]}")

def empezar_interaccion(palabras:list,tablero_usuario:list,posicion_letras_primera:list,tablero:list,celdas_vocales:list,cincuenta_palabras:dict,palabras_insertadas:list)->bool:
    """comienza la interaccion con el usuario y al validarla la inserta"""
    if validar_completo(tablero,tablero_usuario):
        prueba=pedir_palabra() 
        if validacion(prueba,palabras_insertadas):
            if verificar_palabra(prueba,palabras): #si llego hasta aca, ya esta validada, y verificamos ahora sea correcta la respuesta.
                insertar_palabra_verificada(prueba,palabras_insertadas,palabras,tablero_usuario,posicion_letras_primera)
                os.system("cls")
                mostrar_tablero(tablero_usuario,palabras)
                return True
            else:
                os.system("cls")
                input("te equivocaste . . . pulse su letra de la suerte ") #condicion de dados
                os.system("cls")
                mostrar_tablero(tablero_usuario,palabras)
                return tirar_dados(tablero_usuario,celdas_vocales,palabras,posicion_letras_primera,palabras_insertadas,cincuenta_palabras,tablero)
        else:
            print("Intentalo de nuevo. . . pero ingresando bien los datos")
            mostrar_tablero(tablero_usuario,palabras)
            return True               
                
def pedir_palabra()->list:
    return input("Ingrese [defincion]+[referencia del tablero] y la palabra para esos casilleros: ").split(" ")

def validacion(prueba:list,palabras_insertadas:list)->bool:
    """valida si lo que inserto el usuario fue dado en la forma en la que el programa la acepta"""
    referencias="abcdefghijkl"
    condicion1=True   #con esto me aseguro que me den una palabra
    condicion2=False
    condicion3=True
    if len(prueba)==2:
        if prueba[1].isalnum():
            for letra in prueba[1]:
                if letra.isnumeric():
                    condicion1=False
                    os.system("cls")
                    print("ingresaste un caracter numerico en la palabra")
    
        for j in range(len(palabras_insertadas)):   #con esto me aseguro no me de palabra incorrecta si la palabra ya se encuentre en el tablero    
            if prueba[1] in palabras_insertadas[j]:
                os.system("cls")
                print("la palabra ya se encuentra en el tablero")
                condicion1=False


    #con esto me aseguro que la definicion sea un numero de uno o mas digitos
        if len(prueba[0])<=2:
            if prueba[0][0].isnumeric():
                condicion2=True
            else:
                os.system("cls")
                print("en lugar de la definicion pusiste otro caracter")
        elif len(prueba[0])<=3:
            if prueba[0][0].isnumeric() and prueba[0][1].isnumeric():
                condicion2=True
            else:
                os.system("cls")
                print("en uno de los lugares de la definicion pusiste otro caracter")
        
    #con esto me aseguro que la refencia sea una letra
        if len(prueba[0])<=2:
            if prueba[0][1].isalnum():
                if prueba[0][1] not in referencias:#prueba[0][1].isnumeric():
                    condicion3=False
                    os.system("cls")
                    print("No ingresaste una referencia valida")
                    #print("Ingresaste un numero en vez de referencia del tablero")
        elif len(prueba[0])<=3:
            if prueba[0][2].isalnum():
                if prueba[0][2] not in referencias:#prueba[0][2].isnumeric():
                    condicion3=False
                    os.system("cls")
                    print("No ingresaste una referencia valida")
                    #print("Ingresaste un numero en vez de referencia del tablero")
    else:
        print("no ingresaste los datos correctamente")
    condicion_final=False
    if condicion1 and condicion2 and condicion3:
        condicion_final=True
    return condicion_final

def verificar_palabra(prueba_v:list,palabras:list)->bool: # [def+referencia,palabra]
    """verifica si la palabra dada es la que debia ir"""
    if len(prueba_v[0])<=2:
        definicion=int(prueba_v[0][0])
        referencia=prueba_v[0][1]
    elif len(prueba_v[0])<=3:
        definicion=int(prueba_v[0][0]+prueba_v[0][1])
        referencia=prueba_v[0][2]
    palabra_usu=prueba_v[1]

    verficacion={} #con este diccionario vinculo la refenrencia en el tablero con su definicion y palabra
    referencias="abcdefghijkl"
    for j in range(len(referencias)):
        verficacion[referencias[j]]=(j+1,palabras[j][0])  #verficacion={'referencia':(definicion{1 al 12 inclusive},palabra)}
    
    if verficacion[referencia]==(definicion,palabra_usu):
        return True
    else:
        return False

def insertar_palabra_verificada(palabra,palabras_insertadas,palabras,tablero_usuario,posicion_letras_primera)->None:
    """si la palabra fue vericada, entonces la inserta en el tablero del usuario"""
    palabras_aux=[]
    for palabra_aux in palabras:
        palabras_aux.append(palabra_aux[0])

    if len(palabra[0])<=2:
        definicion=int(palabra[0][0])

    elif len(palabra[0])<=3:
        definicion=int(palabra[0][0]+palabra[0][1])
        
        

    palabra_usu=palabra[1]

        
        
    if palabra_usu in palabras_aux[0:6]:
        for letra in range(len(palabra_usu)):
            tablero_usuario[posicion_letras_primera[definicion-1][0]+letra][posicion_letras_primera[definicion-1][1]]=palabra_usu[letra]  #a partir de la celda donde se encuentra la primer letra escribo verticalmente
        tablero_usuario[posicion_letras_primera[definicion-1][0]-1][posicion_letras_primera[definicion-1][1]]="*"
        palabras_insertadas.append([definicion,palabra_usu,palabras[definicion-1][1]])
    elif palabra_usu in palabras_aux[6:12]:
        for letra in range(len(palabra_usu)):
            tablero_usuario[posicion_letras_primera[definicion-1][0]][posicion_letras_primera[definicion-1][1]+letra]=palabra_usu[letra] #a partir de la celda donde se encuentra la primer letra escribo horizontalmente
        tablero_usuario[posicion_letras_primera[definicion-1][0]][posicion_letras_primera[definicion-1][1]-1]="*"
        palabras_insertadas.append([definicion,palabra_usu,palabras[definicion-1][1]])

def validar_completo(tablero:list,tablero_usuario:list)->bool:
    """valida si ambos tablero son iguales, si es asi, termina la partida"""
    if tablero != tablero_usuario:
        return True
    else:
        print("FELICIDADES . . . HAS COMPLETADO EL CRUCIGRAMA")
        return False

def tirar_dados(tablero_usuario:list,celdas_vocales:list,palabras:list,posicion_letras_primera:list,palabras_insertadas:list,cincuenta_palabras:dict,tablero:list)->bool:
    """si el usuario se equivoco entonces ejecuta una funcion dependiendo del dado"""
    dados=random.randint(1,5)
    input(f". . . se estan tirando los dados . . .\n salio {dados} \n pulse una tecla para continuar")
    if dados==1 or dados==2:
        print(palabras_insertadas)
        if len(palabras_insertadas) !=0 :    
            palabra_borrada=cambio_de_palabras(palabras,palabras_insertadas,cincuenta_palabras)
            reordenar(tablero,tablero_usuario,posicion_letras_primera,celdas_vocales,palabras)
            insertar_palabras_ordenadas(palabras,palabras_insertadas,tablero_usuario,posicion_letras_primera)
            os.system("cls")
            print(f"se te ha borrado la plabara {palabra_borrada}")
            mostrar_tablero(tablero_usuario,palabras)
        else:
            print("no puedo borrarte ninguna . . . sigue jugando")  #preguntar que hacer en este caso
        return True
    if dados==3 or dados==4:
        os.system("cls")
        print("Has tenido suerte .. .")
        deslumbrar_vocales(tablero_usuario,celdas_vocales)
        mostrar_tablero(tablero_usuario,palabras)
        return True
    if dados==5:
            
        descubrir_una_palabra(palabras,tablero_usuario,posicion_letras_primera,palabras_insertadas)
        os.system("cls")
        mostrar_tablero(tablero_usuario,palabras)
        return True
    if dados==6:
        return False

def reordenar(tablero:list,tablero_usuario:list,posicion_letras_primera:list,celdas_vocales:list,palabras:list)->None:
    """reordena los tablero con la nueva palabra y los datos que necesitamos para el resto del programa"""
    while tablero!=[]:
            tablero.pop()
            tablero_usuario.pop()
    while posicion_letras_primera!=[]:
        posicion_letras_primera.pop()
    while celdas_vocales!=[]:
        celdas_vocales.pop()
    #limpiar los tableros al igual que los indices de primeras letras y y vocales
    for fila in range(20):
        tablero.append([])
        for columna in range(20):
            tablero[fila].append("███")
        
    u,w=insertar_palabras_tablero(palabras,tablero)
    for i in range(len(u)):
        posicion_letras_primera.append(u[i])
        
    for j in range(len(w)): 
        celdas_vocales.append(w[j])

    tablero_usuario_aux=crear_tablero_usuario(tablero,posicion_letras_primera) #posicion_letras_primera , celdas_vocales
    for p in range(len(tablero_usuario_aux)):
        tablero_usuario.append([])
        for y in range(len(tablero_usuario_aux[p])):
            tablero_usuario[p].append(tablero_usuario_aux[p][y])

def is_vocal(letra:str)->True:
    vocales="aeiou"
    if vocales.find(letra) != -1: return True
    else: return False

def insertar_palabras_ordenadas(palabras:list,palabras_insertadas:list,tablero_usuario:list,posicion_letras_primera:list)->None:
    """inserta las palabras en el nuevo tablero reordenado"""
    for i in range(len(palabras_insertadas)):    
        if (palabras_insertadas[i][1],palabras_insertadas[i][2]) in palabras[0:6]:  #si las palabras son verticales
            for letra in range(len(palabras_insertadas[i][1])):
                tablero_usuario[posicion_letras_primera[palabras_insertadas[i][0]-1][0]+letra][posicion_letras_primera[palabras_insertadas[i][0]-1][1]]=palabras_insertadas[i][1][letra]  #es el codigo de la funcion de arriba pero con los nombres ajustados
            tablero_usuario[posicion_letras_primera[palabras_insertadas[i][0]-1][0]-1][posicion_letras_primera[palabras_insertadas[i][0]-1][1]]="*"
                
        elif (palabras_insertadas[i][1],palabras_insertadas[i][2]) in palabras[6:12]: #si las palabras son horizontales
            for letra in range(len(palabras_insertadas[i][1])):
                tablero_usuario[posicion_letras_primera[palabras_insertadas[i][0]-1][0]][posicion_letras_primera[palabras_insertadas[i][0]-1][1]+letra]=palabras_insertadas[i][1][letra] #es el codigo de la funcion de arriba pero con los nombres ajustados, asi no se me suman sus posicion es la lista de posiciones primeras
            tablero_usuario[posicion_letras_primera[palabras_insertadas[i][0]-1][0]][posicion_letras_primera[palabras_insertadas[i][0]-1][1]-1]="*"

def deslumbrar_vocales(tablero_usuario:list,celdas_vocales:list)->None:
    """pone a la vista del ususario las vocales"""
    for j in range(len(celdas_vocales)):  
        if celdas_vocales[j][2] == "a":
            tablero_usuario[celdas_vocales[j][0]][celdas_vocales[j][1]]="a"
        if celdas_vocales[j][2] == "e":
            tablero_usuario[celdas_vocales[j][0]][celdas_vocales[j][1]]="e"
        if celdas_vocales[j][2] == "i":
            tablero_usuario[celdas_vocales[j][0]][celdas_vocales[j][1]]="i"
        if celdas_vocales[j][2] == "o":
            tablero_usuario[celdas_vocales[j][0]][celdas_vocales[j][1]]="o"
        if celdas_vocales[j][2] == "u":
             tablero_usuario[celdas_vocales[j][0]][celdas_vocales[j][1]]="u"

def descubrir_una_palabra(palabras:list,tablero_usuario:list,posicion_letras_primera:list,palabras_insertadas:list)->None:
    """da a elegir una palabra que quiera descrubrir y si es valido lo que inserto, la descrubre"""
    descubrir=input("Danos la definicion de la palabra que quieres descubrir: ")
    if validacion_descubrir(descubrir,palabras_insertadas,tablero_usuario,palabras):
        descubrir=int(descubrir)
        if ( palabras[descubrir-1][0],palabras[descubrir-1][1] ) in  palabras[0:6]: #veririca si son verticales
            insertar_palabra_verificada((str(descubrir)+"a",palabras[descubrir-1][0]),palabras_insertadas,palabras,tablero_usuario,posicion_letras_primera)
        elif ( palabras[descubrir-1][0],palabras[descubrir-1][1] ) in  palabras[6:12]:
            insertar_palabra_verificada((str(descubrir)+"a",palabras[descubrir-1][0]),palabras_insertadas,palabras,tablero_usuario,posicion_letras_primera) 
    else:
        os.system("cls")
        print("Intentalo de nuevo")
        descubrir_una_palabra(palabras,tablero_usuario,posicion_letras_primera,palabras_insertadas)

def validacion_descubrir(descubrir:str,palabras_insertadas:list,tablero_usuario:list,palabras:list)->bool:
    """valida si inserto algo valido o si lo que inserto ya pertenecia al tablero"""
    condicion1=False
    if descubrir.isdigit() and len(descubrir)<=2:
        if 1<=int(descubrir)<=12:
            condicion1=True
    else:
        os.system("cls")
        print("no has insertado ninguna definicion . . . hazlo de nuevo")
        mostrar_tablero(tablero_usuario,palabras)

    defs_insertadas=[]
    condicion2=False
    for palabra in palabras_insertadas:
        print(palabra[0])
        defs_insertadas.append(palabra[0])
        
    if descubrir not in defs_insertadas:
        condicion2=True
    else:
        os.system("cls")
        print("la definicion de la palabra insertada ya pertenece al tablero . . . intente de nuevo")
        mostrar_tablero(tablero_usuario,palabras)
        
    if condicion1 and condicion2:
        return True
    else:
        return False

def cambio_de_palabras(palabras:list,palabras_insertadas:list,cincuenta_palabras:dict)->None: 
    """elimina una de las palabras insertadas de las 12 y elije otra de las 50"""
    n_random=random.randint(0,len(palabras_insertadas)-1) 
    palabra_borrada=palabras_insertadas[n_random][1]
    palabras_insertadas.remove(palabras_insertadas[n_random])
        
    #hasta aca pierdo una palabra que haya insertado
    indice_p_b=0
    j=0
    while j < len(palabras):
        if palabra_borrada == palabras[j][0]:
            palabras.remove(palabras[j])
            indice_p_b=j
        j+=1
    #hasta aca borro la palabra insertada de las 12 palabras
    condicion=True
    while condicion:
        n_random2=random.randint(1,50)
        if cincuenta_palabras[n_random2] not in palabras:    
            palabras.insert( indice_p_b ,cincuenta_palabras[n_random2])
            condicion=False
     #hasta aca inserto una de las palabras a la lista de palabras que no sea igual a las que ya estan

    return palabra_borrada , indice_p_b


def main():
    cincuenta_palabras={
        1:('casa','un edificio o estructura que se usa como hogar.'),
        2:('perro','un animal domesticado que se usa a menudo como mascota (dice guau).'),
        3:('gato','un animal domesticado que se usa a menudo como mascota (dice miau).'),
        4:('niño','un ser humano joven que aún no es adulto.'),
        5:('arbol','una planta de tronco leñoso que tiene ramas y hojas.'),
        6:('agua','un líquido inodoro, incoloro e insípido que es esencial para la vida.'),
        7:('sol','una estrella que es el centro del sistema solar.'),
        8:('dia','un periodo de 24 horas que comienza y termina con el amanecer y el atardecer.'),
        9:('noche','el periodo de tiempo oscuro entre el atardecer y el amanecer.'),
        10:('manzana','una fruta redonda y roja o verde que es comúnmente consumida.'),
        11:('comida','cualquier cosa que se come para nutrir el cuerpo.'),
        12:('bebida','cualquier líquido que se consume para hidratar el cuerpo.'),
        13:('amigo','una persona con la que se tiene una relación de afecto y confianza.'),
        14:('libro','una obra impresa que contiene historias, información o conocimientos.'),
        15:('juego','una actividad realizada por diversión o entretenimiento.'),
        16:('trabajo','una actividad realizada con el objetivo de producir algo o ganar dinero.'),
        17:('lugar','un sitio o espacio en el que se puede estar o habitar.'),
        18:('cama','un mueble en el que se puede dormir o descansar.'),
        19:('silla','un mueble con un asiento y un respaldo que se usa para sentarse.'),
        20:('mesa','un mueble plano que se usa para colocar cosas o para comer.'),
        21:('telefono','un dispositivo electrónico que se usa para comunicarse con otros a distancia.'),
        22:('computadora','una máquina electrónica que se usa para procesar y almacenar información.'),
        23:('television','un dispositivo electrónico que muestra imágenes y sonidos en una pantalla.'),
        24:('pelota','un objeto esférico que se usa para jugar o hacer ejercicio.'),
        25:('deporte','una actividad física realizada por diversión o competición.'),
        26:('ropa','prendas que se usan para cubrir el cuerpo y protegerlo del clima.'),
        27:('zapatilla','calzado que se usa para cubrir los pies y caminar con comodidad.'),
        28:('tienda','un establecimiento comercial en el que se venden productos.'),
        29:('mercado','un lugar donde se venden productos frescos y comestibles.'),
        30:('escuela','una institución educativa en la que se imparten clases y se aprende.'),
        31:('universidad','una institución educativa superior en la que se imparten estudios superiores.'),
        32:('hospital','un centro médico en el que se atienden a los enfermos y heridos.'),
        33:('medico','un profesional de la salud que diagnostica y trata enfermedades.'),
        34:('enfermera','un profesional de la salud que brinda atención y cuidado a los pacientes.'),
        35:('dentista','un profesional de la salud que se especializa en el cuidado dental.'),
        36:('abogado','un profesional que brinda asesoría y defensa legal a sus clientes.'),
        37:('coche','un vehículo de motor que se utiliza para transportarse en carreteras.'),
        38:('avion','una aeronave que se utiliza para transportar personas o mercancías por el aire.'),
        39:('barco','una embarcación que se utiliza para navegar en agua.'),
        40:('tren','un vehículo que se mueve sobre raíles y se utiliza para transportar personas o mercancías.'),
        41:('colectivo','un vehículo grande que se utiliza para transportar a varias personas a la vez.'),
        42:('bicicleta','un vehículo de dos ruedas que se mueve por la fuerza de la persona que la maneja.'),
        43:('plaza','un lugar al aire libre que se utiliza para actividades recreativas.'),
        44:('playa','una zona de tierra al lado del mar o un río donde se puede nadar y tomar el sol.'),
        45:('montaña','una elevación natural de la superficie terrestre con una cima puntiaguda.'),
        46:('rio','un curso de agua que fluye hacia el mar o un lago.'),
        47:('campo','un área rural o de tierra abierta que se utiliza para la agricultura o la ganadería.'),
        48:('ciudad','una zona densamente poblada que se caracteriza por tener edificios y calles.'),
        49:('pais','una entidad política y geográfica con un gobierno propio y una población definida.'),
        50:('fuego','herramienta muy importante para la humanidad y se utiliza para cocinar, calentar, iluminar y producir energía.')
    }
    
    print("|| BIENVENIDO A MI CRUCIGRAMA || --> porfavor siga las indicaciones del informe \n si no deseas jugar escriba algo distinto a si.")
    decision=input("»¿Deseas hecharte una partida?«")
    while decision.upper()=="SI":
        iniciar_juego(cincuenta_palabras)
        decision=input("¿Quieres jugar otro?")
    else:
        input("VUELVA PRONTO")
main()