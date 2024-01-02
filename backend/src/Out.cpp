/* ----- HEADER ----- */
#include <stdio.h>

float heap[30101999];
float stack[30101999];
float P;
float H;
float t0, t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12, t13, t14, t15, t16, t17;

/* ----- FUNCTIONS ----- */
void factorial() {
	/* ------- Declaración ------- */
	t0 = P + 2;
	t1 = H;
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
	stack[(int) t0] = t1;
	/* ----- Fin Declaración ----- */
	/* ------- Asignacion -------- */
	t2 = P + 2;
	stack[(int) t2] = 1;
	/* ----- Fin Asignacion ------ */
	/* --------- While ----------- */
	/* --------- Acceso ---------- */
	t3 = P + 1;
	t4 = stack[(int) t3];
	/* ------- Fin Acceso -------- */
	if(t4 >= 1) goto L0;
	goto L1;
L0:
	/* ------- Asignacion -------- */
	/* --------- Acceso ---------- */
	t5 = P + 2;
	t6 = stack[(int) t5];
	/* ------- Fin Acceso -------- */
	/* --------- Acceso ---------- */
	t7 = P + 1;
	t8 = stack[(int) t7];
	/* ------- Fin Acceso -------- */
	t9 = t6 * t8;
	t10 = P + 2;
	stack[(int) t10] = t9;
	/* ----- Fin Asignacion ------ */
	/* ------- Asignacion -------- */
	/* --------- Acceso ---------- */
	t11 = P + 1;
	t12 = stack[(int) t11];
	/* ------- Fin Acceso -------- */
	t13 = t12 - 1;
	t14 = P + 1;
	stack[(int) t14] = t13;
	/* ----- Fin Asignacion ------ */
L1:
	/* ------- Fin While --------- */
	/* ---------- Print ---------- */
	/* --------- Acceso ---------- */
	t15 = P + 2;
	t16 = stack[(int) t15];
	/* ------- Fin Acceso -------- */
	printf("%d", (int) t16);
	printf("%c", (char) 10);
	/* -------- Fin Print -------- */
L2:
	return;
}

/* ------ MAIN ------ */
int main() {
	P = 0;
	H = 0;
	/* ----- Llamada Funcion ----- */
	/* ------- Parametros -------- */
	t17 = P + 1;
	stack[(int) t17] = 2;
	/* ----- Fin Parametros ------ */
	P = P + 0;
	factorial();
	t17 = stack[(int) P];
	P = P - 0;
	/* --- Fin Llamada Funcion --- */
	return 0;
}