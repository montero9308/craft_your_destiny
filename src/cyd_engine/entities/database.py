from dataclasses import dataclass


@dataclass(slots=True)
class EntityCatalog:
    playable_races: list[str]
    enemy_races: list[str]
    animal_species: list[str]
    interactable_objects: list[str]
    static_objects: list[str]


def default_entity_catalog() -> EntityCatalog:
    return EntityCatalog(
        playable_races=["humano", "elfo", "enano", "orco", "dracónido"],
        enemy_races=[f"enemigo_raza_{i:02d}" for i in range(1, 26)],
        animal_species=[f"especie_{i:02d}" for i in range(1, 51)],
        interactable_objects=["arma", "recipiente", "armadura", "herramienta", "consumible"],
        static_objects=["edificio", "decoracion", "arbol", "roca", "puente"],
    )
