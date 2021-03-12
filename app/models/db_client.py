from models.asset import Asset
from models.object import Object
from models.scenario import Scenario
from models.scene import Scene
from models.statistics import Statistics
from models.text import Text

from . import Base, engine


def create_entity(data, session):
    # create the session
    Base.metadata.create_all(engine)

    # add the entity to the session
    session.add(data)

    # commit the change to the database
    session.commit()

    # refresh the data to get the id autopopulated in database
    session.refresh(data)

    # return the id to the caller
    return data


def get_assets(session):
    assets = session.query(Asset).all()
    return assets


def get_asset(id, session):
    asset = session.query(Asset).get(id)
    return asset


def delete_asset(id, session):
    try:
        exists = session.query(Asset).filter(Asset.id == id).first() is not None
        if exists:
            session.query(Asset).filter(Asset.id == id).delete()
            session.commit()

    except Exception as e:
        raise e

    return exists


def get_objects(session):
    objects = session.query(Object).all()
    return objects


def get_object(id, session):
    obj = session.query(Object).get(id)
    return obj


def delete_object(id, session):
    try:
        exists = session.query(Object).filter(Object.id == id).first() is not None
        if exists:
            session.query(Object).filter(Object.id == id).delete()
            session.commit()

    except Exception as e:
        raise e

    return exists


def get_scenarios(session):
    scenarios = session.query(Scenario).all()
    return scenarios


def get_scenario(id, session):
    scenario = session.query(Scenario).get(id)
    return scenario


def delete_scenario(id, session):
    try:
        exists = session.query(Scenario).filter(Scenario.id == id).first() is not None
        if exists:
            session.query(Scenario).filter(Scenario.id == id).delete()
            session.commit()

    except Exception as e:
        raise e

    return exists


def get_scenes(session):
    scenes = session.query(Scene).all()
    return scenes


def get_scene(id, session):
    scene = session.query(Scene).get(id)
    return scene


def delete_scene(id, session):
    try:
        exists = session.query(Scene).filter(Scene.id == id).first() is not None
        if exists:
            session.query(Scene).filter(Scene.id == id).delete()
            session.commit()

    except Exception as e:
        raise e

    return exists


def get_statistics(session):
    stats = session.query(Statistics).all()
    return stats


def get_statistic(id, session):
    stat = session.query(Statistics).get(id)
    return stat


def delete_statistic(id, session):
    try:
        exists = (
            session.query(Statistics).filter(Statistics.id == id).first() is not None
        )
        if exists:
            session.query(Statistics).filter(Statistics.id == id).delete()
            session.commit()

    except Exception as e:
        raise e

    return exists


def get_texts(session):
    texts = session.query(Text).all()
    return texts


def get_text(id, session):
    text = session.query(Text).get(id)
    return text


def put_asset(id, data, session):
    try:
        asset = (
            session.query(Asset)
            .filter(Asset.id == id)
            .update(data, synchronize_session="fetch")
        )
        session.commit()
    except Exception as e:
        raise e
    return asset


def put_object(id, data, session):
    try:
        obj = (
            session.query(Object)
            .filter(Object.id == id)
            .update(data, synchronize_session="fetch")
        )
        session.commit()
    except Exception as e:
        raise e
    return obj


def put_scenario(id, data, session):
    try:
        scenario = (
            session.query(Scenario)
            .filter(Scenario.id == id)
            .update(data, synchronize_session="fetch")
        )
        session.commit()
    except Exception as e:
        raise e
    return scenario


def put_scene(id, data, session):
    try:
        scene = (
            session.query(Scene)
            .filter(Scene.id == id)
            .update(data, synchronize_session="fetch")
        )
        session.commit()
    except Exception as e:
        raise e
    return scene


def put_statistics(id, data, session):
    try:
        statistics = (
            session.query(Statistics)
            .filter(Statistics.id == id)
            .update(data, synchronize_session="fetch")
        )
        session.commit()
    except Exception as e:
        raise e
    return statistics


def put_text(id, data, session):
    try:
        text = (
            session.query(Text)
            .filter(Text.id == id)
            .update(data, synchronize_session="fetch")
        )
        session.commit()
    except Exception as e:
        raise e
    return text


def delete_text(id, session):
    try:
        exists = session.query(Text).filter(Text.id == id).first() is not None
        if exists:
            session.query(Text).filter(Text.id == id).delete()
            session.commit()

    except Exception as e:
        raise e

    return exists
