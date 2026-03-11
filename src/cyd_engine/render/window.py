from __future__ import annotations

from dataclasses import dataclass

from cyd_engine.core.config import EngineConfig
from cyd_engine.entities.database import EntityCatalog
from cyd_engine.render.shapes import MeshFactory
from cyd_engine.ui.dialogs import UIWindowManager
from cyd_engine.world.models import WorldData


@dataclass(slots=True)
class GameWindow:
    config: EngineConfig
    world: WorldData
    entity_catalog: EntityCatalog
    ui_manager: UIWindowManager

    def start_loop(self, target_fps: int) -> None:
        """Inicia la ventana y loop de pyglet con fallback sin bloqueo para pruebas."""
        try:
            import pyglet
        except ModuleNotFoundError:
            print("pyglet no está instalado. Motor inicializado en modo headless.")
            return

        window = pyglet.window.Window(
            width=self.config.width,
            height=self.config.height,
            caption=self.config.title,
            vsync=self.config.use_vsync,
            resizable=True,
        )

        mesh_factory = MeshFactory()
        terrain_mesh = mesh_factory.from_heightmap(self.world.heightmap)

        @window.event
        def on_draw() -> None:
            window.clear()
            # Etapa inicial: solo debug textual para mantenerlo ultraligero.
            fps = pyglet.clock.get_fps()
            window.set_caption(f"{self.config.title} | FPS: {fps:.1f} | tris:{terrain_mesh.triangle_count}")

        @window.event
        def on_key_press(symbol, modifiers) -> None:  # type: ignore[no-untyped-def]
            if symbol == pyglet.window.key.I:
                self.ui_manager.toggle_window("inventory")
            if symbol == pyglet.window.key.ESCAPE:
                window.close()

        pyglet.clock.schedule_interval(lambda dt: dt, 1 / max(1, target_fps))
        pyglet.app.run()
