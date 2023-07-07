#include <stdio.h>

int num1_mayor_num2(int num1,int num2, int vector[]){
    if (num1 > num2){
        int i_max;
        for (size_t i = 0 ; num1 >= num2 ; i++){
            vector[i]=num1;
            num1--;
            i_max=i;
        }
        return i_max+1;

    } else {
        vector[0]=-1;
        return 1;

        }
}

int main(){
    int num1;
    int num2;
    int vector[10000];
    int largo;

    printf("Indique el primer numero:");
    scanf("%d",&num1);

    printf("Indique el segundo numero:");
    scanf("%d",&num2);

    largo=num1_mayor_num2(num1,num2,vector);

    for (size_t j = 0 ; j < largo ; j++ ) {
        printf("\n%d",*(vector+j));
    };

    return 0;
}