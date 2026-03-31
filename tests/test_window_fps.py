from types import SimpleNamespace

from cyd_engine.render.window import GameWindow


def test_read_fps_legacy_clock_api() -> None:
    pyglet_like = SimpleNamespace(clock=SimpleNamespace(get_fps=lambda: 27.5))
    assert GameWindow._read_fps(pyglet_like) == 27.5


def test_read_fps_modern_clock_api() -> None:
    default_clock = SimpleNamespace(get_fps=lambda: 31.0)
    pyglet_like = SimpleNamespace(clock=SimpleNamespace(get_default=lambda: default_clock))
    assert GameWindow._read_fps(pyglet_like) == 31.0


def test_read_fps_missing_api_returns_zero() -> None:
    pyglet_like = SimpleNamespace(clock=SimpleNamespace())
    assert GameWindow._read_fps(pyglet_like) == 0.0
