# Benchmark reproducible de multiplicación de matrices

**Autor:** Jonathan Alexis Valenzuela Tapia  
**Programa:** Doctorado en Ingeniería en Informática, USACH  
**Curso:** Experimentación Computacional  
**Estado:** Semana 3, versión reproducible con Docker y validación funcional

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
- **Aleatorización:** orden aleatorio con semilla fija `42`
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
├── src/
│   ├── cpp/
│   ├── go/
│   ├── java/
│   └── python/
├── docker/
│   ├── Dockerfile.cpp
│   ├── Dockerfile.go
│   ├── Dockerfile.java
│   ├── Dockerfile.python
│   ├── Dockerfile.all
│   ├── run_container.sh
│   └── run_lang.sh
├── scripts/
│   ├── run_all.sh
│   ├── gen_order.py
│   ├── record_env.py
│   ├── verify.py
│   └── summarize.py
├── results/
├── results_semana2_windows/
└── .gitignore
```

## Requisitos

- C++17
- Go 1.21+
- JDK 17+
- Python 3.8+
- Docker (opcional, para entorno reproducible)

## Ejecución rápida

Desde la raíz del proyecto:

```bash
./scripts/run_all.sh
```

También puede ejecutarse con tamaños reducidos:

```bash
SIZES="100 200" REPS=3 ./scripts/run_all.sh
```

## Ejecución con Docker

```bash
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
- orden aleatorizado de ejecuciones
- validación de resultados por checksum
- estructura modular del experimento

## Observaciones relevantes

- Python es mucho más lento que C++ en la implementación naive, aun cuando el algoritmo es idéntico.
- El comportamiento cambia según `N`, y hay interacción entre lenguaje y tamaño de la matriz.
- La comparación debe hacerse dentro del mismo entorno experimental para evitar sesgos por hardware o sistema operativo.

## Licencia

Por definir. Se recomienda usar una licencia abierta como MIT para el código y CC-BY 4.0 para la documentación.

## Referencias

- Association for Computing Machinery. *Artifact Review and Badging.*

---

Este repositorio permite comparar rendimiento, reproducibilidad y consistencia de resultados entre lenguajes distintos usando el mismo algoritmo y condiciones experimentales.
