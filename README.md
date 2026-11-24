# Pokémon por generaciones

Proyecto individual de ciencia de datos del Tecnólogo en Análisis y Desarrollo de Software (SENA), Ficha 3169901.

**Autor:** Brandon Maldonado Mesa

## Propósito

Preparar, limpiar y estructurar con Python y Pandas los datos de los Pokémon de las generaciones 1 a 9, para responder la pregunta analítica del proyecto.

## Pregunta analítica

¿Cómo han cambiado las estadísticas base promedio de los Pokémon (HP, ataque, defensa, ataque especial, defensa especial y velocidad) entre generaciones, y cuál de ellas ha tenido el mayor cambio?

## Fuente de datos

| Archivo | Fuente | Contenido |
|---|---|---|
| `data/raw/pokemon_pokeapi.csv` | [PokéAPI](https://pokeapi.co) | 1025 Pokémon (generaciones 1 a 9): id, nombre, generación, tipos, legendario, mítico, seis estadísticas base y total |

El archivo original se genera con `scripts/descargar_pokeapi.py` y no se modifica: todas las transformaciones se hacen en el cuaderno y se guardan en `data/processed/`.

El proyecto usa un solo dataset, por lo que no se combinan tablas: hacerlo habría sido una combinación artificial. En su lugar se aplicaron técnicas de estructuración (columnas derivadas, formato largo y tablas de resultados).

## Estructura

```
pokemon-generaciones/
├── README.md
├── .gitignore
├── requirements.txt
├── data/
│   ├── raw/
│   │   └── pokemon_pokeapi.csv
│   └── processed/              # generados por data_preparation.ipynb
├── scripts/
│   └── descargar_pokeapi.py
├── notebooks/
│   ├── data_quality.ipynb      # diagnóstico de calidad (EV05)
│   └── data_preparation.ipynb  # limpieza, análisis y estructuración (EV07)
└── reports/
    └── data_quality.md         # informe del diagnóstico de calidad
```

## Transformaciones realizadas (`notebooks/data_preparation.ipynb`)

| Etapa | Qué se hizo | Resultado |
|---|---|---|
| Limpieza | Revisión de duplicados (filas, IDs y nombres, también tras normalizar el texto) | Ninguno; el paso queda en el pipeline como protección |
| Limpieza | Revisión del texto y de los tipos (`nombre`, `tipo_1`, `tipo_2`) | Ya estandarizados; los 18 tipos son válidos |
| Limpieza | Análisis de nulos | Los 499 de `tipo_2` corresponden a Pokémon de un solo tipo; se conservan |
| Limpieza | Ajuste de tipos de dato | Enteros a `int16` e `int8`; `tipo_1` y `tipo_2` a `category` |
| Limpieza | Pipeline con `pipe`, informe de cambios y validaciones con `assert` | Informe en `cleaning_report.csv` |
| Análisis | Filtros, ordenamiento, `groupby` y `agg`, tabla dinámica y categorización del poder | Tablas por generación con y sin legendarios y míticos |
| Análisis | Cuatro indicadores: cambio entre generación 1 y 9, tendencia por generación, proporción de legendarios y míticos, y su contribución al cambio del total | Ver `change_indicators.csv` |
| Estructuración | Columnas nuevas `especial`, `doble_tipo` y `categoria_poder` | Dataset de 1025 filas y 17 columnas |
| Estructuración | Formato largo con `melt` | 6150 filas (1025 Pokémon por 6 estadísticas) |
| Validación | Comprobaciones de clave, conteos por generación, consistencia entre formato ancho y largo y lectura de los archivos exportados | Todas superadas |

## Archivos generados en `data/processed/`

| Archivo | Descripción |
|---|---|
| `pokemon_clean.csv` | Dataset limpio y estructurado: 1025 filas y 17 columnas |
| `pokemon_stats_long.csv` | Las seis estadísticas en formato largo: 6150 filas |
| `generation_averages.csv` | Promedio de cada estadística por generación, con número de Pokémon, para todos los Pokémon y sin legendarios ni míticos |
| `change_indicators.csv` | Cambio entre las generaciones 1 y 9 y tendencia por generación de cada estadística |
| `cleaning_report.csv` | Filas, columnas, nulos y memoria después de cada paso del pipeline de limpieza |
| `quality_comparison.csv` | Verificaciones de calidad antes y después del procesamiento |

## Resultados principales

- **HP es la estadística que más cambió** entre la generación 1 y la 9: de 64,2 a 77,4 (+13,2 puntos, +20,5 %). El resultado se mantiene sin legendarios ni míticos y con la mediana.
- **Ataque es la que más sube por generación** (+1,63 puntos por generación frente a +1,08 de HP), por lo que la respuesta depende de cómo se defina el cambio.
- El aumento del total promedio se debe sobre todo a los Pokémon que no son legendarios ni míticos: de los 49,7 puntos de aumento, 43,5 se mantienen al excluirlos.
- La proporción de Pokémon con total entre 500 y 599 pasa de 19,9 % en la generación 1 a 42,5 % en la 9.

## Limitaciones

- Las estadísticas son las vigentes en PokéAPI, no necesariamente las originales de cada generación.
- Hay una sola fuente y una sola forma por Pokémon (sin megaevoluciones ni formas regionales).
- Los valores atípicos se conservaron y falta contrastarlos con una segunda fuente (por ejemplo, Bulbapedia).
- Los resultados son descriptivos: las generaciones tienen tamaños distintos (de 72 a 156 Pokémon) y no se aplicó ninguna prueba estadística.

## Cómo reproducir el trabajo (Windows, cmd)

1. Clonar el repositorio y entrar a la carpeta.
2. Crear y activar el entorno virtual:
   ```
   python -m venv .venv
   .venv\Scripts\activate
   ```
3. Instalar dependencias:
   ```
   pip install -r requirements.txt
   ```
4. Generar el dataset original (solo si `data/raw/pokemon_pokeapi.csv` no existe; requiere internet):
   ```
   python scripts\descargar_pokeapi.py
   ```
5. Abrir JupyterLab:
   ```
   jupyter lab
   ```
6. Ejecutar los cuadernos completos con *Kernel → Restart Kernel and Run All Cells*:
   - `notebooks/data_quality.ipynb` (diagnóstico)
   - `notebooks/data_preparation.ipynb` (limpieza, análisis y estructuración; genera los archivos de `data/processed/`)

## Flujo de trabajo en Git

- Rama base: `develop`.
- Rama de trabajo de la preparación de datos: `feature/project-data-preparation`.
- Commits de la actividad:
  - `feat: clean and standardize project data`
  - `feat: implement data filtering and aggregation`
  - `feat: prepare and validate processed datasets`
  - `docs: update project README`

## Informes

- Diagnóstico de calidad: [`reports/data_quality.md`](reports/data_quality.md)
