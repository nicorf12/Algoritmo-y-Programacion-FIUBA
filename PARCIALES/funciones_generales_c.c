#include <stdio.h>

void igualar_vectores( int vec1[] , int vec2[] , int tamaño) {
    for ( size_t j = 0 ; j < tamaño ; j++)
        vec1[j]=vec2[j];
}

void invertir_vector(int vector[],int tamaño) {

    int vector_invertido[tamaño];

    for (size_t i = 0; i < tamaño; i++) {
        vector_invertido[i]=vector[tamaño-1-i];
    }
    
    igualar_vectores(vector,vector_invertido,tamaño);
}

void mostrar_vector(int vector[] , int tamaño) {
    for (size_t i = 0; i < tamaño; i++) {
        printf("%d",vector[i]);
    }
}

int devolver_mas_grande(int vector[], int tamaño) {
    int max=-1000;
    for (int i ; i < tamaño; i++ ) {
        if (vector[i] > max) {
            max= vector[i];
        }
    }
    return max;
}

int main() {
    return 0; 
}