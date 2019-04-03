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
    int lo_delta = 1; // Default step. For sample counter in spad step = 1.
    long int hi_delta = 500000000; // 500,000,000
    unsigned xx;
    signed long int xx1 = 0;
    unsigned long long ii = 1;
    unsigned errors = 0;
    unsigned error_report = 0;
    unsigned int aa = 0;

    int opt;
    while((opt = getopt(argc, argv, "m:c:l:h:")) != -1)
    {
      switch(opt) {
        case 'm':
          maxcols = atoi(optarg);
          printf("m = %i\n", atoi(optarg));
          break;
        case 'c':
          countcol = atoi(optarg);
          printf("c = %i\n", atoi(optarg));
          break;
        case 'l':
          lo_delta = atoi(optarg);
          printf("l = %i\n", atoi(optarg));
          break;
        case 'h':
          hi_delta = atoi(optarg);
          printf("h = %i\n", atoi(optarg));
        default:
          printf("No args given %d \n", opt);
          break;
      }
    }
    long signed buffer[maxcols];
    while(1) {

      fread(buffer, sizeof(unsigned), maxcols, stdin); // read 104 channels of data.
      aa = buffer[countcol];
      if (ii == 1) { // if first loop: skip
          ii++;
          xx1 = aa;
          continue;
      }
      if (aa == xx1 + lo_delta) {
      } else {
        //printf("Sample now: %d, sample before: %d, delta = %d \n", aa, xx1, aa - xx1);

        if (abs(aa - xx1) < lo_delta || abs(aa - xx1) > hi_delta){
          // if (aa == xx1) {

          printf("Loop = %d, last sample = %d, current sample = %d\n" , ii, xx1, aa);
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
