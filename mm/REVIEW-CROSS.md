# Registro de evaluación cruzada del artifact

Completa este formulario al evaluar el artifact de forma independiente. Registra el sistema, los comandos exactos y los errores; no reemplaces esta evidencia con una descripción de la ejecución del autor.

## Evaluador y entorno

- Evaluador/a:
- Fecha:
- Sistema operativo y versión:
- CPU / arquitectura:
- RAM:
- Docker y modo (Linux/WSL2):
- Python:
- Snakemake:
- Commit, versión o DOI del artifact evaluado:

## Reproducción

- ¿Pudiste obtener el artifact únicamente desde el depósito/README?:
- ¿Construiste localmente las cuatro imágenes desde los Dockerfiles?:
- Comandos exactos utilizados:
- ¿Ejecutaste `snakemake --cores 1` sin modificar el pipeline?:
- ¿Finalizó cada contenedor? (C++, Go, Python, Java):
- ¿Se generaron los cuatro CSV?:
- ¿`benchmark.csv` contiene 120 filas de datos?:
- ¿La validación de estructura, repeticiones y checksums pasó?:
- ¿Se generaron ANOVA, Tukey HSD, tablas, reporte y gráfico?:
- Diferencias en los resultados o conclusiones:

## Incidencias y evaluación

| Etapa/archivo | Dificultad, error o ambigüedad | Mensaje completo / evidencia | Modificación necesaria |
|---|---|---|---|
| | | | |

- Dependencias faltantes:
- Tiempo total aproximado:
- Cambios requeridos para completar la reproducción:
- ¿El README fue suficiente para una persona externa?:
- ¿El artifact es funcional? Justifica:
- ¿El artifact es reutilizable? Justifica qué funcionó y qué no:
- Recomendaciones:

Adjunta logs sanitizados si son necesarios; nunca incluyas contraseñas, tokens ni credenciales.
