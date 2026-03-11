from __future__ import annotations

from dataclasses import dataclass, field
from time import perf_counter

from cyd_engine.core.config import EngineConfig
from cyd_engine.entities.database import default_entity_catalog
from cyd_engine.render.window import GameWindow
from cyd_engine.ui.dialogs import UIWindowManager
from cyd_engine.world.generator import WorldGenerator


@dataclass(slots=True)
class Engine:
    config: EngineConfig
    world_generator: WorldGenerator = field(init=False)
    ui_manager: UIWindowManager = field(default_factory=UIWindowManager)
    running: bool = field(default=False, init=False)

    def __post_init__(self) -> None:
        self.world_generator = WorldGenerator(seed=self.config.world_seed)

    def bootstrap(self) -> GameWindow:
        world = self.world_generator.generate(
            size_km=self.config.world_size_km,
            low_spec_mode=self.config.low_spec_mode,
        )
        entity_catalog = default_entity_catalog()
        return GameWindow(
            config=self.config,
            world=world,
            entity_catalog=entity_catalog,
            ui_manager=self.ui_manager,
        )

    def run(self) -> None:
        window = self.bootstrap()
        self.running = True
        window.start_loop(target_fps=self.config.target_fps)


@dataclass(slots=True)
class EngineProfiler:
    """Medición simple de tiempos para optimizar en hardware modesto."""

    _start: float = field(default=0.0, init=False)

    def begin(self) -> None:
        self._start = perf_counter()

    def end_ms(self) -> float:
        return (perf_counter() - self._start) * 1000.0
