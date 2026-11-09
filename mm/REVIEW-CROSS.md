# Evaluación cruzada de artifacts de Zenodo

Evaluación funcional basada en los ZIP descargados desde los registros Zenodo indicados. Se construyeron las imágenes locales y se ejecutaron los pipelines smoke documentados cuando estaban disponibles. Las pruebas reducidas no sustituyen una reproducción completa del diseño publicado.

## Evaluador y entorno

- Evaluador: Jonathan Valenzuela.
- Fecha: 2026-11-08.
- Sistema operativo: Windows 11 Pro, 10.0.26300.
- CPU: Intel Core i7-1165G7, 4 núcleos / 8 hilos, x86_64.
- RAM del equipo: 15.69 GB. Docker Desktop Linux: 8 CPU y aproximadamente 7.6 GiB.
- Docker: 29.9.1, contenedores Linux.
- Python usado para Snakemake/análisis: 3.12.10. El `python` predeterminado del equipo es 3.14.7.
- Snakemake: 9.27.1.
- Artefactos evaluados: Joel Fuertes (10.5281/zenodo.23988249), Jorge Fornes (10.5281/zenodo.23987654), Pier Miqueles (10.5281/zenodo.23954259) y Alejandro Pirez (10.5281/zenodo.23954875).

## Resultado resumido

| Autor | Imágenes construidas/ejecutadas | Prueba del pipeline | Evidencia generada |
|---|---:|---|---|
| Joel Fuertes | 4/4 | Dry-run correcto; ejecución parcial directa de los cuatro contenedores en N=500 | Cuatro CSV, 10 filas por lenguaje; no se ejecutó la integración/análisis del pipeline |
| Jorge Fornes | 4/4 | Smoke end-to-end con parámetros reducidos temporalmente en el Snakefile | 24 mediciones, benchmark.csv, ANOVA, Tukey, tablas y gráficos |
| Pier Miqueles | 4/4 + imagen de análisis | Smoke documentado, 9/9 pasos | 24 mediciones, benchmark.csv, verificación de equivalencia, análisis y figuras |
| Alejandro Pirez | 4/4 | Smoke documentado, 15/15 pasos | 16 mediciones, benchmark.csv, análisis y figuras |

## Evidencia por artifact

### Joel Fuertes — [DOI 10.5281/zenodo.23988249](https://doi.org/10.5281/zenodo.23988249)

- Los cuatro Dockerfiles construyeron correctamente las imágenes `matrices-cpp:semana4`, `matrices-go:semana4`, `matrices-python:semana4` y `matrices-java:semana4`.
- Comando de planificación documentado ejecutado: `snakemake --cores 1 --forceall --rerun-incomplete --dry-run`. El DAG se construyó correctamente y mostró las reglas de ejecución, integración y análisis.
- Ejecuté los cuatro contenedores para N=500 usando las matrices incluidas en el ZIP. C++, Go, Java y Python terminaron y generaron `cpp.csv`, `go.csv`, `java.csv` y `python.csv`, con 10 mediciones válidas cada uno.
- No ejecuté la corrida completa de 120 mediciones ni las etapas de integración y análisis: no hay modo smoke parametrizable en el Snakefile y Python N=500 ya tardó alrededor de 12 segundos por repetición en este equipo.
- No se comparan estos tiempos parciales con los resultados publicados: el tamaño, hardware y modo de ejecución no permiten validar las conclusiones del experimento completo.

### Jorge Fornes — [DOI 10.5281/zenodo.23987654](https://doi.org/10.5281/zenodo.23987654)

- Las cuatro imágenes (`matrix-cpp`, `matrix-go`, `matrix-java`, `matrix-python`) se construyeron correctamente siguiendo los contextos indicados en README.
- El dry-run con `snakemake --cores 1 --forceall --dry-run` mostró 12 trabajos de benchmark, 4 de integración por lenguaje, consolidación y análisis.
- Probé además cada contenedor con N=50 y 2 repeticiones; los cuatro CSV se generaron. Los checksums impresos fueron idénticos en N=50.
- El Snakefile no ofrece modo smoke. Para comprobar el flujo completo sin ejecutar las 120 mediciones, cambié temporalmente solo `SIZES` a `[50, 100]` y `REPS` a `3` en la copia de prueba del Snakefile y ejecuté `python -m snakemake --cores 1 --forceall`. Las 15/15 etapas finalizaron; cada CSV por lenguaje tuvo 6 filas y `benchmark.csv`, 24. Se generaron ANOVA, Tukey, tablas y gráficos.
- En el primer intento del análisis faltó `seaborn` (`ModuleNotFoundError`). Se resolvió instalando las dependencias descritas por el artifact con `python -m pip install -r analysis/requirements.txt` dentro de un entorno aislado; el segundo intento terminó correctamente.
- En la prueba N=100, el checksum de Java fue `2481575924.829800`; C++, Go y Python reportaron `2481575924.829803` (diferencia de 0.000003 en valores impresos a seis decimales). En N=50 los cuatro coincidieron. Puede ser redondeo de punto flotante; el pipeline no falla ni valida automáticamente estos checksums. Conviene documentar/aplicar una tolerancia explícita para la equivalencia numérica.

