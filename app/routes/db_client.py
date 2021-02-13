from ..models.asset import Asset
from ..models.object import Object
from ..models.scenario import Scenario
from ..models.scene import Scene
from ..models.statistics import Statistics
from ..models.text import Text


def create_asset(data):
    return Asset.create(**data)


def get_assets():
    return Asset.query.all()


def get_asset(id):
    return Asset.get(id)


def create_object(data):
    return Object.create(**data)


def get_objects():
    return Object.query.all()


def get_object(id):
    return Object.get(id)


def create_scenario(data):
    return Scenario.create(**data)


def get_scenarios():
    return Scenario.query.all()


def get_scenario(id):
    return Scenario.get(id)


def create_scenes(data):
    return Scene.create(**data)


def get_scenes():
    return Scene.query.all()


def get_scene(id):
    return Scene.get(id)


def create_statistic(data):
    return Statistics.create(**data)


def get_statistics():
    return Statistics.query.all()


def get_statistic(id):
    return Statistics.get(id)


def create_text(data):
    return Text.create(**data)


def get_texts():
    return Text.query.all()


def get_text(id):
    return Text.get(id)
