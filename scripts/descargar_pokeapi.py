"""Descarga los 1025 Pokémon desde PokéAPI y los guarda en data/raw/pokemon_pokeapi.csv"""
import csv
import time
from pathlib import Path

import requests

BASE = "https://pokeapi.co/api/v2"
SALIDA = Path("data/raw/pokemon_pokeapi.csv")
TOTAL = 1025

ROMANOS = {"i": 1, "ii": 2, "iii": 3, "iv": 4, "v": 5,
           "vi": 6, "vii": 7, "viii": 8, "ix": 9}
STATS = {"hp": "hp", "attack": "ataque", "defense": "defensa",
         "special-attack": "ataque_especial",
         "special-defense": "defensa_especial", "speed": "velocidad"}
CAMPOS = ["id", "nombre", "generacion", "tipo_1", "tipo_2",
          "legendario", "mitico", "hp", "ataque", "defensa",
          "ataque_especial", "defensa_especial", "velocidad", "total"]


def pedir(sesion, url, intentos=3):
    for i in range(intentos):
        r = sesion.get(url, timeout=30)
        if r.status_code == 200:
            return r.json()
        time.sleep(2 * (i + 1))
    raise RuntimeError(f"No se pudo obtener {url}")


def main():
    SALIDA.parent.mkdir(parents=True, exist_ok=True)
    sesion = requests.Session()
    with open(SALIDA, "w", newline="", encoding="utf-8") as f:
        escritor = csv.DictWriter(f, fieldnames=CAMPOS)
        escritor.writeheader()
        for n in range(1, TOTAL + 1):
            poke = pedir(sesion, f"{BASE}/pokemon/{n}")
            especie = pedir(sesion, f"{BASE}/pokemon-species/{n}")

            tipos = [t["type"]["name"] for t in poke["types"]]
            fila = {
                "id": n,
                "nombre": poke["name"],
                "generacion": ROMANOS[especie["generation"]["name"].split("-")[1]],
                "tipo_1": tipos[0],
                "tipo_2": tipos[1] if len(tipos) > 1 else "",
                "legendario": especie["is_legendary"],
                "mitico": especie["is_mythical"],
            }
            total = 0
            for s in poke["stats"]:
                valor = s["base_stat"]
                fila[STATS[s["stat"]["name"]]] = valor
                total += valor
            fila["total"] = total
            escritor.writerow(fila)

            if n % 100 == 0:
                print(f"{n}/{TOTAL}")
            time.sleep(0.05)
    print(f"Listo: {SALIDA}")


if __name__ == "__main__":
    main()