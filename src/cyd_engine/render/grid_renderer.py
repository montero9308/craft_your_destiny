from __future__ import annotations


class GridRenderer:
    """Renderizador de grid de referencia."""
    
    def __init__(self, size: int = 100, spacing: int = 10) -> None:
        self.size = size
        self.spacing = spacing
    
    def render(self) -> None:
        """Renderizar grid."""
        from pyglet.gl import glBegin, glEnd, glVertex3f, glColor3f, GL_LINES
        
        glColor3f(0.3, 0.3, 0.3)
        glBegin(GL_LINES)
        
        # Líneas en X
        for z in range(-self.size, self.size + 1, self.spacing):
            glVertex3f(-self.size, 0, z)
            glVertex3f(self.size, 0, z)
        
        # Líneas en Z
        for x in range(-self.size, self.size + 1, self.spacing):
            glVertex3f(x, 0, -self.size)
            glVertex3f(x, 0, self.size)
        
        glEnd()
        
        # Ejes de referencia
        glBegin(GL_LINES)
        # Eje X (rojo)
        glColor3f(1.0, 0.0, 0.0)
        glVertex3f(0, 0, 0)
        glVertex3f(50, 0, 0)
        
        # Eje Y (verde)
        glColor3f(0.0, 1.0, 0.0)
        glVertex3f(0, 0, 0)
        glVertex3f(0, 50, 0)
        
        # Eje Z (azul)
        glColor3f(0.0, 0.0, 1.0)
        glVertex3f(0, 0, 0)
        glVertex3f(0, 0, 50)
        glEnd()