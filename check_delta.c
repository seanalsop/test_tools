#include <unistd.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
/*
 * This file takes input from nc as below:
 * nc acq2106_112 4210 | pv | ./isramp
 */
int main(int argc, char *argv[]) {

    int maxcols = 104; // Number of columns of data
    int countcol = 96; // Column where the ramp is
    int delta = 1; // Default step. For sample counter in spad step = 1.
    unsigned xx;
    int xx1 = 0;
    unsigned long long ii = 1;
    unsigned errors = 0;
    unsigned error_report = 0;
    unsigned int aa = 0;

    int opt;
    while((opt = getopt(argc, argv, "m:c:d:")) != -1)
    {
      switch(opt) {
        case 'm':
          maxcols = atoi(optarg);
          printf("%i\n", atoi(optarg));
          break;
        case 'c':
          countcol = atoi(optarg);
          printf("%i\n", atoi(optarg));
          break;
        case 'd':
          delta = atoi(optarg);
          printf("%i\n", atoi(optarg));
          break;
        default:
          printf("No args given %d \n", opt);
          break;
      }
    }
    unsigned buffer[maxcols];
    while(1) {

      fread(buffer, sizeof(unsigned), maxcols, stdin); // read 104 channels of data.
      aa = buffer[countcol];

      if (aa == xx1 + delta) {
      } else {
        if (abs(aa - xx1) > delta){
          // if (aa == xx1) {
          printf("Loop = %d, last sample = %d, current sample = %d, delta = %d \n" , ii, xx1, aa, delta);
          if (++error_report < 100000){

            printf("%012llx 0x%08x 0x%08x **ERROR** Sample jump: %d\n",
            ii, xx1, aa, aa - xx1);
            }
          ++errors;
        }else{

          error_report = 0;
        }
      }

      ii++;
      xx1 = aa;
      }
      return 0;
}
