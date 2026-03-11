from dataclasses import dataclass, field


@dataclass(slots=True)
class UIWindow:
    key: str
    title: str
    visible: bool = False


@dataclass(slots=True)
class UIWindowManager:
    windows: dict[str, UIWindow] = field(default_factory=dict)

    def __post_init__(self) -> None:
        defaults = [
            UIWindow("inventory", "Inventario"),
            UIWindow("skills", "Arbol de habilidades"),
            UIWindow("technology", "Arbol de tecnologias"),
            UIWindow("dialog", "Dialogo"),
        ]
        for win in defaults:
            self.windows[win.key] = win

    def toggle_window(self, key: str) -> None:
        if key in self.windows:
            self.windows[key].visible = not self.windows[key].visible

    def visible_windows(self) -> list[UIWindow]:
        return [w for w in self.windows.values() if w.visible]
