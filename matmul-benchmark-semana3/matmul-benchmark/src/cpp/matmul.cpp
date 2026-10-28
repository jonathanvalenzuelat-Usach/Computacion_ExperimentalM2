// Multiplicación naive de matrices NxN (C++).
// Uso: matmul_cpp <N> <repeticiones> <semilla> <archivo_csv>
#include <chrono>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <fstream>
#include <string>
#include <vector>

// Generador congruencial lineal de 32 bits, idéntico en los cuatro lenguajes.
// Devuelve valores en [0, 1) con 24 bits de precisión (exactos en double).
static uint32_t state;
static inline double next_value() {
    state = state * 1664525u + 1013904223u;
    return static_cast<double>(state >> 8) / 16777216.0;
}

static void fill(std::vector<double>& m) {
    for (double& x : m) x = next_value();
}

// Algoritmo naive: triple bucle i-j-k, matrices en arreglo contiguo por filas.
static void multiply(const double* a, const double* b, double* c, int n) {
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            double sum = 0.0;
            for (int k = 0; k < n; k++) {
                sum += a[i * n + k] * b[k * n + j];
            }
            c[i * n + j] = sum;
        }
    }
}

static double checksum(const std::vector<double>& c) {
    double s = 0.0;
    for (double x : c) s += x;
    return s;
}

static bool file_is_empty(const std::string& path) {
    std::ifstream f(path, std::ios::binary | std::ios::ate);
    return !f.good() || f.tellg() == 0;
}

int main(int argc, char** argv) {
    if (argc != 5) {
        std::fprintf(stderr, "Uso: %s <N> <repeticiones> <semilla> <archivo_csv>\n", argv[0]);
        return 1;
    }
    const int n = std::atoi(argv[1]);
    const int reps = std::atoi(argv[2]);
    state = static_cast<uint32_t>(std::strtoull(argv[3], nullptr, 10));
    const std::string out = argv[4];

    // Creación de matrices: FUERA de la medición.
    std::vector<double> a(static_cast<size_t>(n) * n), b(a.size()), c(a.size(), 0.0);
    fill(a);
    fill(b);

    const bool header = file_is_empty(out);
    std::FILE* f = std::fopen(out.c_str(), "a");
    if (!f) { std::fprintf(stderr, "No se pudo abrir %s\n", out.c_str()); return 1; }
    if (header) std::fprintf(f, "language,N,repetition,time_seconds\n");

    double ref = 0.0;
    for (int r = 1; r <= reps; r++) {
        auto t0 = std::chrono::steady_clock::now();
        multiply(a.data(), b.data(), c.data(), n);
        auto t1 = std::chrono::steady_clock::now();
        const double secs = std::chrono::duration<double>(t1 - t0).count();

        const double cs = checksum(c);
        if (r == 1) ref = cs;
        else if (cs != ref) { std::fprintf(stderr, "Checksum inconsistente entre repeticiones\n"); return 2; }

        std::fprintf(f, "cpp,%d,%d,%.9f\n", n, r, secs);
        std::fflush(f);
        std::fprintf(stderr, "[cpp N=%d rep %d/%d] %.6f s\n", n, r, reps, secs);
    }
    std::fclose(f);
    std::printf("CHECKSUM,cpp,%d,%.17g\n", n, ref);
    return 0;
}
