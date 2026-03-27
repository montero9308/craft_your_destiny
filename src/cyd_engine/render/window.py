from __future__ import annotations

from dataclasses import dataclass, field
from time import perf_counter

from cyd_engine.core.config import EngineConfig
from cyd_engine.entities.database import EntityCatalog
from cyd_engine.render.shapes import MeshFactory
from cyd_engine.render.camera import Camera
from cyd_engine.render.terrain_renderer import TerrainRenderer
from cyd_engine.render.grid_renderer import GridRenderer
from cyd_engine.ui.dialogs import UIWindowManager
from cyd_engine.world.models import WorldData


@dataclass(slots=True)
class FPSCounter:
    """Contador de FPS manual para pyglet."""
    
    _frame_times: list[float] = field(default_factory=list, init=False)
    _last_time: float = field(default=0.0, init=False)
    _max_samples: int = field(default=30, init=False)
    
    def __post_init__(self) -> None:
        self._last_time = perf_counter()
    
    def update(self) -> None:
        """Actualizar el contador con el tiempo del frame actual."""
        current_time = perf_counter()
        dt = current_time - self._last_time
        self._last_time = current_time
        
        self._frame_times.append(dt)
        if len(self._frame_times) > self._max_samples:
            self._frame_times.pop(0)
    
    def get_fps(self) -> float:
        """Obtener FPS promedio."""
        if not self._frame_times:
            return 0.0
        avg_dt = sum(self._frame_times) / len(self._frame_times)
        return 1.0 / avg_dt if avg_dt > 0 else 0.0


