import csv
import sys
sys.path.append('PARCIALES')
import funciones_generales as f_g

def cuestionario(atenciones:list):
    muñeco= input("Ingrese el nombre del muñeco: ")
    fecha= input("Ingrese la fecha de atencion: ")
    estadia=input("Ingrese el tiempo de estadia: ")
    diagnostico=input("Ingrese el diagnosico: ")
    medico=input("Ingrese el medico que lo atendio: ")
    costo=input("ingrese el costo: ")

    atenciones.append([muñeco,fecha,estadia,diagnostico,medico,costo])

def nueva_atencion(atenciones:list):
    nuevas_atenciones=list()
    cuestionario(nuevas_atenciones)

    usuario=True
    while usuario:
        pregunta=input("¿Desea agregar otra atencion? (si/no)").lower()
        while pregunta.lower() != "no" and pregunta.lower() != "si":
            pregunta=input("Ingrese una respuesta valida: ")
        if pregunta.lower() == "no": usuario=False
        else: cuestionario(nuevas_atenciones)

    archive=open("PARCIALES/2022/atenciones.csv" , "w" ,encoding="UTF-8" , newline="")
    csv_writer=csv.writer(archive,delimiter=",")
    csv_writer.writerows(atenciones)
    csv_writer.writerows(nuevas_atenciones)
    archive.close()

def validar_miembro(atenciones:list,miembro:str):
    veces_que_aparece=0
    for atencion in atenciones:
            diagnostico=atencion[3].lower()
            if miembro in diagnostico:
                veces_que_aparece+=1
    if veces_que_aparece == 0:
        return True
    else:
        return False

def reporte_miembro(atenciones:list):

    miembro=input("Ingrese un miembro: ").lower()
    while validar_miembro(atenciones,miembro):
        print(validar_miembro(atenciones,miembro))
        miembro=input("El miembro que ingreso es incorrecto, ingrese uno valido: ").lower()
    
    costo_total_por_miembro=0
    veces_que_aparece=0
    for atencion in atenciones:
            diagnostico=atencion[3].lower()
            monto=int(atencion[5])
            if miembro.lower() in diagnostico:
                costo_total_por_miembro+=monto
                veces_que_aparece+=1
    
    promedio=round(costo_total_por_miembro/veces_que_aparece,2)
    print(f"{miembro} tiene un costo promedio de ${promedio}")

def datos_medicos(atenciones):
    medicos=list()
    for atencion in atenciones:
        medico=atencion[4]
        if medico not in medicos:
             medicos.append(medico)
    
    dict_medicos=dict()
    suma_total_atenciones=0
    estadia_total=0
    for medico in medicos:
        estadia_por_medico=0
        pacientes=0
        for atencion in atenciones:
              estadia=int(atencion[2])
              if atencion[4] == medico:
                   pacientes+=1
                   estadia_por_medico+=estadia
        dict_medicos[medico]=(pacientes, estadia_por_medico)
        suma_total_atenciones+=pacientes
        estadia_total+=estadia_por_medico
    
    for i in range(1,101):
        for medico in dict_medicos:
            promedio_estadia=(dict_medicos[medico][1]*100)//estadia_total
            pacientes=int(dict_medicos[medico][0])
            if promedio_estadia == i:
                print(f"{medico} -> {promedio_estadia}% de estadia con {pacientes} pacientes")

def abandonados(atenciones:list):
    pacientes_abandonados=list()
    pacientes=list()
    for atencion in atenciones:
        paciente=atencion[0]
        if paciente not in pacientes:
             pacientes.append(paciente)
    fecha_referencia=202208

    for paciente in pacientes:
        ultima_fecha=0
        for atencion in atenciones:
            fecha=int(atencion[1])
            if paciente == atencion[0] and fecha > ultima_fecha:
                ultima_fecha=fecha
                diagnostico=atencion[3]
        if abs(fecha_referencia-ultima_fecha) > 100:
            pacientes_abandonados.append([paciente,diagnostico])
    
    archive=open("PARCIALES/2022/abandonados.csv","w",encoding="UTF-8",newline="")
    csv_writer=csv.writer(archive,delimiter=",")
    csv_writer.writerows(pacientes_abandonados)

def main():
    atenciones=f_g.leer_archivo("PARCIALES/2022/atenciones.csv","csv")
    print(atenciones)
    opcciones={"a":("nueva atencion",nueva_atencion,[atenciones]),"b":("Reporte por miembro", reporte_miembro , [atenciones]),"c":("distribucion de atenciones por medico y promedio de estadia",datos_medicos,[atenciones]),"d":("archivo abandonados.csv",abandonados,[atenciones])}
    f_g.ejecutar_menu(opcciones)

main()