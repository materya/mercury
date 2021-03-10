import configparser
import importlib
import logging
from distutils import util

from mercury import Engine, Timeframe


config = configparser.ConfigParser()
config.read("config.cfg")
params = config["main"]

log_levels = importlib.import_module("logging")
level = getattr(log_levels, params["logging"])
logging.basicConfig(
    level=level,
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def main():
    brokers = importlib.import_module("mercury.extras.brokers")
    Broker = getattr(brokers, params["broker"])
    broker_config = config[params["broker"]]
    broker = Broker(is_paper=bool(util.strtobool(params["is_paper"])),
                    **broker_config)

    strategies = importlib.import_module("mercury.extras.strategies")
    Strategy = getattr(strategies, params["strategy"])

    engine = Engine(broker=broker, strategy=Strategy)
    engine.start(instrument=broker_config["instrument"],
                 timeframe=Timeframe[params["timeframe"]],
                 warmup=int(params["warmup"]))


if __name__ == "__main__":
    main()
