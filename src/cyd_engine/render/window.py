from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from cyd_engine.core.config import EngineConfig
from cyd_engine.entities.database import EntityCatalog
from cyd_engine.render.renderer import ModernGLRenderer
from cyd_engine.render.shapes import MeshFactory
from cyd_engine.ui.dialogs import UIWindowManager
from cyd_engine.world.models import WorldData


@dataclass(slots=True)
class GameWindow:
    config: EngineConfig
    world: WorldData
    entity_catalog: EntityCatalog
    ui_manager: UIWindowManager

    @staticmethod
    def _read_fps(pyglet_module: Any) -> float:
        """
        Compatibilidad entre versiones de pyglet:
        - pyglet 1.x: pyglet.clock.get_fps()
        - pyglet 2.x: pyglet.clock.get_default().get_fps()
        """
        get_fps = getattr(pyglet_module.clock, "get_fps", None)
        if callable(get_fps):
            return float(get_fps())

        get_default = getattr(pyglet_module.clock, "get_default", None)
        if callable(get_default):
            default_clock = get_default()
            default_get_fps = getattr(default_clock, "get_fps", None)
            if callable(default_get_fps):
                return float(default_get_fps())

        return 0.0

    def start_loop(self, target_fps: int) -> None:
        """Inicia la ventana y loop de pyglet con fallback sin bloqueo para pruebas."""
        try:
            import pyglet
        except ModuleNotFoundError:
            print("pyglet no está instalado. Motor inicializado en modo headless.")
            return
        try:
            import moderngl
        except ModuleNotFoundError:
            print("moderngl no está instalado. Motor inicializado en modo headless.")
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
        ctx = moderngl.create_context()
        renderer = ModernGLRenderer(ctx=ctx)
        renderer.setup(terrain_mesh)
        ctx.enable(moderngl.DEPTH_TEST)
        ctx.wireframe = self.config.low_spec_mode

        @window.event
        def on_draw() -> None:
            renderer.render()
            fps = self._read_fps(pyglet)
            window.set_caption(f"{self.config.title} | FPS: {fps:.1f} | tris:{terrain_mesh.triangle_count}")

        @window.event
        def on_key_press(symbol, modifiers) -> None:  # type: ignore[no-untyped-def]
            if symbol == pyglet.window.key.I:
                self.ui_manager.toggle_window("inventory")
            if symbol == pyglet.window.key.ESCAPE:
                window.close()

        pyglet.clock.schedule_interval(lambda dt: dt, 1 / max(1, target_fps))
        pyglet.app.run()
