import sys
sys.path.append('PARCIALES')
import funciones_generales as f_g

def cargar_ingreso(ingresos):

    concepto=input("Ingrese el concepto: ")
    tipo=input("Ingrese el tipo: ")
    monto=input("Ingrese el monto: ")
    while not monto.isdigit():
        monto=input("Ingrese un monto valido: ")

    ingresos.append((concepto,tipo,monto))

def gastos_categoria(gastos):
    categorias=[]
    total=0
    for gasto in gastos:
        categoria=gasto[1]
        monto=int(gasto[2])
        total+= monto
        if categoria not in categorias:
            categorias.append(categoria)
    print(categorias)


    for categoria in categorias:
        sumatorio=0
        for gasto in gastos:
            monto=int(gasto[2])
            if categoria == gasto[1]:
                sumatorio+=monto
        porcentaje= round( (sumatorio*100)/total , 2)
        print(f"{categoria} --> {porcentaje}%")

def analisis_gastos(gastos,ingresos):
    dinero_disponible=0
    for ingreso in ingresos:
        dinero_disponible+= int(ingreso[2])
    
    diccionario_prioridades=dict()
    for gasto in gastos:
        prioridad=gasto[3]
        if prioridad not in diccionario_prioridades:
            diccionario_prioridades[prioridad]=[gasto]
        else:
            diccionario_prioridades[prioridad].append(gasto)

    for prioridadd in diccionario_prioridades:
        for prioridad in diccionario_prioridades[prioridadd]:
            importe= int(prioridad[2])
            concepto= prioridad[0]
            prioridad= prioridad[3]
            if importe <= dinero_disponible:
                dinero_disponible-=importe
                print(f"{concepto}, {importe}, Cubierto totalmente")
            elif importe>=dinero_disponible and dinero_disponible!=0:
                porcentaje=round( (dinero_disponible*100)/importe ,2)
                dinero_disponible=0
                print(f"{concepto}, {importe}, Cubierto al {porcentaje}%")
            elif dinero_disponible==0:
                print(f"{concepto}, {importe}, No cubierto")

def gastos_excedidos(gastos:list):
    categorias=list()
    for gasto in gastos:
        categoria=gasto[1]
        if categoria.lower() not in categorias:
            categorias.append(categoria.lower())
            print(categoria)

    categoria=input("Ingrese un categoria: ").lower()
    while categoria not in categorias:
        categoria=input("Ingrese un categoria valida: ").lower()

    gastos_importantes=list()
    for gasto in gastos:
        categoria_gasto=gasto[1].lower()
        importe=int(gasto[2])
        if categoria_gasto == categoria and importe>20000:
            gastos_importantes.append(gasto)
    
    archive= open( f"PARCIALES/2023/gastos_importantes_{categoria}.txt" , "w" , encoding="UTF-8",  newline="" )
    for gasto in gastos_importantes:
        archive.write(f"{gasto[0]},{gasto[2]} \n")
    archive.close()


def main():
    gastos=f_g.leer_archivo("PARCIALES/2023/gastos.csv" , "csv")
    ingresos=[["MercadoLibre","Sueldo",50000],["MercadoLibre","Sueldo",40000]]
    opcciones={ "a": ("Cargar ingreso" , cargar_ingreso , [ingresos]) , "b" : ("Reporte de gastos" , gastos_categoria , [gastos]), "c":("Analisis de gastos" , analisis_gastos , [gastos,ingresos]),"d":("reporte de gastos que excedan los 20000", gastos_excedidos, [gastos])}
    f_g.ejecutar_menu(opcciones)
main()