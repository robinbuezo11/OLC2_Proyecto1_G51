/* ----- HEADER ----- */
#include <stdio.h>

float heap[30101999];
float stack[30101999];
float P;
float H;
float t0, t1, t2, t3, t4, t5;

/* ------ NATIVES ------ */
void _printString() {
	t0 = P + 1;
	t1 = stack[(int) t0];
L0:
	t2 = heap[(int) t1];
	if(t2 == -1) goto L1;
	printf("%c", (char) t2);
	t1 = t1 + 1;
	goto L0;
L1:
	return;
}

/* ------ MAIN ------ */
int main() {
	P = 0;
	H = 0;
	/* ---------- Print ---------- */
	printf("%d", (int) 12);
	printf("%c", (char) 10);
	/* -------- Fin Print -------- */
	/* ---------- Print ---------- */
	printf("%f", (float) 3.14);
	printf("%c", (char) 10);
	/* -------- Fin Print -------- */
	/* ---------- Print ---------- */
	printf("%d", (int) 15);
	printf("%c", (char) 10);
	/* -------- Fin Print -------- */
	/* ---------- Print ---------- */
	t3 = H;
	heap[(int) H ] = 72;
	H = H + 1;
	heap[(int) H ] = 111;
	H = H + 1;
	heap[(int) H ] = 108;
	H = H + 1;
	heap[(int) H ] = 97;
	H = H + 1;
	heap[(int) H ] = -1;
	H = H + 1;
	t4 = P + 0;
	t5 = t4 + 1;
	stack[(int) t4] = t3;
	P = P + 0;
	_printString();
	t5 = stack[(int) P];
	P = P - 0;
	printf("%c", (char) 10);
	/* -------- Fin Print -------- */
	return 0;
}