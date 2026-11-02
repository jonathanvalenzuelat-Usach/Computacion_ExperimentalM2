# Análisis estadístico del benchmark

ANOVA de dos factores con interacción; α = 0.05.

## Estadística descriptiva

| Lenguaje | N | n | Media (s) | Mediana (s) | Desv. est. (s) | Mín. (s) | Máx. (s) |
|---|---:|---:|---:|---:|---:|---:|---:|
| cpp | 500 | 10 | 0.176278 | 0.15993 | 0.0519141 | 0.126987 | 0.304564 |
| cpp | 1000 | 10 | 1.19237 | 1.20509 | 0.0691031 | 1.08204 | 1.28864 |
| cpp | 1500 | 10 | 4.89352 | 4.85609 | 0.42077 | 4.384 | 5.57028 |
| go | 500 | 10 | 0.18247 | 0.183958 | 0.0391262 | 0.135567 | 0.252479 |
| go | 1000 | 10 | 1.35899 | 1.2935 | 0.152414 | 1.19828 | 1.67692 |
| go | 1500 | 10 | 6.08581 | 6.0385 | 0.300563 | 5.7685 | 6.70901 |
| java | 500 | 10 | 0.236138 | 0.19843 | 0.0817967 | 0.158132 | 0.39877 |
| java | 1000 | 10 | 1.81344 | 1.83608 | 0.260179 | 1.35509 | 2.10136 |
| java | 1500 | 10 | 6.61921 | 6.55232 | 0.941412 | 5.62022 | 8.80178 |
| python | 500 | 10 | 10.7756 | 10.6804 | 0.630361 | 9.92874 | 11.8229 |
| python | 1000 | 10 | 90.4817 | 88.2533 | 4.92341 | 87.2569 | 102.935 |
| python | 1500 | 10 | 332.242 | 331.054 | 6.8632 | 327.395 | 351.315 |

## ANOVA tipo II

| Factor | Suma de cuadrados | gl | F | p-valor |
|---|---:|---:|---:|---:|
| C(language) | 453658 | 3 | 24857.6 | 3.74076e-153 |
| C(N) | 155461 | 2 | 12777.4 | 5.0408e-129 |
| C(language):C(N) | 405553 | 6 | 11110.9 | 2.90066e-148 |
| Residual | 657.01 | 108 | nan | nan |

## Comparaciones post-hoc (Tukey HSD)

Con interacción significativa se comparó lenguaje dentro de cada N y N dentro de cada lenguaje. Sin interacción significativa, se compararon los niveles de cada efecto principal significativo.

| Factor | Estrato | Grupo 1 | Grupo 2 | Diferencia media | p ajustado | Rechaza H0 |
|---|---|---|---|---:|---:|---|
| language | N=500 | cpp | go | 0.0062 | 1 | False |
| language | N=500 | cpp | java | 0.0599 | 0.9749 | False |
| language | N=500 | cpp | python | 10.5994 | 0 | True |
| language | N=500 | go | java | 0.0537 | 0.9816 | False |
| language | N=500 | go | python | 10.5932 | 0 | True |
| language | N=500 | java | python | 10.5395 | 0 | True |
| language | N=1000 | cpp | go | 0.1666 | 0.9987 | False |
| language | N=1000 | cpp | java | 0.6211 | 0.9423 | False |
| language | N=1000 | cpp | python | 89.2893 | 0 | True |
| language | N=1000 | go | java | 0.4545 | 0.9761 | False |
| language | N=1000 | go | python | 89.1227 | 0 | True |
| language | N=1000 | java | python | 88.6682 | 0 | True |
| language | N=1500 | cpp | go | 1.1923 | 0.8685 | False |
| language | N=1500 | cpp | java | 1.7257 | 0.6852 | False |
| language | N=1500 | cpp | python | 327.349 | 0 | True |
| language | N=1500 | go | java | 0.5334 | 0.9858 | False |
| language | N=1500 | go | python | 326.157 | 0 | True |
| language | N=1500 | java | python | 325.623 | 0 | True |
| N | language=cpp | 1000 | 1500 | 3.7012 | 0 | True |
| N | language=cpp | 1000 | 500 | -1.0161 | 0 | True |
| N | language=cpp | 1500 | 500 | -4.7172 | 0 | True |
| N | language=go | 1000 | 1500 | 4.7268 | 0 | True |
| N | language=go | 1000 | 500 | -1.1765 | 0 | True |
| N | language=go | 1500 | 500 | -5.9033 | 0 | True |
| N | language=java | 1000 | 1500 | 4.8058 | 0 | True |
| N | language=java | 1000 | 500 | -1.5773 | 0 | True |
| N | language=java | 1500 | 500 | -6.3831 | 0 | True |
| N | language=python | 1000 | 1500 | 241.761 | 0 | True |
| N | language=python | 1000 | 500 | -79.706 | 0 | True |
| N | language=python | 1500 | 500 | -321.467 | 0 | True |
