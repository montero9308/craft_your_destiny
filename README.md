# craft_your_destiny

Motor base para RPG procedural 3D en Python con enfoque **ligero** (hardware humilde) y arquitectura limpia para crecer a futuro.

## Objetivos de esta primera base

- Motor modular con `pyglet` + OpenGL listo para evolución.
- Generación procedural de mundo (isla -> continente) sin modelos externos.
- Catálogo inicial de entidades:
  - 5 razas jugables humanoides.
  - 25 razas enemigas.
  - 50 especies animales base.
  - Objetos interactuables y estáticos.
- Sistema de ventanas UI (inventario, habilidades, tecnología, diálogo).
- Soporte actual para mallas básicas low-poly generadas en runtime (cubo, cilindro, terreno por heightmap).
- Diseño preparado para añadir importación de modelos externos más adelante.

## Estructura

- `src/cyd_engine/core`: configuración y ciclo principal.
- `src/cyd_engine/world`: generación procedural y biomas.
- `src/cyd_engine/render`: ventana y fábrica de mallas.
- `src/cyd_engine/entities`: catálogos de razas, enemigos, animales y objetos.
- `src/cyd_engine/ui`: ventanas de interacción in-game.

## Instalación

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
```

## Ejecución

```bash
cyd-engine
```

> Si `pyglet` no está instalado, el motor arranca en modo headless sin ventana para facilitar pruebas en entornos limitados.

## Pruebas

```bash
pytest
```

## Siguiente fase sugerida

1. Pipeline de render low-poly real (VBO/VAO, iluminación simple).
2. LOD y culling para mapas grandes en CPUs lentos.
3. Sistema ECS mínimo para NPCs/enemigos/animales.
4. Persistencia de mundo y chunks.
5. UI in-game dibujada con batches de pyglet.