### Pier Miqueles — [DOI 10.5281/zenodo.23954259](https://doi.org/10.5281/zenodo.23954259)

- Construí las cuatro imágenes de lenguaje y la imagen de análisis desde los Dockerfiles del ZIP.
- Ejecuté la prueba corta documentada: `snakemake --cores 1 --config results_dir=results_smoke 'sizes=[50,100]' repetitions=3`.
- El pipeline terminó con 9/9 pasos. Se generaron cuatro CSV con 6 filas cada uno, `benchmark.csv` con 24 filas, informe de equivalencia y los resultados estadísticos y gráficos.
- El informe de equivalencia indicó `SÍ` para C++, Go, Java y Python en N=50 y N=100.

### Alejandro Pirez — [DOI 10.5281/zenodo.23954875](https://doi.org/10.5281/zenodo.23954875)

- Construí correctamente las imágenes `matrix-bench-cpp:1.0`, `matrix-bench-go:1.0`, `matrix-bench-java:1.0` y `matrix-bench-python:1.0` desde los contextos descritos.
- Ejecuté el smoke documentado: `python -m snakemake --cores 1 --resources machine=1 --config smoke=true`, usando Python 3.12 en el PATH. Terminó con 15/15 pasos.
- Se generaron cuatro CSV con 4 filas cada uno, `results/smoke/benchmark.csv` con 16 filas y los productos estadísticos y gráficos.
- El equipo tenía Python 3.14 como predeterminado, que no tenía Snakemake instalado; seleccionar Python 3.12 (la versión requerida por el README) resolvió el problema sin cambios al artifact.

## Incidencias, límites y conclusión

| Etapa/archivo | Dificultad o diferencia | Evidencia / resolución | Modificación necesaria |
|---|---|---|---|
| Jorge, análisis | Faltaba `seaborn` al primer intento | Error `ModuleNotFoundError`; se instaló `analysis/requirements.txt` y el pipeline pasó | Ninguna en el artifact; instalar las dependencias documentadas |
| Jorge, Snakefile | No incluye parámetros smoke | Para probar la integración se usaron N=50,100 y 3 repeticiones en una copia temporal | El Snakefile distribuido no se cambió |
| Joel, duración | Sin modo smoke en el pipeline; Python N=500 tomó ~12 s por repetición | Los cuatro contenedores se ejecutaron; no se midieron N=1000/1500 ni se ejecutó integración/análisis | Para una prueba rápida sería útil permitir sobrescribir tamaños y repeticiones |
| Jorge, checksums | Java difirió en 0.000003 a N=100, con impresión de 6 decimales | Los demás lenguajes y Java coinciden en N=50; el pipeline no compara checksums | Definir y usar una tolerancia explícita, o explicar la variación de redondeo |
| Alejandro, intérprete | `python` predeterminado era 3.14 y no tenía Snakemake | Se ejecutó con Python 3.12, conforme al README | Ninguna en el artifact |

- Los 16 contenedores de lenguaje solicitados se construyeron y ejecutaron. Además, se construyó y ejecutó la imagen de análisis de Pier.
- Las pruebas smoke de Jorge, Pier y Alejandro comprobaron generación de CSV, consolidación automática y productos del análisis. La prueba de Joel confirmó los cuatro CSV por separado, pero no la consolidación automática.
- **No se ejecutaron las corridas completas de 120 observaciones** (N=500, 1000, 1500; 10 repeticiones) para estos artifacts. Por lo tanto, esta evaluación no confirma que se reproduzcan los resultados numéricos publicados ni las conclusiones estadísticas; los tiempos de smoke no son comparables con los resultados originales.
- La documentación fue suficiente para construir y ejecutar los artifacts probados una vez resueltas las dependencias del host. Para Jorge y Joel sería conveniente agregar instrucciones de smoke parametrizables.
- Evaluación funcional: los contenedores funcionan; tres pipelines se completaron en modo smoke y el cuarto requiere aún validar el pipeline completo. Reutilización: buena para pruebas reducidas, pero la reproducción íntegra de los cuatro experimentos queda pendiente.
