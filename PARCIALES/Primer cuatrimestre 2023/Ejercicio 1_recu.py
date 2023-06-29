
print("~Menu~ \n a -> Cargar un nuevo turno medico \n b -> Ver cuantas personas hay delante \n c -> Cargar medico \n d -> Listar cantidad de pacientes atendidos \n f -> Listar los pacientes que estan en espera")

def cargar_nuevo_turno_medico(turnos:dict , prioridad:dict ) -> None:
    turno= len(turnos) + 1
    dni=input("Ingrese el DNI: ")
    obra_social=input("Ingrese la obra social: ")
    medico=input("Ingrese el medico: ")
    tipo_atencion=input("Tipo de atencion: ")
    if tipo_atencion == "pediatría":
        edad=int(input("Ingrese la edad del menor: "))
    else:
        edad=0

    if (tipo_atencion == "pediatría" and edad < 2) or (tipo_atencion == "urgencia"):
        prioridad["alta"].append(turno)
    elif (tipo_atencion == "pediatría" and edad >= 2) or (tipo_atencion == "psiquiatria"):
        prioridad["media"].append(turno)
    elif tipo_atencion == "clinica":
        prioridad["baja"].append(turno)

    print(f"Su turno fue confirmado y posee el siguiente N°{turno}")
    turnos[turno]=[dni,obra_social,medico,tipo_atencion,edad]

def personas_delante(turnos_espera,prioridades):
    turno=int(input("Ingrese su turno: "))
    
    for prioridad_generica in prioridades:
        for j in range(len(prioridades[prioridad_generica])):
            if turno == prioridades[prioridad_generica][j]:
                prioridad=prioridad_generica
    for turno_generico in range(len(prioridades[prioridad])):
        if prioridades[prioridad][turno_generico] == turno:
            posicion=turno_generico
    
    if prioridad=="alta": personas_delante=posicion
    elif prioridad=="media": personas_delante=posicion + len(prioridades["alta"])
    elif prioridad=="baja": personas_delante=posicion + len(prioridades["alta"]) + len(prioridades["media"])
    print(f"Tenes {personas_delante} personas delante")

def ingresar_medico(medicos:list)->None:
    nombre=input("Nombre: ")
    apellido=input("Apellido: ")
    medicos.append(f"{nombre} {apellido}")
    print(medicos)

def listado_atendidos(turnos):
    urgencia=0
    pediatria=0
    clinica=0
    psiquiatria=0
    total=len(turnos)
    
    for turno in turnos:
        if turnos[turno][3] == "urgencia":
            urgencia+=1
        elif turnos[turno][3] == "pediatria":
            pediatria+=1
        elif turnos[turno][3] == "clinica":
            clinica+=1
        elif turnos[turno][3] == "psiquiatria":
            psiquiatria+=1
        
            
    print(f"Cantidad de pacientes atendidos: {total}")
    
    for turno in turnos:
        print(f"{turnos[turno][0]} fue atendido por {turnos[turno][2]} con atendicion de {turnos[turno][3]}")
    
    print(f"Porcentaje de urgencia: {(urgencia*100)/total}%")
    print(f"Porcentaje de pediatria: {(pediatria*100)/total}%")
    print(f"Porcentaje de clinica: {(clinica*100)/total}%")
    print(f"Porcentaje de psiquiatria: {(psiquiatria*100)/total}%")

def listado_por_prioridad(prioridades):
    print("Turnos con alta prioridad:")
    for turno_a in prioridades["alta"]:
        print(turno_a)
    print("Turnos con media prioridad:")
    for turno_a in prioridades["media"]:
        print(turno_a)
    print("Turnos con baja prioridad:")
    for turno_a in prioridades["baja"]:
        print(turno_a)

def listado_de_espera(turnos):
    print("Por orden de llegada:")
    for turno in turnos:
        print(turnos[turno][0])
    print("Por orden de atencion:")
    for turno in turnos:
        if (turnos[turno][3] == "pediatría" and turnos[turno][4] < 2) or (turnos[turno][3]  == "urgencia"): print(turnos[turno][0])
        elif (turnos[turno][3] == "pediatría" and turnos[turno][4] >= 2) or (turnos[turno][3] == "psiquiatria"): print(turnos[turno][0])
        elif turnos[turno][3] == "clinica" :print(turnos[turno][0])

def main():
    prioridad={'alta': [] , 'media': [] , 'baja': [] }
    #prioridad={'alta': [12,134,4653,3] , 'media': [1,2,3,4,5] , 'baja': [6,7,8,9] }
    #turnos_en_espera={"12":[1,"no","barrios","urgencia","20"]}
    medicos= ["fran barrios","max lopez","gel fernandez"," lur warner","tobi santillan"]
    turnos_en_espera=dict() #{ TURNO : [ dni , obra social , medico , tipo de atencion , edad ] }
    turnos_atendidos=dict() #{ TURNO : [ dni , obra social , medico , tipo de atencion , edad ] }
    
    condicion=""

    while condicion != "g":
        if condicion == "a":
            cargar_nuevo_turno_medico(turnos_en_espera,prioridad)
        elif condicion == "b":
            personas_delante(turnos_en_espera,prioridad)
        elif condicion == "c":
            ingresar_medico(medicos)
        elif condicion == "d":
            listado_atendidos(turnos_atendidos)
        elif condicion == "e":
            listado_por_prioridad(prioridad)
        elif condicion == "f":
            listado_de_espera(turnos_en_espera)
        condicion=input("indique que opccion quiere usar; \n ")
main()