from cyd_engine.core.config import EngineConfig
from cyd_engine.core.engine import Engine


def main() -> None:
    config = EngineConfig()
    engine = Engine(config=config)
    engine.run()


if __name__ == "__main__":
    main()
