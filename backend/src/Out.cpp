/* ----- HEADER ----- */
#include <stdio.h>

float heap[30101999];
float stack[30101999];
float P;
float H;
float t0;

/* ------ MAIN ------ */
int main() {
	P = 0;
	H = 0;
	/* ------- Declaración ------- */
	t0 = H;
	heap[(int) H ] = 78;
	H = H + 1;
	heap[(int) H ] = 85;
	H = H + 1;
	heap[(int) H ] = 76;
	H = H + 1;
	heap[(int) H ] = 76;
	H = H + 1;
	heap[(int) H ] = -1;
	H = H + 1;
	stack[(int) 0] = t0;
	/* ----- Fin Declaración ----- */
	return 0;
}