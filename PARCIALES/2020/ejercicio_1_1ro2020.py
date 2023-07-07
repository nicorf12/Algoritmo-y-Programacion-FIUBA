import os

def leer_archivo(archivo:str)->list:
    lineas=list()
    if os.path.exists(archivo):
        f=open(archivo, "r" ,encoding="UTF-8",newline='\n')
        
        for linea in f:
            lineas.append(linea[0:-2].split(", "))
        f.close()
    return lineas[1::]

def viajes_de_roma():
    datos=leer_archivo("viajes.txt")
    for linea in datos:
        if "roma" in linea[3].lower():
            print(f"El tren {linea[0]} de {linea[3]} a {linea[4]} llega a su destino a las {linea[6]}")

def mostrar_trenes_demorados():
    datos=leer_archivo("viajes.txt")
    cant_trenes_demorados=0
    trenes_demorados=list()
    for linea in datos:
        if linea[7].lower()=="demorado":
            cant_trenes_demorados+=1
            trenes_demorados.append((linea[0],linea[1]))
    print(f"La cantidad de trenes demorados es: {cant_trenes_demorados} \nListado:")
    for tren in trenes_demorados:
        print(f"Tren {tren[0]} de {tren[1]}")

def trenes_demorados_entre_horarios(hora1:str,hora2:str):
    datos= leer_archivo("viajes.txt")
    for linea in datos:
        if linea[7].lower()=="demorado" and int(hora1)<=int(linea[6])<=int(hora2):
            print(f"Tren {linea[0]} de {linea[1]}")

def mostrar_trenes_ordenados():
    datos=leer_archivo("viajes.txt")
    abecedario=["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
    aux=list()
    for letra in abecedario:
        for linea in range(len(datos)):
            if datos[linea][3][0].lower()==letra:
                aux.append(datos[linea])
    for tren in aux:
        print(tren) #se podria hacer mas lindo pero al final lo hago

def archivo_demorados():
    datos=leer_archivo("viajes.txt")
    aux=list()
    for linea in range(len(datos)):
        if datos[linea][7].lower()=="demorado":
            aux.append(datos[linea])

    f=open("demorados.txt","w",encoding="UTF-8",newline='\n')
    for tren in aux:
        f.write(", ".join(tren))
    f.close()

def archivo_plataforma():
    datos=leer_archivo("viajes.txt")
    trenes_plataforma=list()
    for linea in datos:
        if linea[7].isdigit():
            trenes_plataforma.append([linea[0],linea[3],linea[4],linea[7]])
        
    f=open("en_plataforma","w",encoding="UTF-8",newline='')
    
    for tren in range(len(trenes_plataforma)):
        trenes_plataforma[tren]=", ".join(trenes_plataforma[tren]) + "\n"
    f.writelines(trenes_plataforma)
    f.close()

def main():
    condicion=True
    while condicion:
        print("~~MENU~~ \n a- Mostrar por pantalla todos los viajes procedentes de Roma. \n b- Mostrar trenes demorados \n c-Mostrar vuelos con hora de llegada (0700:0745) y esten demorados \n d- Mostrar todos los trenes ordenados por origen \n e-Crear archivo 'demorados.txt' \n f- Crear archivo 'total_trenes.txt' \n g.- Salir del programa")
        pregunta=input("¿Que deseas hacer? (indique el indice): ")
        if pregunta.upper()=="A":
            viajes_de_roma()
        elif pregunta.upper()=="B":
            mostrar_trenes_demorados()
        elif pregunta.upper()=="C":
            trenes_demorados_entre_horarios("0700" , "0745")
        elif pregunta.upper()=="D":
            mostrar_trenes_ordenados()
        elif pregunta.upper()=="E":
            archivo_demorados()
        elif pregunta.upper()=="F":
            archivo_plataforma()
        elif pregunta.upper()=="G":
            condicion=False
        else:
            print("Ingrese una opccion valida.")

main()
