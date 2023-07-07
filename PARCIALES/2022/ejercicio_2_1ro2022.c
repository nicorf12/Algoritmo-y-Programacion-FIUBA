#include <stdio.h>
#include <string.h>
#include <stdbool.h>

bool verificar(char vector[] , char caracter , int tamaño ) {
    for (size_t j = 0 ; j < tamaño ; j++) {
        if (vector[j]==caracter) {
            return true;
        }
    }
    return false;
}

char caracteres_repetidos(char cadena[], int tamaño) {
    char auxiliar[tamaño];
    char caracter_repetido="_";
    int veces;
    
    for ( size_t j = 0 ; j < tamaño ; j++) {
        if (verificar(auxiliar , cadena[j] , tamaño) == 0) {
            auxiliar[j]=cadena[j];
        } else {
            auxiliar[j]=" ";
        }
    }
    
    for ( size_t j = 0 ; j < tamaño ; j++) {
        veces=0;
        for ( size_t i = 0 ; i < tamaño ; i++) {
            if (auxiliar[j] == cadena[i]) {
                veces++;
            }
        }
        
        if (veces!=2) {
            return auxiliar[j];
            }
        
    }
    
    return caracter_repetido;
}

int main() {
    char cadena[30];
    char vuelta;
    scanf("%s", cadena);
    vuelta=caracteres_repetidos(cadena , strlen(cadena));
    printf("\n%c" , vuelta);

    return 0;
}