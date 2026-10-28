# Benchmark reproducible de multiplicación de matrices NxN en C++, Go, Java y Python

**Autor:** Jonathan Alexis Valenzuela Tapia
**Programa:** Doctorado en Ingeniería en Informática, Universidad de Santiago de Chile (USACH)
**Curso:** Experimentación Computacional, módulo *Documentación de experimentos (Reproducibilidad y Replicabilidad)*
**Estado:** Semana 2, implementación y ejecución del experimento (versión 0.2)

---

## 1. Objetivo

Diseñar y desarrollar un experimento computacional **reproducible** que compare el tiempo de ejecución del algoritmo *naive* de multiplicación de matrices cuadradas NxN implementado en C++, Go, Java y Python, siguiendo los principios de [ACM Artifact Review and Badging](https://www.acm.org/publications/policies/artifact-review-and-badging-current).

> *Algoritmo naive:* versión más directa de la multiplicación de matrices (triple bucle `i-j-k`, complejidad O(N³)), sin optimizaciones especiales ni bibliotecas de álgebra lineal.

## 2. Pregunta de investigación

¿Existen diferencias estadísticamente significativas en el tiempo de ejecución del algoritmo naive de multiplicación de matrices NxN entre implementaciones equivalentes desarrolladas en C++, Go, Java y Python, y cómo varían estas diferencias según el tamaño de la matriz?

## 3. Hipótesis

- **H0:** el lenguaje de implementación no produce diferencias estadísticamente significativas en el tiempo de ejecución.
- **H1:** al menos uno de los lenguajes presenta un tiempo de ejecución significativamente diferente de los demás.

Sobre la interacción (segunda parte de la pregunta):

- **H0 de interacción:** el efecto del lenguaje no depende del tamaño N.
- **H1 de interacción:** el efecto del lenguaje depende de N (interacción lenguaje × N).

Nivel de significancia: α = 0,05.

## 4. Variables

| Tipo | Variable | Valores |
|---|---|---|
| Independiente | Lenguaje de implementación | C++, Go, Java, Python |
| Independiente | Tamaño de la matriz (N) | 500, 1000, 1500 |
| Dependiente | Tiempo de ejecución (`time_seconds`) | Segundos, medido solo sobre la multiplicación |
| Controladas | Algoritmo, tipo de dato, matrices de entrada, criterio de medición, máquina, versiones | Ver sección 6 |

## 5. Diseño experimental

- **Diseño:** factorial completo 4 (lenguajes) × 3 (tamaños) = 12 condiciones.
- **Repeticiones:** 10 por combinación de lenguaje y tamaño (120 mediciones en total).
- **Aleatorización:** el orden de ejecución de los 12 bloques (lenguaje, N) se baraja con la semilla fija 42 (`scripts/gen_order.py`), para repartir posibles efectos de deriva térmica o carga externa.
- **Validación de correctitud:** cada ejecución calcula un *checksum* (suma de los elementos de C) y `scripts/verify.py` comprueba que los cuatro lenguajes obtienen el mismo valor.

## 6. Implementación (Semana 2)

### 6.1 Equivalencia funcional entre lenguajes

| Aspecto | Decisión | Justificación |
|---|---|---|
| Algoritmo | Triple bucle `i-j-k`, acumulando en una variable local y asignando `C[i][j]` al final | El mismo orden de operaciones en los cuatro lenguajes |
| Tipo de dato | `double` (64 bits) | Mismo tipo y precisión |
| Almacenamiento | Arreglo (lista en Python) contiguo por filas, con índice `i*N+k` | Misma disposición en memoria y misma aritmética de índices |
| Datos de entrada | Generador congruencial lineal de 32 bits (`s = s·1664525 + 1013904223 mod 2³²`, valor = `(s >> 8) / 2²⁴`), semilla 42 | Aritmética entera exacta, por lo que A y B son idénticas en los cuatro lenguajes |
| Librerías | Ninguna de multiplicación de matrices (Python sin NumPy) | Requisito del módulo |
| Hilos | Un solo hilo | Implementación secuencial, sin paralelismo |
| Compilación C++ | `g++ -O2 -std=c++17 -ffp-contract=off` | Optimización estándar; la última bandera evita fusionar multiplicación y suma (FMA) |
| Compilación Go | `go build` | Valores por defecto; `float64(a*b)` explícito para impedir la fusión FMA |
| Java | `javac` / `java` sin banderas | Valores por defecto de la JVM |
| Python | CPython, sin extensiones | Intérprete estándar |

### 6.2 Criterio de medición

- Las matrices A y B se generan **por completo antes** de iniciar el temporizador; la matriz resultado C se reserva e inicializa en cero también antes.
- El temporizador **parte inmediatamente antes** de llamar a la función de multiplicación y **termina al volver** de ella (matriz resultante obtenida).
- Relojes monotónicos en cada lenguaje: `std::chrono::steady_clock` (C++), `time.Now()` / `time.Since()` (Go), `System.nanoTime()` (Java) y `time.perf_counter()` (Python).
- Cada combinación (lenguaje, N) se ejecuta en **un proceso**, con 10 repeticiones consecutivas sobre las mismas matrices. Se registran las 10, sin descartar ninguna. Esto implica que en Java la primera repetición puede incluir efectos de compilación JIT; se trata como parte de la variabilidad observada y se discute en la sección 11.

### 6.3 Formato de resultados

Cada lenguaje escribe su propio archivo (`results/cpp.csv`, `go.csv`, `java.csv`, `python.csv`) con la misma estructura:

```csv
language,N,repetition,time_seconds
cpp,500,1,0.078512345
```

| Columna | Significado |
|---|---|
| `language` | Lenguaje utilizado (`cpp`, `go`, `java`, `python`) |
| `N` | Tamaño de la matriz |
| `repetition` | Número de la ejecución (1 a 10) |
| `time_seconds` | Tiempo de la multiplicación, en segundos, con 9 decimales |

Además se genera `results/checksums.txt` (un valor por lenguaje y tamaño) y `results/summary.md` (estadística descriptiva).

## 7. Estructura del repositorio

```
.
├── README.md
├── src/
│   ├── cpp/matmul.cpp
│   ├── go/matmul.go  (+ go.mod)
│   ├── java/MatMul.java
│   └── python/matmul.py
├── scripts/
│   ├── run_all.sh          # compila y ejecuta todo el experimento
│   ├── gen_order.py        # orden aleatorizado de los bloques
│   ├── record_env.py       # registra el entorno de ejecución
│   ├── verify.py           # valida los CSV y compara checksums
│   └── summarize.py        # estadística descriptiva
└── results/
    ├── cpp.csv  go.csv  java.csv  python.csv
    ├── checksums.txt  summary.md
    └── environment.json  environment.md
```

## 8. Cómo ejecutar

**Requisitos (Linux, macOS o WSL):** `g++` (C++17), Go 1.21 o superior, JDK 17 o superior (`javac` y `java`) y Python 3.8 o superior. Con las herramientas ya instaladas, basta un comando:

```bash
./scripts/run_all.sh
```

El script compila, registra el entorno, ejecuta los 12 bloques en orden aleatorizado, valida los resultados y muestra el resumen. Para una prueba rápida:

```bash
SIZES="100 200" REPS=3 ./scripts/run_all.sh
```

Variables opcionales: `SEED` (por defecto 42), `REPS` (10), `SIZES` ("500 1000 1500") y `LANGS_ONLY` (por ejemplo `"cpp go"`).

**Duración estimada:** en una prueba preliminar, Python tardó unos 11 s por repetición con N = 500, y su tiempo crece de forma cúbica. Se espera que el experimento completo demore entre 1,5 y 2 horas, casi todo en Python con N = 1000 y N = 1500. Conviene ejecutarlo con el equipo enchufado y sin otras tareas pesadas.

## 9. Entorno de ejecución

Equipo utilizado para todas las mediciones: **HP EliteBook 840 G8 Notebook PC**. El experimento se ejecutó de forma **nativa en Windows 11** (sin WSL ni contenedores). Los datos del entorno de software los registró `scripts/record_env.py` el 2026-10-21 (UTC) en `results/environment.md`.

| Característica | Valor |
|---|---|
| Procesador | 11th Gen Intel(R) Core(TM) i7-1165G7 @ 2.80 GHz |
| Núcleos lógicos | 8 (4 núcleos físicos según la especificación del fabricante) |
| RAM | 16,0 GB instalados (15,7 GB utilizables), 3200 MT/s |
| Sistema operativo | Windows 11 Pro, versión 26H2, compilación 26300.9711 |
| Arquitectura | 64 bits, x64 (AMD64) |
| g++ | g++ (MinGW-W64 x86_64-ucrt-posix-seh, built by Brecht Sanders, r2) 16.2.0 |
| Go | go1.27.0 windows/amd64 |
| Java | OpenJDK 21.0.12.1 LTS (javac 21.0.12.1) |
| Python | 3.14.7 (CPython) |

**Opciones de compilación y ejecución:**

| Lenguaje | Opciones |
|---|---|
| C++ | `g++ -O2 -std=c++17 -ffp-contract=off` |
| Go | `go build` (valores por defecto) |
| Java | `javac` / `java` (valores por defecto) |
| Python | CPython sin extensiones, sin NumPy |

## 10. Primeros resultados

Ejecución completa (4 lenguajes × 3 tamaños × 10 repeticiones = 120 mediciones) en el equipo descrito en la sección 9. Datos crudos en `results/cpp.csv`, `go.csv`, `java.csv` y `python.csv`; estadística descriptiva en `results/summary.md`.

| N | Lenguaje | Media (s) | Desv. est. (s) | Razón respecto de C++ |
|---|---|---|---|---|
| 500 | C++ | 0,1012 | 0,0002 | 1,00 |
| 500 | Go | 0,1117 | 0,0043 | 1,10 |
| 500 | Java | 0,1101 | 0,0014 | 1,09 |
| 500 | Python | 10,2099 | 0,0835 | 100,9 |
| 1000 | C++ | 0,9430 | 0,0022 | 1,00 |
| 1000 | Go | 1,0630 | 0,0058 | 1,13 |
| 1000 | Java | 1,4950 | 0,0141 | 1,59 |
| 1000 | Python | 90,9261 | 0,1993 | 96,4 |
| 1500 | C++ | 4,3470 | 0,4513 | 1,00 |
| 1500 | Go | 7,7272 | 0,6461 | 1,78 |
| 1500 | Java | 4,5887 | 0,0857 | 1,06 |
| 1500 | Python | 350,8686 | 3,2535 | 80,7 |

**Lectura preliminar (sin pruebas de significancia, que se harán en la semana 4):**

- Python es entre 80 y 100 veces más lento que C++ en los tres tamaños, una diferencia muy superior a la variabilidad entre repeticiones.
- Entre C++, Go y Java las diferencias son pequeñas en N = 500 y cambian de orden según N: Java queda más lejos de C++ en N = 1000 (1,59×) y casi empata en N = 1500 (1,06×), mientras que Go se aleja en N = 1500 (1,78×).
- El tiempo crece aproximadamente de forma cúbica con N en Python (×8,9 de 500 a 1000 y ×3,9 de 1000 a 1500, frente a ×8 y ×3,4 teóricos). En C++, Go y Java las razones se desvían más del valor teórico, lo que sugiere efectos de memoria caché y de otro tipo que habrá que analizar.
- En N = 1500, C++ y Go muestran una variabilidad mayor (coeficiente de variación de 10 % y 8 %), con las primeras repeticiones más lentas que las últimas.

## 11. Análisis estadístico planificado (Semana 4)

1. Integración de los cuatro CSV en `benchmark.csv`.
2. Estadística descriptiva por condición y gráficos de caja.
3. Verificación de supuestos: normalidad (Shapiro-Wilk) y homogeneidad de varianzas (Levene), con transformación logarítmica si corresponde.
4. ANOVA de dos factores con interacción (lenguaje y N).
5. Comparaciones post-hoc con Tukey HSD, cuando corresponda.
6. Análisis de escalamiento: ajuste de `log(tiempo)` vs `log(N)` por lenguaje, contrastado con O(N³).

## 12. Alineación con ACM Artifact Review and Badging

Las insignias de ACM se otorgan a artículos de sus publicaciones; en este módulo se usan sus criterios como marco de referencia.

| Insignia | Cómo se aborda | Alcance |
|---|---|---|
| **Artifacts Available** | Publicación en un repositorio de archivo con DOI (Zenodo). GitHub por sí solo no basta | Semana 5 |
| **Evaluated: Functional** | Artifact documentado, consistente, completo y ejecutable, con evidencia de verificación (checksums) | Semana 3 |
| **Evaluated: Reusable** | Documentación cuidada, pipeline Snakemake y estructura que facilite la reutilización | Semana 4 |
| **Results Reproduced** | Un compañero obtiene resultados equivalentes usando el artifact publicado | Evaluación cruzada, semana 5 |
| **Results Replicated** | Otro equipo obtiene los resultados con una implementación desarrollada de forma independiente | Fuera del alcance del módulo |

Según ACM, no se exige un resultado idéntico, sino acuerdo dentro de una tolerancia aceptable que no cambie las conclusiones. Con tiempos de ejecución, se espera coincidencia en el orden entre lenguajes y en la significancia estadística, no en los segundos exactos.

## 13. Amenazas a la validez y limitaciones

- **Validez interna:** el JIT de Java (sobre todo en la primera repetición de cada bloque), el recolector de basura y la frecuencia de la CPU añaden ruido. Se mitigan con orden aleatorizado, matrices fijas y registro del entorno.
- **Validez de constructo:** el algoritmo naive mide más la calidad del compilador y del runtime que la "velocidad del lenguaje". Las conclusiones se limitan a estas implementaciones y versiones. El nivel de optimización de C++ (`-O2`) condiciona el resultado.
- **Validez externa:** los resultados dependen de la arquitectura y del sistema operativo.
- **Muestra:** 10 repeticiones por condición dan pocos datos para estimar la variabilidad.
- **Variabilidad observada:** en N = 1500, C++ y Go presentan repeticiones iniciales más lentas que las finales. Puede deberse a la frecuencia de la CPU o a procesos en segundo plano del sistema operativo; no se ha podido confirmar.
- **Costo:** Python puro con N = 1500 es mucho más lento que el resto y domina el tiempo total de ejecución.

## 14. Cronograma del módulo

| Semana | Entregable |
|---|---|
| 1 | Repositorio y README inicial: diseño experimental |
| 2 | Implementación y ejecución: cuatro CSV por lenguaje y registro del entorno (este documento) |
| 3 | Entornos Docker y evaluación funcional del artifact |
| 4 | Pipeline Snakemake y análisis estadístico (ANOVA de dos factores, Tukey HSD) |
| 5 | Publicación en Zenodo (DOI) y evaluación cruzada |

## 15. Licencia y citación

_Por definir (se sugiere MIT para el código y CC-BY 4.0 para los datos y la documentación)._

## 16. Referencias

- Association for Computing Machinery. *Artifact Review and Badging, Version 1.1.* https://www.acm.org/publications/policies/artifact-review-and-badging-current
