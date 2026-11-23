# Informe de diagnóstico de calidad de datos — Pokémon por generaciones

**Autor:** Brandon Maldonado Mesa · Ficha 3169901
**Actividad:** GA1-220501094-01-AA1-EV05 — Diagnosticar la calidad de datos
**Notebook de soporte:** `notebooks/data_quality.ipynb`

## 1. Proyecto y pregunta analítica

**Proyecto:** evolución de las estadísticas de combate de los Pokémon a lo largo de las generaciones de los videojuegos.

**Pregunta analítica:** ¿cómo han cambiado las estadísticas base promedio de los Pokémon (HP, ataque, defensa, ataque especial, defensa especial y velocidad) entre generaciones, y cuál de ellas ha tenido el mayor cambio?

**Pregunta orientadora de la actividad:** ¿qué condiciones de calidad presentan los datos y qué acciones de preparación deberían considerarse antes del análisis?

## 2. Descripción del dataset

Se utiliza un único dataset, `data/raw/pokemon_pokeapi.csv`, generado con el script `scripts/descargar_pokeapi.py` a partir de PokéAPI (https://pokeapi.co). Contiene un registro por Pokémon, de la generación 1 a la 9.

| Columna | Descripción | Relación con la pregunta |
|---|---|---|
| `id` | Número de Pokédex | Identifica cada registro |
| `nombre` | Nombre del Pokémon | Identifica cada registro |
| `generacion` | Generación en la que apareció (1 a 9) | Variable principal de comparación |
| `tipo_1`, `tipo_2` | Tipos del Pokémon (`tipo_2` solo existe en los de doble tipo) | Permiten ver si el cambio se concentra en ciertos tipos |
| `legendario`, `mitico` | Indicadores de Pokémon legendario o mítico | Permiten separar casos extremos que pueden sesgar los promedios |
| `hp`, `ataque`, `defensa`, `ataque_especial`, `defensa_especial`, `velocidad` | Las seis estadísticas base | Variables cuyo cambio se analiza |
| `total` | Suma de las seis estadísticas | Medida global de poder |

## 3. Resultados de la inspección estructural

| Dataset | Filas | Columnas | Tipos de datos | Observaciones |
|---|---|---|---|---|
| pokemon_pokeapi.csv | 1025 | 14 | int64 (9), str (3), bool (2) | Un registro por Pokémon, sin duplicados. Solo `tipo_2` tiene valores nulos. Los tipos de dato coinciden con el significado de cada columna. |

Resumen de las estadísticas descriptivas (`describe()`):

| Variable | Mínimo | Promedio | Máximo |
|---|---|---|---|
| hp | 1 | 70.2 | 255 |
| ataque | 5 | 77.5 | 181 |
| defensa | 5 | 72.5 | 230 |
| ataque_especial | 10 | 70.1 | 173 |
| defensa_especial | 20 | 70.2 | 230 |
| velocidad | 5 | 67.2 | 200 |
| total | 175 | 427.7 | 720 |

Las columnas de texto (`nombre`, `tipo_1`, `tipo_2`) tienen 1025, 1025 y 526 valores no nulos respectivamente. `nombre` tiene 1025 valores únicos; `tipo_1` y `tipo_2` tienen 18 tipos distintos cada una (`water` es el tipo principal más frecuente, con 134 registros).

## 4. Valores faltantes, tipos de datos e inconsistencias

### 4.1 Valores faltantes

| Columna | Nulos | Porcentaje |
|---|---|---|
| tipo_2 | 499 | 48.68 % |

Las demás 13 columnas no tienen valores faltantes. No hay cadenas vacías ni espacios en blanco en las columnas de texto. Los 499 nulos de `tipo_2` corresponden a Pokémon de un solo tipo (los 526 restantes tienen dos tipos), por lo que son una ausencia con significado y no un error de captura.

### 4.2 Tipos de datos

Las 14 columnas tienen un tipo coherente con la información que representan: identificadores y estadísticas como enteros, indicadores como booleanos y nombres y tipos como texto. En Pandas reciente el texto se almacena con el tipo `str` en lugar de `object`; no afecta el análisis.

### 4.3 Duplicados

| Verificación | Casos |
|---|---|
| Filas completamente duplicadas | 0 |
| IDs repetidos | 0 |
| Nombres repetidos | 0 |

### 4.4 Posibles inconsistencias

| Verificación | Casos encontrados |
|---|---|
| Total distinto de la suma de las 6 estadísticas | 0 |
| Estadísticas menores o iguales a 0, o mayores a 255 | 0 |
| Generación fuera del rango 1-9 | 0 |
| IDs no consecutivos | 0 |
| Generación que baja al subir el ID | 0 |
| `tipo_1` o `tipo_2` con un tipo inexistente | 0 |
| `tipo_2` igual a `tipo_1` | 0 |
| Legendario y mítico a la vez | 0 |

Ninguna de las verificaciones detectó registros incompatibles con el significado de las variables.

### 4.5 Distribución por generación

| Generación | Pokémon | Legendarios | Míticos | Total promedio | Referencia | Diferencia |
|---|---|---|---|---|---|---|
| 1 | 151 | 4 | 1 | 407.6 | 151 | 0 |
| 2 | 100 | 5 | 1 | 407.2 | 100 | 0 |
| 3 | 135 | 8 | 2 | 403.7 | 135 | 0 |
| 4 | 107 | 9 | 5 | 445.6 | 107 | 0 |
| 5 | 156 | 9 | 4 | 425.8 | 156 | 0 |
| 6 | 72 | 3 | 3 | 429.3 | 72 | 0 |
| 7 | 88 | 11 | 5 | 449.4 | 88 | 0 |
| 8 | 96 | 11 | 1 | 439.2 | 96 | 0 |
| 9 | 120 | 11 | 1 | 457.4 | 120 | 0 |

La cantidad de Pokémon por generación coincide con la referencia oficial en las nueve generaciones.

### 4.6 Valores atípicos (regla del rango intercuartílico)

| Variable | Valores atípicos |
|---|---|
| hp | 18 |
| ataque | 1 |
| defensa | 11 |
| ataque_especial | 1 |
| defensa_especial | 11 |
| velocidad | 2 |
| total | 0 |

### 4.7 Efecto de legendarios y míticos

| Grupo | Promedio del total |
|---|---|
| Todos los Pokémon | 427.7 |
| Sin legendarios ni míticos | 411.1 |
| Solo legendarios y míticos | 592.0 |

## 5. Principales hallazgos de calidad

| Dataset | Problema identificado | Evidencia encontrada | Posible impacto | Acción propuesta |
|---|---|---|---|---|
| pokemon_pokeapi.csv | `tipo_2` con muchos valores nulos | 499 nulos (48.68 %); equivalen a Pokémon de un solo tipo | Afecta solo si se analizan los tipos: los promedios por tipo secundario excluirían a casi la mitad de los registros | Conservar los nulos; si se analiza por tipo, reemplazarlos por una categoría explícita como `ninguno` en una copia del DataFrame |
| pokemon_pokeapi.csv | Valores atípicos en las estadísticas | 18 en `hp`, 11 en `defensa`, 11 en `defensa_especial`, 2 en `velocidad`, 1 en `ataque`, 1 en `ataque_especial` | Pueden desplazar el promedio de las generaciones donde aparezcan | Listar los registros atípicos y confirmar que son valores reales del juego antes de decidir si se conservan o se analizan por separado |
| pokemon_pokeapi.csv | Legendarios y míticos sesgan el promedio | Promedio del total: 592.0 en legendarios y míticos frente a 411.1 en el resto | Las generaciones con más legendarios (7, 8 y 9, con 11 legendarios cada una) podrían parecer más fuertes por su composición y no por un cambio de diseño general | Calcular los promedios por generación con y sin legendarios y míticos y comparar |
| pokemon_pokeapi.csv | Generaciones con tamaños muy distintos | De 72 Pokémon en la generación 6 a 156 en la generación 5 | Los promedios de generaciones pequeñas son más sensibles a casos individuales | Reportar el número de Pokémon junto a cada promedio |
| pokemon_pokeapi.csv | El dataset contiene una sola fuente y una sola forma por Pokémon | 1025 registros, uno por Pokémon, sin formas alternativas; sin segunda fuente cargada | No permite contrastar valores ni estudiar megaevoluciones o formas regionales; no se cumple todavía la validación con una segunda fuente prevista en la formulación del proyecto | Contrastar una muestra con otra fuente (por ejemplo, un dataset de Kaggle o Bulbapedia) y documentar si se incluirán formas alternativas |
| pokemon_pokeapi.csv | La generación indica cuándo apareció el Pokémon, no cuándo se midió su estadística | Columna `generacion` única por Pokémon | Las estadísticas son las actuales en la API; si alguna fue modificada en una generación posterior, la comparación por generación refleja valores vigentes y no los originales | Documentarlo como limitación en el análisis y, de ser posible, verificar casos puntuales en Bulbapedia |

## 6. Acciones de limpieza y preparación propuestas

1. Mantener los nulos de `tipo_2` y definir una categoría explícita (`ninguno`) solo en los análisis por tipo.
2. Listar los registros atípicos en `hp`, `defensa` y `defensa_especial` y confirmar su validez con una segunda fuente.
3. Crear una columna auxiliar `especial` (legendario o mítico) para calcular los promedios con y sin estos casos.
4. Incluir el número de Pokémon por generación en las tablas de resultados.
5. Contrastar una muestra de registros con otra fuente antes de dar por validados los datos.
6. Definir si se incorporarán las formas alternativas (megaevoluciones, formas regionales) o si el análisis se limitará a la forma base.

En esta actividad no se ejecutó ninguna limpieza; el objetivo fue diagnosticar y documentar.

## 7. Conclusiones

- El dataset está completo y es consistente: no hay duplicados, los tipos de dato son coherentes y todas las verificaciones de inconsistencia dieron cero casos. El único valor faltante estructural es `tipo_2`, y corresponde a Pokémon de un solo tipo.
- Las condiciones actuales permiten continuar con el análisis de la pregunta analítica. Sin embargo, antes de comparar promedios entre generaciones conviene tratar los legendarios y míticos por separado, reportar el tamaño de cada generación y revisar los valores atípicos.
- Las limitaciones más importantes no son de captura sino de alcance: una sola fuente, una sola forma por Pokémon y estadísticas vigentes en lugar de históricas. Deben quedar documentadas al presentar los resultados.
- Los promedios del total por generación (de 403.7 en la generación 3 a 457.4 en la generación 9) son un dato preliminar del diagnóstico y no una conclusión sobre la pregunta analítica, que se responderá en la etapa de análisis.
