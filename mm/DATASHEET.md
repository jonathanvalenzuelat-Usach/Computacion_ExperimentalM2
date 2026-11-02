# Mini datasheet FAIR

## Identificación

- **Nombre:** Benchmark de multiplicación de matrices NxN en C++, Go, Java y Python.
- **Versión:** 1.0.0.
- **Responsable:** Jonathan Alexis Valenzuela Tapia, Universidad de Santiago de Chile (USACH).
- **Pregunta:** ¿Cómo varía el tiempo de multiplicación naive de matrices entre cuatro implementaciones y tres tamaños de entrada?
- **Identificador persistente:** DOI de la versión 1.0.0 en Zenodo: [10.5281/zenodo.23891451](https://doi.org/10.5281/zenodo.23891451). El DOI que resuelve a todas las versiones es [10.5281/zenodo.23891450](https://doi.org/10.5281/zenodo.23891450). La versión de código también está identificada con la etiqueta Git [v1.0.0](https://github.com/jonathanvalenzuelat-Usach/Computacion_ExperimentalM2/tree/v1.0.0).

## Composición y procedencia

- El conjunto consolidado `results/benchmark.csv` contiene 120 mediciones: cuatro lenguajes × tres tamaños (500, 1000 y 1500) × diez repeticiones.
- Los datos proceden de ejecuciones de los programas del artifact en contenedores Docker construidos localmente desde `docker/Dockerfile.cpp`, `Dockerfile.go`, `Dockerfile.java` y `Dockerfile.python`.
- Las matrices de entrada se generan determinísticamente con la semilla 42. El archivo consolidado reúne los CSV individuales `cpp.csv`, `go.csv`, `java.csv` y `python.csv`.
- Los checksums permiten verificar que cada implementación produjo resultados concordantes para el mismo tamaño.
- El entorno registrado es Ubuntu 24.04.5 LTS en WSL2, arquitectura x86_64, ocho núcleos visibles y 7 970 432 kB de memoria visibles en el contenedor. Las versiones concretas de compiladores e intérpretes constan en `results/environment_*.txt`.
- El modelo exacto del procesador anfitrión no quedó registrado en esos archivos; la memoria visible es la asignada/expuesta al entorno de contenedores y no necesariamente la RAM física instalada.

## Estructura y formato

`results/benchmark.csv` es UTF-8 y CSV con encabezado. Cada fila es una observación; los tiempos son segundos decimales y los tamaños y repeticiones son enteros.

| Campo | Tipo | Descripción |
|---|---|---|
| `language` | texto | `cpp`, `go`, `java` o `python` |
| `N` | entero | Dimensión de cada matriz cuadrada |
| `repetition` | entero | Número de repetición, de 1 a 10 |
| `time_seconds` | decimal | Duración de la multiplicación, en segundos |

`results/descriptive.csv` contiene estadística descriptiva por condición; `results/anova.csv`, la tabla ANOVA factorial tipo II; `results/tukey_hsd.csv`, las comparaciones post-hoc; `results/analysis.md`, la interpretación tabular; y `results/benchmark_by_language.png`, el gráfico.

## FAIR: localización, acceso e interoperabilidad

- **Findable (localizable):** el [registro público de Zenodo](https://zenodo.org/records/23891451), el DOI de esta versión y el DOI de todas las versiones están enlazados aquí y desde GitHub.
- **Accessible (accesible):** el CSV es texto plano y se puede descargar desde el repositorio y el [registro público de Zenodo](https://zenodo.org/records/23891451). No contiene datos personales ni requiere credenciales para su lectura.
- **Interoperable:** usa CSV UTF-8, nombres de campos explícitos y tipos simples compatibles con R, Python, hojas de cálculo y otras herramientas estadísticas.
- **Reusable (reutilizable):** incluye código, configuración, Snakefile, instrucciones, checksums y registro de entorno. El código tiene licencia MIT y los datos/documentación CC BY 4.0; cita este artifact y conserva la atribución.

## Limitaciones y uso apropiado

- Las mediciones representan este algoritmo, estas implementaciones, esta configuración de contenedores y el entorno registrado; no establecen que un lenguaje sea universalmente más rápido.
- Hay diez repeticiones por condición. La máquina, el planificador, la temperatura, la frecuencia de CPU y la virtualización pueden cambiar los tiempos absolutos.
- El flujo Docker de Snakemake ejecuta secuencialmente los lenguajes, pero no aleatoriza el orden de los bloques. El orden aleatorio pertenece al script nativo y no debe atribuirse a esta ejecución Docker.
- Se aplica ANOVA de dos factores con interacción y Tukey HSD; esta versión del análisis no produce diagnósticos de normalidad de residuos ni homogeneidad de varianzas. Interpreta los valores p teniendo en cuenta esta limitación.
- Las imágenes Docker se construyen manualmente. Los Dockerfiles parten de `ubuntu:24.04` y los paquetes del sistema se instalan desde los repositorios configurados al momento de construir; actualizaciones futuras de esos repositorios pueden cambiar las versiones. Las versiones observadas en la ejecución de referencia están registradas en `results/environment_*.txt`.

## Reutilización y citación

Para repetir el experimento, sigue `README.md`, construye localmente las cuatro imágenes Docker y ejecuta `snakemake --cores 1`. Para citar, usa `CITATION.cff` o el DOI de la versión 1.0.0: [10.5281/zenodo.23891451](https://doi.org/10.5281/zenodo.23891451). Registro público de Zenodo: [zenodo.org/records/23891451](https://zenodo.org/records/23891451).
