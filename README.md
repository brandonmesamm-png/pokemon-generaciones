# Pokémon por generaciones — Diagnóstico de calidad de datos

Proyecto individual de ciencia de datos del Tecnólogo en Análisis y Desarrollo de Software (SENA), Ficha 3169901.

**Autor:** Brandon Maldonado Mesa

## Propósito

Realizar un diagnóstico inicial de calidad del dataset de Pokémon con Python y Pandas (estructura, tipos de datos, valores faltantes e inconsistencias) antes de cualquier limpieza o análisis.

## Pregunta analítica

¿Cómo han cambiado las estadísticas base promedio de los Pokémon (HP, ataque, defensa, ataque especial, defensa especial y velocidad) entre generaciones, y cuál de ellas ha tenido el mayor cambio?

## Datasets

| Archivo | Fuente | Contenido |
|---|---|---|
| `data/raw/pokemon_pokeapi.csv` | [PokéAPI](https://pokeapi.co) | 1025 Pokémon (generaciones 1 a 9): id, nombre, generación, tipos, legendario, mítico, seis estadísticas base y total |

El archivo se genera con `scripts/descargar_pokeapi.py`.

## Resultados del diagnóstico (resumen)

- 1025 filas y 14 columnas; sin duplicados ni inconsistencias detectadas.
- Único valor faltante: `tipo_2` (499 nulos, 48.68 %), que corresponde a Pokémon de un solo tipo.
- Valores atípicos en `hp`, `defensa` y `defensa_especial`, por revisar.
- Los legendarios y míticos elevan el promedio del total (592.0 frente a 411.1 del resto).
- Limitaciones: una sola fuente y una sola forma por Pokémon.

El detalle completo está en `reports/data_quality.md`.

## Estructura

```
pokemon-generaciones/
├── README.md
├── .gitignore
├── requirements.txt
├── data/
│   └── raw/
│       └── pokemon_pokeapi.csv
├── scripts/
│   └── descargar_pokeapi.py
├── notebooks/
│   └── data_quality.ipynb
└── reports/
    └── data_quality.md
```

## Cómo reproducir el diagnóstico (Windows, cmd)

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
4. Generar el dataset (solo si `data/raw/pokemon_pokeapi.csv` no existe; requiere internet):
   ```
   python scripts\descargar_pokeapi.py
   ```
5. Abrir JupyterLab y ejecutar `notebooks/data_quality.ipynb` completo:
   ```
   jupyter lab
   ```

## Informe

Ver `reports/data_quality.md`.