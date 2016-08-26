#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>
#include <assert.h>
#include <stdbool.h>
#include <string.h>


/*Convert a spins vector in {+1, -1} to a hex representation
  spins[0] is MSB
  N:        length of the spin vector
  spins:    vector in {+1, -1}
  hex:      char buffer for writing to
*/
void spins_as_hex(int N, int* spins, char* hex) {

    unsigned hex_digit = 0;
    int i = 0;
    char* j = hex;
    int stop = 0; //end of first digit, if less than 4
    if(N > 4)
        stop = N % 4; 

    while(true) {
        if(spins[i] == 1) {
            hex_digit |= 1;
        }
        i++;
        if(i == N) {
            sprintf(j, "%x", hex_digit);
            break;
        }
        else if(i == stop) {
            sprintf(j, "%x", hex_digit);
            j++;
            hex_digit = 0;
        }
        else if((i > stop) && (((i-stop) % 4) == 0)) {
            sprintf(j, "%x", hex_digit);
            j++;
            hex_digit = 0;
        }
        else
            hex_digit <<= 1;
    }
}

/*write to spins
  spins[0] is MSB
  hex:      string of hex digits
  N:        length of the spins buffer
  spins:    write out to vector in {+1, -1}
*/
void hex_to_spins(int N, char* hex, int* spins) {

    // read the leftmost digit
    // check how many spins it needs to represent
    // write it to spins
    // proceed in groups of 4 going forward
    int stop = N;
    unsigned digit = 0;
    char *k = hex;
    int i = 0;
    char tmp[2];
    tmp[1] = '\0';
    if(N >= 4)
        stop = N % 4;

    while(k != NULL) {

        tmp[0] = *k;
        sscanf(tmp, "%x", &digit);
        k++;
        while(true) {

            if(stop == 0)
                break;

            stop--;
            if((digit >> stop) & 1)
                spins[i] = 1;
            else
                spins[i] = -1;

            i++;
            if(i == N) {
                assert(k != NULL);
                return;
            }
        }
        stop = 4;
    }
}

void printarray(int* arr, int N) {

    for(int i = 0; i < N; i++)
        printf("%d ", arr[i]);
    printf("\n");
}

void test_hex_to_spins(int N, char* hex, int* spins) {

    printf("hex: %s\n", hex);
    printf("expecting: ");
    printarray(spins, N);
    hex_to_spins(N, hex, spins);
    printf("result:    ");
    printarray(spins, N);
    printf("\n");

}

void main() {

    char hex4[2] = "4";
    char hex12[2] = "C";
    char hex18[3] = "12";
    char hex1026[5] = "402";

    int spins4[3] = {1, -1, -1};
    int spins12[4] = {1, 1, -1, -1};
    int spins18[5] = {1, -1, -1, 1, -1};
    int spins1026[11] = {1, -1, -1, -1, -1, -1, -1, -1, -1, 1, -1};

    char tmp4[2];
    char tmp12[2];
    char tmp18[3];
    char tmp1026[5];

    printf("\n********** Testing spins_as_hex *********\n");
    spins_as_hex(3, spins4, tmp4);
    printf("expecting: 4, result: %s\n", tmp4);
    spins_as_hex(4, spins12, tmp12);
    printf("expecting: c (12), results: %s\n", tmp12);
    spins_as_hex(5, spins18, tmp18);
    printf("expecting: 12 (18), results: %s\n", tmp18);
    spins_as_hex(11, spins1026, tmp1026);
    printf("expecting: 402, results: %s\n", tmp1026);
    printf("Testing for overwrites\nexpecting: 0x4, result: %s\n", tmp4);

// 
//     assert(strcmp(hex4, tmp4) == 0);
//     assert(strcmp(hex12, tmp12) == 0);
//     assert(strcmp(hex18, tmp18) == 0);
//     assert(strcmp(hex1026, tmp1026) == 0);


    printf("\n********** Testing hex_to_spins *********\n");
    test_hex_to_spins(3, hex4, spins4);
    test_hex_to_spins(4, hex12, spins12);
    test_hex_to_spins(5, hex18, spins18);
    test_hex_to_spins(11, hex1026, spins1026);

}
