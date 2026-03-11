from dataclasses import dataclass


@dataclass(slots=True)
class EngineConfig:
    """Configuración base orientada a hardware limitado."""

    width: int = 960
    height: int = 540
    title: str = "Craft Your Destiny Engine"
    target_fps: int = 30
    low_spec_mode: bool = True
    use_vsync: bool = False
    world_seed: int = 42
    world_size_km: int = 16
    enable_opengl_debug: bool = False
