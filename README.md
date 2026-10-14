# Benchmark reproducible de multiplicación de matrices NxN en C++, Go, Java y Python

**Autor:** Jonathan Alexis Valenzuela Tapia
**Programa:** Doctorado en Ingeniería en Informática, Universidad de Santiago de Chile (USACH)
**Curso:** Experimentación Computacional, módulo *Documentación de experimentos (Reproducibilidad y Replicabilidad)*
**Estado:** Semana 1, diseño experimental y documentación inicial del artifact (versión 0.1)

---

## 1. Objetivo

Diseñar y desarrollar un experimento computacional **reproducible** que compare el tiempo de ejecución del algoritmo *naive* de multiplicación de matrices cuadradas NxN implementado en C++, Go, Java y Python, siguiendo los principios de reproducibilidad y replicabilidad de [ACM Artifact Review and Badging](https://www.acm.org/publications/policies/artifact-review-and-badging-current).

> *Algoritmo naive:* versión más directa de la multiplicación de matrices (triple bucle `i-j-k`, complejidad O(N³)), sin optimizaciones especiales como bloqueo por caché, vectorización explícita, paralelismo ni bibliotecas de álgebra lineal.

## 2. Pregunta de investigación

¿Existen diferencias estadísticamente significativas en el tiempo de ejecución del algoritmo naive de multiplicación de matrices NxN entre implementaciones equivalentes desarrolladas en C++, Go, Java y Python, y cómo varían estas diferencias según el tamaño de la matriz?

## 3. Hipótesis

- **H0:** el lenguaje de implementación no produce diferencias estadísticamente significativas en el tiempo de ejecución del algoritmo de multiplicación de matrices.
- **H1:** al menos uno de los lenguajes presenta un tiempo de ejecución significativamente diferente de los demás.

Hipótesis complementaria sobre la interacción (segunda parte de la pregunta):

- **H0₂:** el efecto del lenguaje sobre el tiempo de ejecución no depende del tamaño N.
- **H1₂:** el efecto del lenguaje sobre el tiempo de ejecución depende del tamaño N (existe interacción lenguaje × N).

Nivel de significancia: α = 0,05.

## 4. Variables

### 4.1 Independientes (factores)

| Factor | Niveles | Tipo |
|---|---|---|
| Lenguaje de implementación | C++, Go, Java, Python | Categórica |
| Tamaño de la matriz (N) | 500, 1000, 1500 | Numérica discreta |

### 4.2 Dependiente

- **Tiempo de ejecución** (`time_seconds`), medido **solo sobre la multiplicación**: las matrices se crean antes de iniciar el temporizador, que parte justo antes del algoritmo y termina al obtener la matriz resultante.

### 4.3 Variables controladas

| Variable | Valor fijado |
|---|---|
| Algoritmo | Triple bucle `i-j-k` estándar, orden de bucles idéntico en los 4 lenguajes |
| Tipo de dato | `double` (64 bits) |
| Disposición en memoria | Matrices en arreglo contiguo por filas (*row-major*) donde el lenguaje lo permita |
| Datos de entrada | Generados con semilla fija (`SEED = 42`), mismos valores para todos los lenguajes |
| Paralelismo | Un solo hilo / proceso |
| Bibliotecas externas | Ninguna (Python **sin** NumPy; no se usan librerías optimizadas de multiplicación) |
| Hardware y SO | Misma máquina, mismo SO, misma configuración (se registra en `results/environment.json`) |
| Carga del sistema | Sin otras aplicaciones pesadas; gobernador de CPU fijo en modo *performance* |
| Versiones | Compiladores e intérpretes fijados (sección 6) |

### 4.3.1 Variables no controladas (fuentes de ruido reconocidas)

Planificación del SO, caché del procesador, frecuencia dinámica de la CPU, recolector de basura (Java, Go, Python) y compilación JIT (Java). Se mitigan con repeticiones, aleatorización del orden de ejecución y registro del entorno.

## 5. Diseño experimental

- **Tipo de diseño:** factorial completo 4 (lenguajes) × 3 (tamaños) = 12 condiciones.
- **Repeticiones:** 10 repeticiones por combinación de lenguaje y tamaño (120 mediciones en total).
- **Aislamiento:** cada medición se realiza en un proceso nuevo, para evitar efectos de estado compartido entre ejecuciones.
- **Aleatorización:** el orden de las 120 mediciones se baraja con semilla fija para reducir sesgos por deriva térmica o carga externa.
- **Validación de correctitud:** cada implementación calcula un *checksum* (suma de los elementos de C) y se compara con una referencia común. Una medición solo es válida si el checksum coincide.
- **Compilación y ejecución:**
  - C++: `g++ -O2 -std=c++17` (la bandera se documenta y se justifica; optimización moderada, sin vectorización agresiva).
  - Go: `go build` (compilador estándar).
  - Java: JVM estándar, sin banderas especiales.
  - Python: CPython, sin extensiones.

### 5.1 Análisis estadístico planificado

1. Integración de `cpp.csv`, `go.csv`, `java.csv` y `python.csv` (columnas `language`, `N`, `repetition`, `time_seconds`) en `benchmark.csv`.
2. Estadística descriptiva por condición (media, mediana, desviación estándar) y gráficos de caja.
3. Verificación de supuestos: normalidad (Shapiro-Wilk) y homogeneidad de varianzas (Levene), con transformación logarítmica si corresponde.
4. ANOVA de dos factores con interacción (lenguaje y N).
5. Comparaciones post-hoc con Tukey HSD, cuando corresponda.
6. Análisis de escalamiento: ajuste de `log(tiempo)` vs `log(N)` por lenguaje, contrastado con el crecimiento teórico O(N³).

## 6. Entorno (a completar con los valores reales)

| Componente | Versión / valor |
|---|---|
| CPU | _por definir_ |
| RAM | _por definir_ |
| Sistema operativo | _por definir_ |
| g++ | _por definir_ |
| Go | _por definir_ |
| Java (JDK) | _por definir_ |
| Python | _por definir_ |
| R o Python (análisis) | _por definir_ |

Se planea empaquetar el entorno en un `Dockerfile` con versiones fijadas, para facilitar la reproducción por terceros.

## 7. Estructura prevista del repositorio

```
.
├── README.md
├── LICENSE
├── docker/                 # un Dockerfile por lenguaje (build manual)
├── src/
│   ├── cpp/matmul.cpp
│   ├── go/matmul.go
│   ├── java/MatMul.java
│   └── python/matmul.py
├── Snakefile               # pipeline (semana 4)
├── scripts/
│   └── analyze.py          # análisis estadístico y gráficos
├── results/
│   ├── cpp.csv  go.csv  java.csv  python.csv
│   ├── benchmark.csv
│   ├── environment.json
│   └── figures/
└── docs/
```

## 8. Alineación con ACM Artifact Review and Badging

| Insignia / criterio | Cómo se aborda en este artifact |
|---|---|
| **Artifacts Available** | Repositorio público en GitHub, con licencia abierta y *release* etiquetado (idealmente con DOI vía Zenodo) |
| **Artifacts Evaluated – Functional** | Documentado, consistente y completo: README, scripts y código ejecutables de punta a punta |
| **Artifacts Evaluated – Reusable** | Código modular y comentado, parámetros configurables (N, repeticiones, semilla), entorno containerizado |
| **Results Reproduced** | Otra persona, con el mismo artifact y entorno, obtiene resultados consistentes (mismos *checksums*, mismas conclusiones estadísticas) |
| **Results Replicated** | Otra persona reimplementa o ejecuta en otro hardware y llega a conclusiones cualitativamente equivalentes (mismo ordenamiento entre lenguajes) |

## 9. Amenazas a la validez y limitaciones

- **Validez interna:** el JIT de Java, el GC y la frecuencia de la CPU pueden introducir variabilidad. Se mitigan con repeticiones, aleatorización del orden y registro del entorno.
- **Validez de constructo:** el tiempo del algoritmo *naive* mide más la calidad del compilador y del runtime que la "velocidad del lenguaje" en sí. La conclusión se limita a las implementaciones y versiones evaluadas.
- **Validez externa:** los resultados dependen de la arquitectura y del SO usados, por lo que no se generalizan a otras plataformas sin replicación.
- **Costo y muestra:** Python puro en N = 1500 es mucho más lento que los demás lenguajes, y 10 repeticiones por condición dan pocos datos para estimar la variabilidad.
- **Banderas de compilación:** los resultados de C++ dependen del nivel de optimización elegido (`-O0` vs `-O2` vs `-O3`); se documenta y se puede incluir como análisis de sensibilidad.

## 10. Cómo reproducir (a completar en las semanas 3 y 4)

Las cuatro imágenes Docker se construyen manualmente a partir de los Dockerfile del repositorio; luego el pipeline de Snakemake ejecuta el flujo completo.

```bash
git clone <URL-del-repositorio>
cd <repositorio>
# 1) construir las cuatro imágenes (semana 3)
# 2) snakemake --cores 1   (semana 4)
```

## 11. Cronograma del módulo

| Semana | Entregable |
|---|---|
| 1 | Repositorio y README inicial: diseño experimental (este documento) |
| 2 | Implementación y ejecución: cuatro CSV por lenguaje y registro del entorno |
| 3 | Entornos Docker y evaluación funcional del artifact |
| 4 | Pipeline Snakemake y análisis estadístico (ANOVA de dos factores, Tukey HSD) |
| 5 | Publicación en Zenodo (DOI) y evaluación cruzada |

## 12. Licencia y citación

_Por definir (se sugiere MIT para el código y CC-BY 4.0 para los datos y la documentación)._

## 13. Referencias

- Association for Computing Machinery. *Artifact Review and Badging, Current Version.* https://www.acm.org/publications/policies/artifact-review-and-badging-current
