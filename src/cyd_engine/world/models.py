from dataclasses import dataclass
from enum import StrEnum


class Biome(StrEnum):
    GRASSLAND = "pradera"
    FOREST = "bosque"
    DESERT = "desierto"
    MOUNTAIN = "montana"
    WATER = "agua"


@dataclass(slots=True)
class WorldData:
    size_km: int
    resolution: int
    heightmap: list[list[float]]
    biome_map: list[list[Biome]]
