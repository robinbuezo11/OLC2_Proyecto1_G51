/* ----- HEADER ----- */
#include <stdio.h>

float heap[30101999];
float stack[30101999];
float P;
float H;
float t0, t1, t2, t3, t4, t5, t6, t7, t8;

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
	/* ---------- Print ---------- */
	/* --------- Acceso ---------- */
	t1 = stack[(int) 0];
	/* ------- Fin Acceso -------- */
	printf("%c", (char) 78);
	printf("%c", (char) 85);
	printf("%c", (char) 76);
	printf("%c", (char) 76);
	printf("%c", (char) 10);
	/* -------- Fin Print -------- */
	/* ------- Asignacion -------- */
	stack[(int) 0] = 0;
	/* ----- Fin Asignacion ------ */
	/* ---------- Print ---------- */
	/* --------- Acceso ---------- */
	t2 = stack[(int) 0];
	/* ------- Fin Acceso -------- */
	printf("%d", (int) t2);
	printf("%c", (char) 10);
	/* -------- Fin Print -------- */
	/* ------- Declaración ------- */
	t3 = H;
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
	stack[(int) 1] = t3;
	/* ----- Fin Declaración ----- */
	/* ---------- Print ---------- */
	/* --------- Acceso ---------- */
	t4 = stack[(int) 1];
	/* ------- Fin Acceso -------- */
	printf("%c", (char) 78);
	printf("%c", (char) 85);
	printf("%c", (char) 76);
	printf("%c", (char) 76);
	printf("%c", (char) 10);
	/* -------- Fin Print -------- */
	/* ------- Asignacion -------- */
	stack[(int) 1] = 0;
	/* ----- Fin Asignacion ------ */
	/* ---------- Print ---------- */
	/* --------- Acceso ---------- */
	t5 = stack[(int) 1];
	/* ------- Fin Acceso -------- */
	printf("%d", (int) t5);
	printf("%c", (char) 10);
	/* -------- Fin Print -------- */
	/* ---------- Print ---------- */
	/* --------- Acceso ---------- */
	t6 = stack[(int) 0];
	/* ------- Fin Acceso -------- */
	/* --------- Acceso ---------- */
	t7 = stack[(int) 1];
	/* ------- Fin Acceso -------- */
	if(t6 == 1) goto L0;
	if(t7 == 1) goto L0;
	goto L1;
L0:
	t8 = 1;
	goto L2;
L1:
	t8 = 0;
L2:
	printf("%d", (int) t8);
	printf("%c", (char) 10);
	/* -------- Fin Print -------- */
	return 0;
}