@dataclass(slots=True)
class GameWindow:
    config: EngineConfig
    world: WorldData
    entity_catalog: EntityCatalog
    ui_manager: UIWindowManager
    _fps_counter: FPSCounter = field(default_factory=lambda: FPSCounter(), init=False)

    def start_loop(self, target_fps: int) -> None:
        """Inicia la ventana y loop de pyglet con renderizado 3D."""
        try:
            import pyglet
            from pyglet.gl import (
                GL_DEPTH_TEST, GL_LIGHTING, GL_LIGHT0, GL_POSITION,
                GL_AMBIENT, GL_DIFFUSE, GL_COLOR_MATERIAL, GL_AMBIENT_AND_DIFFUSE,
                GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT,
                GL_PROJECTION, GL_MODELVIEW,
                glEnable, glClear, glClearColor, glViewport,
                glMatrixMode, glLoadIdentity, gluPerspective,
                glLightfv, glColorMaterial,
            )
            from pyglet.window import key, mouse
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

        # Configurar OpenGL
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_COLOR_MATERIAL)
        glColorMaterial(GL_AMBIENT_AND_DIFFUSE)
        glClearColor(0.5, 0.7, 0.9, 1.0)  # Cielo azul claro
        
        # Iluminación básica
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glLightfv(GL_LIGHT0, GL_POSITION, (1.0, 1.0, 1.0, 0.0))
        glLightfv(GL_LIGHT0, GL_AMBIENT, (0.3, 0.3, 0.3, 1.0))
        glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.8, 0.8, 0.8, 1.0))

        # Configurar proyección
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(60.0, window.width / window.height, 1.0, 1000.0)
        glMatrixMode(GL_MODELVIEW)

        # Crear renderizadores
        mesh_factory = MeshFactory()
        terrain_mesh = mesh_factory.from_heightmap(self.world.heightmap)
        terrain_renderer = TerrainRenderer(self.world, terrain_mesh)
        grid_renderer = GridRenderer(size=self.world.resolution, spacing=10)
        
        # Crear cámara
        camera = Camera(
            distance=self.world.resolution * 1.5,
            target=(self.world.resolution / 2, 0, self.world.resolution / 2)
        )
        camera.update_position()
        
        # Estado de controles
        mouse_pressed = False
        last_mouse_pos = (0, 0)
        show_grid = True
        show_wireframe = False

        @window.event
        def on_draw() -> None:
            window.clear()
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            
            # Actualizar FPS
            self._fps_counter.update()
            fps = self._fps_counter.get_fps()
            
            # Configurar vista
            glMatrixMode(GL_MODELVIEW)
            glLoadIdentity()
            camera.apply()
            
            # Renderizar grid de referencia
            if show_grid:
                grid_renderer.render()
            
            # Renderizar terreno
            if show_wireframe:
                from pyglet.gl import glPolygonMode, GL_FRONT_AND_BACK, GL_LINE, GL_FILL
                glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
                terrain_renderer.render()
                glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
            else:
                terrain_renderer.render()
            
            # Actualizar título
            window.set_caption(
                f"{self.config.title} | FPS: {fps:.1f} | "
                f"Tris: {terrain_mesh.triangle_count} | "
                f"Mundo: {self.world.size_km}km | "
                f"Res: {self.world.resolution}x{self.world.resolution} | "
                f"Cam: {camera.distance:.0f}u"
            )

        @window.event
        def on_key_press(symbol, modifiers):
            nonlocal show_grid, show_wireframe
            
            if symbol == key.I:
                self.ui_manager.toggle_window("inventory")
                print(f"Inventario: {'abierto' if self.ui_manager.windows['inventory'].visible else 'cerrado'}")
            elif symbol == key.K:
                self.ui_manager.toggle_window("skills")
                print(f"Habilidades: {'abierto' if self.ui_manager.windows['skills'].visible else 'cerrado'}")
            elif symbol == key.T:
                self.ui_manager.toggle_window("technology")
                print(f"Tecnología: {'abierto' if self.ui_manager.windows['technology'].visible else 'cerrado'}")
            elif symbol == key.D:
                self.ui_manager.toggle_window("dialog")
                print(f"Diálogo: {'abierto' if self.ui_manager.windows['dialog'].visible else 'cerrado'}")
            elif symbol == key.G:
                show_grid = not show_grid
                print(f"Grid: {'ON' if show_grid else 'OFF'}")
            elif symbol == key.W:
                show_wireframe = not show_wireframe
                print(f"Wireframe: {'ON' if show_wireframe else 'OFF'}")
            elif symbol == key.R:
                # Reset cámara
                camera.yaw = 45.0
                camera.pitch = -30.0
                camera.distance = self.world.resolution * 1.5
                camera.update_position()
                print("Cámara reseteada")
            elif symbol == key.ESCAPE:
                window.close()
            elif symbol == key.F1:
                # Debug info
                print("\n=== DEBUG INFO ===")
                print(f"Mundo: {self.world.size_km}km")
                print(f"Resolución: {self.world.resolution}x{self.world.resolution}")
                print(f"Triángulos: {terrain_mesh.triangle_count}")
                print(f"Vértices: {len(terrain_mesh.vertices)}")
                print(f"Cámara - Pos: {camera.position}")
                print(f"Cámara - Yaw: {camera.yaw:.1f}° Pitch: {camera.pitch:.1f}°")
                print(f"Cámara - Distancia: {camera.distance:.1f}")
                print(f"Razas jugables: {len(self.entity_catalog.playable_races)}")
                print(f"Razas enemigas: {len(self.entity_catalog.enemy_races)}")
                print(f"Especies animales: {len(self.entity_catalog.animal_species)}")
                print("==================\n")

        @window.event
        def on_mouse_press(x, y, button, modifiers):
            nonlocal mouse_pressed, last_mouse_pos
            if button == mouse.LEFT:
                mouse_pressed = True
                last_mouse_pos = (x, y)

        @window.event
        def on_mouse_release(x, y, button, modifiers):
            nonlocal mouse_pressed
            if button == mouse.LEFT:
                mouse_pressed = False

        @window.event
        def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
            if buttons & mouse.LEFT:
                # Rotar cámara
                camera.rotate(dx * 0.3, dy * 0.3)

        @window.event
        def on_mouse_scroll(x, y, scroll_x, scroll_y):
            # Zoom
            camera.zoom(-scroll_y * 5.0)

        @window.event
        def on_resize(width, height):
            glViewport(0, 0, width, height)
            glMatrixMode(GL_PROJECTION)
            glLoadIdentity()
            gluPerspective(60.0, width / height, 1.0, 1000.0)
            glMatrixMode(GL_MODELVIEW)

        print("\n=== CONTROLES ===")
        print("Mouse izquierdo + arrastrar: Rotar cámara")
        print("Rueda del mouse: Zoom")
        print("G: Toggle grid")
        print("W: Toggle wireframe")
        print("R: Reset cámara")
        print("I: Inventario")
        print("K: Habilidades")
        print("T: Tecnología")
        print("F1: Info de debug")
        print("ESC: Salir")
        print("=================\n")

        pyglet.clock.schedule_interval(lambda dt: None, 1 / max(1, target_fps))
        pyglet.app.run()
        
        # Cleanup
        terrain_renderer.cleanup()