#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include "deps/b64/b64.h"

int main()
{
    char *msg = "R29vZCBKb2IhIFRoZSBmbGFnIGlzOiBVU0NHe2YxeDNkX3RoM19qdW04bDM1fQ==";
    char *dec = b64_decode(msg, strlen(msg));

    printf("%s\n", dec);

   return 0;
}