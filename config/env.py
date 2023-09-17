import configparser

config = configparser.ConfigParser()
config.read("config.ini")

pylama_config = {}
isort_config = {}
black_config = {}

if config.has_section("pylama"):
    pylama_config = config["pylama"]

if config.has_section("isort"):
    isort_config = config["isort"]

if config.has_section("black"):
    black_config = config["black"]
