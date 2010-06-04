#include <stdio.h>
#include "test.h"

char * test(char *buf, char *in)
{
  (void)sprintf(buf, "silly %s", in);
  return buf;
}
