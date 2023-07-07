#include <stdio.h>
#include <stdbool.h>

bool ksum(int vector[], int tamaño, int k) {
    int num1;
    for (size_t i= 0 ; i < tamaño ; i++) {
        num1=vector[i];
        for (size_t j=0 ; j < tamaño ; j++) {
            if (vector[i] + vector[j] == k && i != j) {
                return true;
            }
        }

    }
}

int main() {
    int vector[9]={1,2,3,4,5,6,7,8,9};
    bool mostrar;
    int k=5;
    mostrar=ksum(vector,sizeof(vector)/sizeof(int),k);
    printf("%d",mostrar);
    return 0;
}