#include <stdio.h>
#include <string.h>

int obscure_function(char * input);

int main(int argc, char * argv[]){
    if (argc != 2){
        printf("USAGE: %s <string_input>\n",argv[0]);
        return 1;
    }

   char * input = argv[1];
   if (obscure_function(input) == 0x5A){
       printf("Congrats!");
   }
   else{
       printf(":(");
   }
   return 0;
}
int obscure_function(char * input){
    int result = 0;
    for (int i = 0; i < strlen(input); ++i) {
        result ^= input[i];
        result = (result + i) & 0xff;
    }
    return result;
}
