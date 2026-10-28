// Multiplicación naive de matrices NxN (Go).
// Uso: matmul_go <N> <repeticiones> <semilla> <archivo_csv>
package main

import (
	"fmt"
	"os"
	"strconv"
	"time"
)

// Generador congruencial lineal de 32 bits, idéntico en los cuatro lenguajes.
var state uint32

func nextValue() float64 {
	state = state*1664525 + 1013904223
	return float64(state>>8) / 16777216.0
}

func fill(m []float64) {
	for i := range m {
		m[i] = nextValue()
	}
}

// Algoritmo naive: triple bucle i-j-k, matrices en arreglo contiguo por filas.
// La conversión explícita float64(...) impide que el compilador fusione la
// multiplicación y la suma en una instrucción FMA (en algunas arquitecturas),
// de modo que el redondeo sea el mismo que en los otros lenguajes.
func multiply(a, b, c []float64, n int) {
	for i := 0; i < n; i++ {
		for j := 0; j < n; j++ {
			sum := 0.0
			for k := 0; k < n; k++ {
				sum += float64(a[i*n+k] * b[k*n+j])
			}
			c[i*n+j] = sum
		}
	}
}

func checksum(c []float64) float64 {
	s := 0.0
	for _, x := range c {
		s += x
	}
	return s
}

func fail(msg string, code int) {
	fmt.Fprintln(os.Stderr, msg)
	os.Exit(code)
}

func main() {
	if len(os.Args) != 5 {
		fail("Uso: matmul_go <N> <repeticiones> <semilla> <archivo_csv>", 1)
	}
	n, _ := strconv.Atoi(os.Args[1])
	reps, _ := strconv.Atoi(os.Args[2])
	seed, _ := strconv.ParseUint(os.Args[3], 10, 64)
	state = uint32(seed)
	out := os.Args[4]

	// Creación de matrices: FUERA de la medición.
	a := make([]float64, n*n)
	b := make([]float64, n*n)
	c := make([]float64, n*n)
	fill(a)
	fill(b)

	info, err := os.Stat(out)
	header := err != nil || info.Size() == 0
	f, err := os.OpenFile(out, os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0o644)
	if err != nil {
		fail("No se pudo abrir "+out, 1)
	}
	defer f.Close()
	if header {
		fmt.Fprintln(f, "language,N,repetition,time_seconds")
	}

	ref := 0.0
	for r := 1; r <= reps; r++ {
		t0 := time.Now()
		multiply(a, b, c, n)
		secs := time.Since(t0).Seconds()

		cs := checksum(c)
		if r == 1 {
			ref = cs
		} else if cs != ref {
			fail("Checksum inconsistente entre repeticiones", 2)
		}

		fmt.Fprintf(f, "go,%d,%d,%.9f\n", n, r, secs)
		fmt.Fprintf(os.Stderr, "[go N=%d rep %d/%d] %.6f s\n", n, r, reps, secs)
	}
	fmt.Printf("CHECKSUM,go,%d,%s\n", n, strconv.FormatFloat(ref, 'g', 17, 64))
}
