#include <unistd.h>
#include <stdio.h>
/*
 * This file takes input from nc as below:
 * nc acq2106_112 4210 | ./isramp
 */
int main(int argc, char *argv[]) {

    int maxcols = 104; // Number of columns of data
    int countcol = 96; // Column where the ramp is
    unsigned xx;
    int xx1 = 0;
    unsigned long long ii = 1;
    unsigned errors = 0;
    unsigned error_report = 0;
    unsigned int aa = 0;
    unsigned buffer[104];
    int opt;
    while((opt = getopt(argc, argv, ":if:mc")) != -1)
    {
      switch(opt) {
        case 'm':
          maxcols = opt;
          break;
        case 'c':
          countcol = opt;
          break;
        default:
          printf("No args given %d \n", opt);
          break;
      }
    }

    while(1) {

      fread(buffer, sizeof(unsigned), 104, stdin); // read 104 channels of data.
      aa = buffer[96];

      if (aa == xx1 + 1) {
      } else {
        if (aa != xx1 + 1){
          if (++error_report < 100000){

            printf("%012llx 0x%08x 0x%08x **ERROR** Sample jump: %d\n",
            ii, xx1, aa, aa - xx1);
            }
          ++errors;
        }else{

          error_report = 0;
        }
      }

      if (ii % 100000 == 0) {
      printf("Loops completed = %d \n \n", ii);
      }
      ii++;
      xx1 = aa;
      }
      return 0;
}
