// Multiplicación naive de matrices NxN (Java).
// Uso: java MatMul <N> <repeticiones> <semilla> <archivo_csv>
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.Locale;

public class MatMul {
    // Generador congruencial lineal de 32 bits, idéntico en los cuatro lenguajes.
    private static long state;

    private static double nextValue() {
        state = (state * 1664525L + 1013904223L) & 0xFFFFFFFFL;
        return (double) (state >>> 8) / 16777216.0;
    }

    private static void fill(double[] m) {
        for (int i = 0; i < m.length; i++) m[i] = nextValue();
    }

    // Algoritmo naive: triple bucle i-j-k, matrices en arreglo contiguo por filas.
    private static void multiply(double[] a, double[] b, double[] c, int n) {
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

    private static double checksum(double[] c) {
        double s = 0.0;
        for (double x : c) s += x;
        return s;
    }

    public static void main(String[] args) throws IOException {
        if (args.length != 4) {
            System.err.println("Uso: java MatMul <N> <repeticiones> <semilla> <archivo_csv>");
            System.exit(1);
        }
        int n = Integer.parseInt(args[0]);
        int reps = Integer.parseInt(args[1]);
        state = Long.parseLong(args[2]) & 0xFFFFFFFFL;
        File out = new File(args[3]);

        // Creación de matrices: FUERA de la medición.
        double[] a = new double[n * n];
        double[] b = new double[n * n];
        double[] c = new double[n * n];
        fill(a);
        fill(b);

        boolean header = !out.exists() || out.length() == 0;
        double ref = 0.0;
        try (FileWriter w = new FileWriter(out, true)) {
            if (header) w.write("language,N,repetition,time_seconds\n");
            for (int r = 1; r <= reps; r++) {
                long t0 = System.nanoTime();
                multiply(a, b, c, n);
                long t1 = System.nanoTime();
                double secs = (t1 - t0) / 1e9;

                double cs = checksum(c);
                if (r == 1) ref = cs;
                else if (cs != ref) {
                    System.err.println("Checksum inconsistente entre repeticiones");
                    System.exit(2);
                }

                w.write(String.format(Locale.ROOT, "java,%d,%d,%.9f", n, r, secs) + "\n");
                w.flush();
                System.err.println(String.format(Locale.ROOT, "[java N=%d rep %d/%d] %.6f s", n, r, reps, secs));
            }
        }
        System.out.println("CHECKSUM,java," + n + "," + Double.toString(ref));
    }
}
