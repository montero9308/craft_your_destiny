from cyd_engine.world.generator import WorldGenerator
from cyd_engine.world.models import Biome


def test_generation_is_deterministic() -> None:
    gen_a = WorldGenerator(seed=123)
    gen_b = WorldGenerator(seed=123)
    world_a = gen_a.generate(size_km=16, low_spec_mode=True)
    world_b = gen_b.generate(size_km=16, low_spec_mode=True)
    assert world_a.heightmap == world_b.heightmap
    assert world_a.biome_map == world_b.biome_map


def test_biomes_are_present() -> None:
    world = WorldGenerator(seed=777).generate(size_km=64, low_spec_mode=False)
    present = {biome for row in world.biome_map for biome in row}
    assert Biome.WATER in present
    assert Biome.MOUNTAIN in present
