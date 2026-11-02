# Benchmark reproducible de multiplicación de matrices

**Autor:** Jonathan Alexis Valenzuela Tapia  
**Programa:** Doctorado en Ingeniería en Informática, USACH  
**Curso:** Experimentación Computacional  
**Versión:** 1.0.0, archivada en Zenodo

## Descripción general

Este proyecto compara el tiempo de ejecución del algoritmo clásico de multiplicación de matrices cuadradas `NxN` en cuatro lenguajes de programación: C++, Go, Java y Python.

La implementación sigue una estrategia equivalente en los cuatro casos: mismo algoritmo naive, mismo tipo de datos (`double`), misma semilla para la generación de entrada y la misma estructura de validación.

## Pregunta de investigación

¿Existen diferencias estadísticamente significativas en el tiempo de ejecución entre implementaciones equivalentes en C++, Go, Java y Python, y cómo cambian estas diferencias con el tamaño de la matriz?

## Hipótesis

- **H0:** No hay diferencias estadísticamente significativas entre lenguajes.
- **H1:** Al menos uno de los lenguajes presenta diferencias significativas.

## Técnicas y diseño

- **Diseño factorial:** 4 lenguajes × 3 tamaños de matriz (`500`, `1000`, `1500`)
- **Repeticiones:** 10 por condición
- **Semilla:** `42` para generar entradas idénticas en las cuatro implementaciones; el script nativo aleatoriza bloques
- **Validación:** cada ejecución genera un checksum para comprobar que todas las implementaciones producen el mismo resultado

## Lenguajes implementados

- C++
- Go
- Java
- Python (sin NumPy)

## Estructura del repositorio

```text
.
├── README.md
└── mm/
    ├── Snakefile
    ├── config.yaml
    ├── requirements-lock.txt
    ├── LICENSE / LICENSE-DATA.md
    ├── DATASHEET.md
    ├── docker/       # Dockerfiles y runner de contenedor
    ├── scripts/      # benchmark, integración, validación y análisis
    ├── src/          # implementaciones C++, Go, Java y Python
    └── results/      # resultados, análisis y gráfico generado
```

## Requisitos

- C++17
- Go 1.21+
- JDK 17+
- Python 3.8+
- Docker (opcional, para entorno reproducible)

## Ejecución rápida

La ejecución nativa se realiza desde el artifact `mm/`:

```bash
./mm/scripts/run_all.sh
```

También puede ejecutarse con tamaños reducidos:

```bash
SIZES="100 200" REPS=3 ./mm/scripts/run_all.sh
```

## Pipeline automatizado del artifact

La versión con Docker y Snakemake está en [mm/](mm/); su guía completa está en [mm/README.md](mm/README.md). En Windows, usa Docker Desktop en modo Linux y PowerShell o WSL2. Desde esa carpeta, construye manualmente las cuatro imágenes locales y luego ejecuta Snakemake:

```bash
cd mm
docker build --pull -f docker/Dockerfile.cpp -t matmul-cpp .
docker build --pull -f docker/Dockerfile.go -t matmul-go .
docker build --pull -f docker/Dockerfile.python -t matmul-python .
docker build --pull -f docker/Dockerfile.java -t matmul-java .
python -m pip install -r requirements-lock.txt
snakemake --cores 1
```

La ejecución validada generó 120 mediciones (30 por lenguaje) en [benchmark.csv](mm/results/benchmark.csv) y los checksums coinciden entre lenguajes para los tres tamaños. El análisis detectó efectos significativos del lenguaje (p = 3,74 × 10⁻¹⁵³), tamaño (p = 5,04 × 10⁻¹²⁹) e interacción lenguaje × tamaño (p = 2,90 × 10⁻¹⁴⁸); por ello, el reporte presenta comparaciones de Tukey por estrato. Los resultados completos están en [analysis.md](mm/results/analysis.md), [anova.csv](mm/results/anova.csv) y [benchmark_by_language.png](mm/results/benchmark_by_language.png). La evidencia y evaluación requisito por requisito están en [mm/README.md](mm/README.md). La pauta de semana 4 no solicita diagnósticos de los supuestos del ANOVA; el análisis no los incluye, por lo que las inferencias deben leerse con esa limitación.

## Publicación y reutilización (semana 5)

La versión 1.0.0 incluye el código y el pipeline, resultados de referencia, [licencia MIT para el software](mm/LICENSE), [CC BY 4.0 para los datos y documentación](mm/LICENSE-DATA.md), [mini datasheet FAIR](mm/DATASHEET.md), metadatos de citación y una [plantilla de evaluación cruzada](mm/REVIEW-CROSS.md). Las instrucciones completas para quien evalúe el artifact están en [mm/README.md](mm/README.md).

**DOI de la versión 1.0.0:** [10.5281/zenodo.23891451](https://doi.org/10.5281/zenodo.23891451)

**Registro de Zenodo:** [zenodo.org/records/23891451](https://zenodo.org/records/23891451)

**DOI de todas las versiones:** [10.5281/zenodo.23891450](https://doi.org/10.5281/zenodo.23891450)

**Etiqueta estable en GitHub:** [v1.0.0](https://github.com/jonathanvalenzuelat-Usach/Computacion_ExperimentalM2/tree/v1.0.0)

Para las condiciones de uso, consulta la [licencia MIT del código](mm/LICENSE) y la [licencia CC BY 4.0 de los datos y documentación](mm/LICENSE-DATA.md).

## Ejecución con Docker

Para ejecutar un contenedor manualmente, primero cambia a la carpeta `mm/` y construye las imágenes siguiendo las instrucciones de su [README](mm/README.md):

```bash
cd mm
docker build -f docker/Dockerfile.cpp -t matmul-cpp .
docker build -f docker/Dockerfile.go -t matmul-go .
docker build -f docker/Dockerfile.java -t matmul-java .
docker build -f docker/Dockerfile.python -t matmul-python .
```

Luego:

```bash
docker run --rm -v "$(pwd)/results:/app/results" matmul-cpp
```

## Resultados esperados

Los archivos CSV generados contienen columnas como:

```csv
language,N,repetition,time_seconds
cpp,500,1,0.078512345
```

Se generan además archivos de checksum y resúmenes de validación.

## Reproducibilidad

El proyecto está diseñado para ser reproducible y reutilizable bajo los principios de ACM Artifact Review and Badging. Se registran:

- entorno de ejecución
- versiones de software
- semilla y datos de entrada reproducibles; el orden aleatorio aplica al script nativo, no al flujo Docker de Snakemake
- validación de resultados por checksum
- estructura modular del experimento

## Observaciones relevantes

- Python es mucho más lento que C++ en la implementación naive, aun cuando el algoritmo es idéntico.
- El comportamiento cambia según `N`, y hay interacción entre lenguaje y tamaño de la matriz.
- La comparación debe hacerse dentro del mismo entorno experimental para evitar sesgos por hardware o sistema operativo.

## Licencia

El código se distribuye bajo [MIT](mm/LICENSE); los datos y la documentación, bajo [CC BY 4.0](mm/LICENSE-DATA.md).

## Referencias

- Association for Computing Machinery. *Artifact Review and Badging.*

---

Este repositorio permite comparar rendimiento, reproducibilidad y consistencia de resultados entre lenguajes distintos usando el mismo algoritmo y condiciones experimentales.
