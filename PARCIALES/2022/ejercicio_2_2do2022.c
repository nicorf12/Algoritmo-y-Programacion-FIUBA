#include <stdio.h>
#include <string.h>

int mayor_sumatoria( int vector_sumatoria[] , char* tipo_vector , int N , int matriz[N][N] ) {
    int sumatoria_columna;
    int sumatoria_fila;
    int vector_filas[N][2]; // {sumatoria,numero de fila}
    int fila_max;
    int vector_columnas[N][2];
    int columna_max;
    int max_fila=-1000;
    int max_columna=-1000;
    char columna[]="columna";
    //int vector_sumatoria[2]; {Ñro de fila o columa , sumatoria }
    //vector_sumatoria[0]=1;
    //vector_sumatoria[1]=12;

    //fila mas grande
    // matriz[fila][columna] 
    for (int i=0; i< N; i++) {
        sumatoria_fila=0;
        for (int j=0; j< N; j++) {
            sumatoria_fila= sumatoria_fila + matriz[i][j];
        }
        vector_filas[i][0]=sumatoria_fila;
        vector_filas[i][1]=i+1;
    }

    
    for (int i = 0 ; i < N; i++ ) {
        if (vector_filas[i][0] > max_fila) {
            max_fila= vector_filas[i][0];
            fila_max= vector_filas[i][1];
        }
    }

    printf("%d tiene la fila %d\n" ,max_fila , fila_max);

    //columna mas grande
    for (int i=0; i< N; i++) {
        sumatoria_columna=0;
        for (int j=0; j< N; j++) {
            sumatoria_columna= sumatoria_columna + matriz[j][i];
        }
        vector_columnas[i][0]=sumatoria_columna;
        vector_columnas[i][1]=i+1;
    }

    
    for (int i = 0 ; i < N; i++ ) {
        if (vector_columnas[i][0] > max_columna) {
            max_columna= vector_columnas[i][0];
            columna_max= vector_columnas[i][1];
        }
    }

    printf("%d tiene la columna %d\n" ,max_columna , columna_max);
    
    //comparamos

    if (max_columna > max_fila) {
        vector_sumatoria[0]=columna_max;
        vector_sumatoria[1]=max_columna;
        strcpy(tipo_vector,columna);
    } else {
        vector_sumatoria[0]=fila_max;
        vector_sumatoria[1]=max_fila;
    }

    return vector_sumatoria;
}

int main() {
    int vector_sumatoria[2];
    char tipo_vector[10]="fila";
    int N;
    printf("Ingrese el N de la matriz");
    scanf("%d", &N);
    int matriz[N][N];

    for (int i=0; i < N ; i++) {
        for (int j=0 ; j < N ; j++ ) {
            printf("Ingrese el valor de la %d fila en la %d columna: ",i,j);
            scanf("%d", &matriz[i][j]);
        }
    }

    printf("\n");
    mayor_sumatoria(vector_sumatoria, tipo_vector , N , matriz);
    printf("\n");
    printf("La fila o columna que mas sumatoria tiene es la %s %d con %d", tipo_vector,vector_sumatoria[0],vector_sumatoria[1]);
    return 0;
}