/* arraySum.c uses an array to sum the values in an input file,
 *  whose name is specified on the command-line.
 * Huib Aldewereld, HU, HPP, 2020
 */

#include <stdio.h>      /* I/O stuff */
#include <stdlib.h>     /* calloc, etc. */
#include <omp.h>

void readArray(char * fileName, double ** a, int * n);
double sumArray(double * a, int numValues) ;

int main(int argc, char * argv[])
{
  int  howMany;
  double sum;
  double * a;
  double start;
  doubel end; 
  
  int threads[] = {1,2,4,8};
  //Bron: https://flaviocopes.com/c-array-length/
  int size = sizeof threads/ sizeof threads[0]; 

  if (argc != 2) {
    fprintf(stderr, "\n*** Usage: arraySum <inputFile>\n\n");
    exit(1);
  }
  
  readArray(argv[1], &a, &howMany);
  for (int n = 0; n < size ; n++){
	omp_set_num_threads(threads[n]);
	
	#pragma omp parallel 

	start = omp_get_wtime();
  	sum = sumArray(a, howMany);
	end = omp_get_wtime();

	printf("Elasped time = %f sec\n", end - start);
}
  free(a);

  return 0;
}

/* readArray fills an array with values from a file.
 * Receive: fileName, a char*,
 *          a, the address of a pointer to an array,
 *          n, the address of an int.
 * PRE: fileName contains N, followed by N double values.
 * POST: a points to a dynamically allocated array
 *        containing the N values from fileName
 *        and n == N.
 */

void readArray(char * fileName, double ** a, int * n) {
  int count, howMany;
  double * tempA;
  FILE * fin;

  fin = fopen(fileName, "r");
  if (fin == NULL) {
    fprintf(stderr, "\n*** Unable to open input file '%s'\n\n",
                     fileName);
    exit(1);
  }

  fscanf(fin, "%d", &howMany);
  tempA = calloc(howMany, sizeof(double));
  if (tempA == NULL) {
    fprintf(stderr, "\n*** Unable to allocate %d-length array",
                     howMany);
    exit(1);
  }

  for (count = 0; count < howMany; count++)
   fscanf(fin, "%lf", &tempA[count]);

  fclose(fin);

  *n = howMany;
  *a = tempA;
}

/* sumArray sums the values in an array of doubles.
 * Receive: a, a pointer to the head of an array;
 *          numValues, the number of values in the array.
 * Return: the sum of the values in the array.
 */

double sumArray(double * a, int numValues) {
  int i;
  double result = 0.0;
  // Bron: https://pages.tacc.utexas.edu/~eijkhout/pcse/html/omp-reduction.html
  #pragma omp parallel for reduction(+:result)

  for (i = 0; i < numValues; i++) {
    result += a[i];
  }

  return result;
}

