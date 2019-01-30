#include <unistd.h>
#include <stdio.h>

int main(int argc, char* argv[]) {

    unsigned xx;
    int xx1 = 0;
    unsigned long long ii = 1;
    unsigned errors = 0;
    unsigned error_report = 0;
    unsigned int aa = 0;
    char buffer[416];

    while(1) {

      fread(buffer, sizeof(char), 416, stdin); // read 104 channels of data.
      aa = *(int*)&buffer[384];

      if (aa == xx1 + 1) {
      } else {
        if (aa != xx1 + 1){
          if (++error_report < 100000){

            printf("%012llx 0x%08x 0x%08x ** ERROR **\n",
            ii, xx1, xx);
            printf("Failed at sample number: %d \n", ii);
            printf("Sample jump: %d \n \n", aa - xx1);
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
