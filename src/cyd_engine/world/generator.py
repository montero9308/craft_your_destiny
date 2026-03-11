from __future__ import annotations

import random
from dataclasses import dataclass

from cyd_engine.world.models import Biome, WorldData


@dataclass(slots=True)
class WorldGenerator:
    seed: int

    def generate(self, size_km: int, low_spec_mode: bool = True) -> WorldData:
        resolution = self._choose_resolution(size_km, low_spec_mode)
        rng = random.Random(self.seed + size_km * 97)
        base = self._heightmap(resolution, rng)
        normalized = self._normalize(base)
        biomes = self._classify_biomes(normalized)
        return WorldData(size_km=size_km, resolution=resolution, heightmap=normalized, biome_map=biomes)

    @staticmethod
    def _choose_resolution(size_km: int, low_spec_mode: bool) -> int:
        # Escala: isla (8-16km) hasta continente (64-256km)
        base = 24 if low_spec_mode else 40
        return max(16, min(256, base + size_km))

    def _heightmap(self, resolution: int, rng: random.Random) -> list[list[float]]:
        data = [[rng.uniform(-1.0, 1.0) for _ in range(resolution)] for _ in range(resolution)]
        # Suavizado barato O(n^2)
        for _ in range(3):
            data = self._blur_pass(data)
        return data

    @staticmethod
    def _blur_pass(data: list[list[float]]) -> list[list[float]]:
        size = len(data)
        out = [[0.0] * size for _ in range(size)]
        for z in range(size):
            for x in range(size):
                total = 0.0
                samples = 0
                for dz in (-1, 0, 1):
                    for dx in (-1, 0, 1):
                        nz = z + dz
                        nx = x + dx
                        if 0 <= nz < size and 0 <= nx < size:
                            total += data[nz][nx]
                            samples += 1
                out[z][x] = total / samples
        return out

    @staticmethod
    def _normalize(data: list[list[float]]) -> list[list[float]]:
        values = [value for row in data for value in row]
        lo, hi = min(values), max(values)
        span = max(1e-6, hi - lo)
        return [[(value - lo) / span for value in row] for row in data]

    @staticmethod
    def _classify_biomes(heightmap: list[list[float]]) -> list[list[Biome]]:
        out: list[list[Biome]] = []
        for row in heightmap:
            biome_row: list[Biome] = []
            for h in row:
                if h < 0.32:
                    biome_row.append(Biome.WATER)
                elif h < 0.5:
                    biome_row.append(Biome.GRASSLAND)
                elif h < 0.67:
                    biome_row.append(Biome.FOREST)
                elif h < 0.82:
                    biome_row.append(Biome.DESERT)
                else:
                    biome_row.append(Biome.MOUNTAIN)
            out.append(biome_row)
        return out
