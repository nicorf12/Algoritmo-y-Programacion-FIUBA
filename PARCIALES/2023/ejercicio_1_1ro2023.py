import sys
sys.path.append('PARCIALES')
import funciones_generales as f_g

def procesar_datos():
    ventas=f_g.leer_archivo("PARCIALES/2023/ventas.csv","csv",";") 
    productos=f_g.leer_archivo("PARCIALES/2023/productos.csv","csv",";")
    detalles=f_g.leer_archivo("PARCIALES/2023/detalles.csv","csv",";")
    
    dic_operaciones=dict() #{"numero de operacion":[ID Concesionaria,AAAAMMDD, {ID Producto:Cantidad,Importe total del registro}}
    dic_productos=dict()


    for operacion in ventas:
        j=0
        for venta in detalles:
            id_producto=venta[1]
            cantidad=venta[2]
            importe_total=venta[3]
            if operacion[0] == venta[0] and j==0:
                dic_operaciones[operacion[0]]=[operacion[1],operacion[2],{id_producto: (cantidad,importe_total)}]
                j+=1
            elif venta[0] == operacion[0] and j>0 :
                dic_operaciones[operacion[0]][2][id_producto]=(cantidad,importe_total)
            
    for producto in productos:
        dic_productos[producto[0]]=(producto[1],producto[2])

    print(dic_operaciones)
    print(dic_productos)
    return dic_productos, dic_operaciones

def linea_que_mas_vendio(productos:dict,operaciones:dict):
    lineas=[]
    for producto in productos:
        if productos[producto][1] not in lineas:
            linea=productos[producto][1]
            lineas.append(linea)

    dict_articulo_importe={}
    for linea in lineas:
        for key_operacion in operaciones:
            for articulo in operaciones[key_operacion][2]:
                importe=operaciones[key_operacion][2][articulo][1]
                if articulo not in dict_articulo_importe:
                    dict_articulo_importe[articulo]=int(importe)
                elif articulo in dict_articulo_importe and linea==articulo:
                    dict_articulo_importe[articulo]+=int(importe)

    resultados=dict()
    for articulo in dict_articulo_importe:
        if articulo in productos:
            linea=productos[articulo][1]
            importe=int(dict_articulo_importe[articulo])
            if linea not in resultados:
                resultados[linea]=importe
            elif linea in resultados:
                resultados[linea]+=importe

    max=-1
    linea_mas_vendio=""
    for resultado in resultados:
        if resultados[resultado]>max:
            max=resultados[resultado]
            linea_mas_vendio=resultado 
    print(f"La linea que mas vendio fue {linea_mas_vendio} con ${max}")

def ver_articulos_año(productos,operaciones,año):
    max=-1
    dict_aux=operaciones
    for operacion in dict_aux:
        if dict_aux[operacion][1][0:4]==año:
            dict_productos=dict_aux[operacion][2]
            for producto in dict_productos:
                cantidad=int(dict_productos[producto][0])
                if cantidad>max:
                    max=cantidad
                    articulo_max=producto
                    operacion_max=operacion
    print(f"{max} -> {productos[articulo_max][0]} ")


def articulos_años(productos,operaciones):
    años=list()
    for operacion in operaciones:
        año=operaciones[operacion][1][0:4]
        if año not in años:
            años.append(año)
    años.sort()
    print(años)
    for año in años:
        ver_articulos_año(productos,operaciones,año)
def importe_promedio():
    pass

def porcentaje_año_producto():
    pass

def cerrar():
    return False

def main():
    productos,operaciones = procesar_datos()
    articulos_años(productos,operaciones)

"""def main():
    menu={'a':("Linea que mas se vendio",linea_que_mas_vendio),'b':("ver cantidad de articulos vendidos por año",articulos_año),'c':("ver importe promedio por operacion",importe_promedio),'d':("ver porcentaje del total de operaciones para un año y linea de producto",porcentaje_año_producto),'e':("cerrar programa",cerrar)}
    productos,operaciones = procesar_datos()
    condicion=True
    while condicion:
        vuelta=f_g.ejecutar_menu(menu)
        if vuelta == False:
            condicion=False"""
main()