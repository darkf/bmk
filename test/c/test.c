#include <stdio.h>
#include "test.h"

int main(int argc, char *argv[])
{
  char buf[32];
  printf("Hello, %s!\n", test(buf, argv[1]));
  return 0;
}
