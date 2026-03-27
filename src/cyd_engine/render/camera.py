from __future__ import annotations

from dataclasses import dataclass
from math import cos, sin, radians
from typing import Tuple


@dataclass(slots=True)
class Camera:
    """Cámara 3D con controles de órbita."""
    
    position: Tuple[float, float, float] = (0.0, 50.0, 100.0)
    target: Tuple[float, float, float] = (0.0, 0.0, 0.0)
    up: Tuple[float, float, float] = (0.0, 1.0, 0.0)
    
    # Parámetros de órbita
    distance: float = 100.0
    yaw: float = 45.0  # Rotación horizontal (grados)
    pitch: float = -30.0  # Rotación vertical (grados)
    
    # Límites
    min_distance: float = 10.0
    max_distance: float = 500.0
    min_pitch: float = -89.0
    max_pitch: float = 89.0
    
    def update_position(self) -> None:
        """Actualizar posición de la cámara basada en yaw, pitch y distance."""
        # Convertir a radianes
        yaw_rad = radians(self.yaw)
        pitch_rad = radians(self.pitch)
        
        # Calcular posición orbital
        x = self.target[0] + self.distance * cos(pitch_rad) * cos(yaw_rad)
        y = self.target[1] + self.distance * sin(pitch_rad)
        z = self.target[2] + self.distance * cos(pitch_rad) * sin(yaw_rad)
        
        self.position = (x, y, z)
    
    def rotate(self, delta_yaw: float, delta_pitch: float) -> None:
        """Rotar la cámara."""
        self.yaw += delta_yaw
        self.pitch += delta_pitch
        
        # Normalizar yaw
        self.yaw = self.yaw % 360.0
        
        # Limitar pitch
        self.pitch = max(self.min_pitch, min(self.max_pitch, self.pitch))
        
        self.update_position()
    
    def zoom(self, delta: float) -> None:
        """Acercar/alejar la cámara."""
        self.distance += delta
        self.distance = max(self.min_distance, min(self.max_distance, self.distance))
        self.update_position()
    
    def pan(self, delta_x: float, delta_z: float) -> None:
        """Mover el punto objetivo de la cámara."""
        self.target = (
            self.target[0] + delta_x,
            self.target[1],
            self.target[2] + delta_z
        )
        self.update_position()
    
    def apply(self) -> None:
        """Aplicar transformación de cámara (para usar con gluLookAt)."""
        from pyglet.gl import gluLookAt
        gluLookAt(
            self.position[0], self.position[1], self.position[2],
            self.target[0], self.target[1], self.target[2],
            self.up[0], self.up[1], self.up[2]
        )