#include <stdio.h>

int segundo_numero(int vector[] , int tamaño ) {
    int max = -100;
    int numero_maximo;
    int vector_aux[tamaño];
    
    for ( size_t j = 0 ; j < tamaño ; j++)
        vector_aux[j]=vector[j];
    
    for (size_t j=0 ; j < tamaño ; j++) {
        if (vector_aux[j] > max) {
            max=vector_aux[j];
            numero_maximo=j;
        }
    }
    vector_aux[numero_maximo]=0;
    max=-100;
    for (size_t j=0 ; j < tamaño ; j++) {
        if (vector_aux[j] > max) {
            max=vector_aux[j];
            numero_maximo=j;
        }
    }
    
    return max;
}

int main() {
    int vector[10];
    int mostrar;

    for (size_t i = 0 ; i < 10 ; i++) {
        printf("Ingrese un numero: \n");
        scanf("%d",vector+i);
    }

    mostrar=segundo_numero(vector , sizeof(vector)/sizeof(int));
    printf("El segundo numero mas grande es %d" , mostrar);


    return 0;
}