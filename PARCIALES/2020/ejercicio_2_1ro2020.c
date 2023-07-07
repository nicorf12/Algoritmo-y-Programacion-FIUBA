#include <stdio.h>

int sueldos(){
    int empleados_sueldos_buenos=0;
    int i=0;
    int empleados_sueldos[100][2];
    int condicion;
    int min=10000000;

    do{
        printf("Ingrese el lejago:");
        scanf("%d",&empleados_sueldos[i][0]);
        printf("Ingrese el sueldo:");
        scanf("%d",&empleados_sueldos[i][1]);
        printf("Ingrese -1 para cortar o cualquier otro numero para seguir");
        scanf("%d",&condicion);
        if (empleados_sueldos[i][1] >= 80500){
            empleados_sueldos_buenos++;
        }
        if (empleados_sueldos[i][1] < min){
            min=empleados_sueldos[i][1];
        }
        i++;
        } while (condicion != -1 );
    
    printf("\n sueldo minimo: %d\n",min);

    for (size_t j = 0; j < i ; j++){
        if (empleados_sueldos[j][1] >= 80500){
            printf("\n%d cobra %d\n", empleados_sueldos[j][0] , empleados_sueldos[j][1] );
        } 
    }

    return empleados_sueldos_buenos;
}

void imprimir_cantidad_sueldos(int cantidad){
    if (cantidad==0){
        printf("Aun no se han ingresado sueldos o ningun cobra mas de 80500\n");
    } else {
        printf("En Somos Más S.A. los empleados que cobran más de 80500 pesos son: %d\n",cantidad);
    }

}

int main() {
    int cantidad;
    int pregunta;
    int condicion;
    do{
        printf("Menu -> 1 para ingresar sueldos, 2 para ver los que cobran mas de 80500\n");
        scanf("%d", &pregunta);
        switch (pregunta)
        {
        case 1:
            cantidad=sueldos();
            break;
        case 2:
            imprimir_cantidad_sueldos(cantidad);
            break;
        default:
            printf("No has ingresado algo bien\n");
            break;
        }
        printf("Escriba -1 para salir del programa\n");
        scanf("%d", &condicion);
    } while (condicion != -1);
    return 0;
}