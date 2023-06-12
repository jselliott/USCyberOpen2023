#include <stdio.h>
#include <string.h>

int main() {

    int i;
    char input[64];
    char flag[] = {94,88,72,76,112,70,68,93,58,101,84,59,101,84,126,123,84,127,99,56,84,120,104,59,121,56,105,59,63,121,111,118,0};

    fputs("What is the flag? ", stdout);
    fgets(input,sizeof(input)-1, stdin);

    for(i = 0; i < strlen(flag); i++){
        char x = input[i]^0x0b;
        if(x != flag[i]){
            fputs("Wrong!",stdout);
            return 0;
        }
    }
    fputs("Correct! Good job!",stdout);

    return 0;
}