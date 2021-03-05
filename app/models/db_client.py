from models.asset import Asset
from models.object import Object
from models.scenario import Scenario
from models.scene import Scene
from models.statistics import Statistics
from models.text import Text

from . import Base, engine
from .sessionManager import SessionManager


# TODO: move session creating and closing out of these individual calls
def create_entity(data):
    # create the session
    Base.metadata.create_all(engine)
    session = SessionManager.get_session()

    # add the entity to the session
    session.add(data)

    # commit the change to the database
    session.commit()

    # refresh the data to get the id autopopulated in database
    session.refresh(data)

    # close the session
    SessionManager.yield_session()

    # return the id to the caller
    return data


# TODO: move session creating and closing out of these individual calls
def get_assets():
    session = SessionManager.get_session()
    assets = session.query(Asset).all()
    SessionManager.yield_session()
    return assets


# TODO: move session creating and closing out of these individual calls
def get_asset(id):
    session = SessionManager.get_session()
    asset = session.query(Asset).get(id)
    SessionManager.yield_session()
    return asset


# TODO: move session creating and closing out of these individual calls
def delete_asset(id):
    try:
        session = SessionManager.get_session()

        exists = session.query(Asset).filter(Asset.id == id).first() is not None
        if exists:
            session.query(Asset).filter(Asset.id == id).delete()
            session.commit()

        SessionManager.yield_session()
    except Exception as e:
        raise e

    return exists


# TODO: move session creating and closing out of these individual calls
def get_objects():
    session = SessionManager.get_session()
    objects = session.query(Object).all()
    SessionManager.yield_session()
    return objects


# TODO: move session creating and closing out of these individual calls
def get_object(id):
    session = SessionManager.get_session()
    obj = session.query(Object).get(id)
    SessionManager.yield_session()
    return obj


# TODO: move session creating and closing out of these individual calls
def delete_object(id):
    try:
        session = SessionManager.get_session()

        exists = session.query(Object).filter(Object.id == id).first() is not None
        if exists:
            session.query(Object).filter(Object.id == id).delete()
            session.commit()

        SessionManager.yield_session()
    except Exception as e:
        raise e

    return exists


# TODO: move session creating and closing out of these individual calls
def get_scenarios():
    session = SessionManager.get_session()
    scenarios = session.query(Scenario).all()
    SessionManager.yield_session()
    return scenarios


# TODO: move session creating and closing out of these individual calls
def get_scenario(id):
    session = SessionManager.get_session()
    scenario = session.query(Scenario).get(id)
    SessionManager.yield_session()
    return scenario


# TODO: move session creating and closing out of these individual calls
def delete_scenario(id):
    try:
        session = SessionManager.get_session()

        exists = session.query(Scenario).filter(Scenario.id == id).first() is not None
        if exists:
            session.query(Scenario).filter(Scenario.id == id).delete()
            session.commit()

        SessionManager.yield_session()
    except Exception as e:
        raise e

    return exists


# TODO: move session creating and closing out of these individual calls
def get_scenes():
    session = SessionManager.get_session()
    scenes = session.query(Scene).all()
    SessionManager.yield_session()
    return scenes


# TODO: move session creating and closing out of these individual calls
def get_scene(id):
    session = SessionManager.get_session()
    scene = session.query(Scene).get(id)
    SessionManager.yield_session()
    return scene


# TODO: move session creating and closing out of these individual calls
def delete_scene(id):
    try:
        session = SessionManager.get_session()

        exists = session.query(Scene).filter(Scene.id == id).first() is not None
        if exists:
            session.query(Scene).filter(Scene.id == id).delete()
            session.commit()

        SessionManager.yield_session()
    except Exception as e:
        raise e

    return exists


# TODO: move session creating and closing out of these individual calls
def get_statistics():
    session = SessionManager.get_session()
    stats = session.query(Statistics).all()
    SessionManager.yield_session()
    return stats


# TODO: move session creating and closing out of these individual calls
def get_statistic(id):
    session = SessionManager.get_session()
    stat = session.query(Statistics).get(id)
    SessionManager.yield_session()
    return stat


# TODO: move session creating and closing out of these individual calls
def delete_statistic(id):
    try:
        session = SessionManager.get_session()

        exists = (
            session.query(Statistics).filter(Statistics.id == id).first() is not None
        )
        if exists:
            session.query(Statistics).filter(Statistics.id == id).delete()
            session.commit()

        SessionManager.yield_session()
    except Exception as e:
        raise e

    return exists


# TODO: move session creating and closing out of these individual calls
def get_texts():
    session = SessionManager.get_session()
    texts = session.query(Text).all()
    SessionManager.yield_session()
    return texts


# TODO: move session creating and closing out of these individual calls
def get_text(id):
    session = SessionManager.get_session()
    text = session.query(Text).get(id)
    SessionManager.yield_session()
    return text


# TODO: move session creating and closing out of these individual calls
def put_asset(id, data):
    try:
        session = SessionManager.get_session()
        asset = (
            session.query(Asset)
            .filter(Asset.id == id)
            .update(data, synchronize_session="fetch")
        )
        session.commit()
        SessionManager.yield_session()
    except Exception as e:
        raise e
    return asset


# TODO: move session creating and closing out of these individual calls
def put_object(id, data):
    try:
        session = SessionManager.get_session()
        obj = (
            session.query(Object)
            .filter(Object.id == id)
            .update(data, synchronize_session="fetch")
        )
        session.commit()
        SessionManager.yield_session()
    except Exception as e:
        raise e
    return obj


# TODO: move session creating and closing out of these individual calls
def put_scenario(id, data):
    try:
        session = SessionManager.get_session()
        scenario = (
            session.query(Scenario)
            .filter(Scenario.id == id)
            .update(data, synchronize_session="fetch")
        )
        session.commit()
        SessionManager.yield_session()
    except Exception as e:
        raise e
    return scenario


# TODO: move session creating and closing out of these individual calls
def put_scene(id, data):
    try:
        session = SessionManager.get_session()
        scene = (
            session.query(Scene)
            .filter(Scene.id == id)
            .update(data, synchronize_session="fetch")
        )
        session.commit()
        SessionManager.yield_session()
    except Exception as e:
        raise e
    return scene


# TODO: move session creating and closing out of these individual calls
def put_statistics(id, data):
    try:
        session = SessionManager.get_session()
        statistics = (
            session.query(Statistics)
            .filter(Statistics.id == id)
            .update(data, synchronize_session="fetch")
        )
        session.commit()
        SessionManager.yield_session()
    except Exception as e:
        raise e
    return statistics


# TODO: move session creating and closing out of these individual calls
def put_text(id, data):
    try:
        session = SessionManager.get_session()
        text = (
            session.query(Text)
            .filter(Text.id == id)
            .update(data, synchronize_session="fetch")
        )
        session.commit()
        SessionManager.yield_session()
    except Exception as e:
        raise e
    return text


def delete_text(id):
    try:
        session = SessionManager.get_session()

        exists = session.query(Text).filter(Text.id == id).first() is not None
        if exists:
            session.query(Text).filter(Text.id == id).delete()
            session.commit()

        SessionManager.yield_session()
    except Exception as e:
        raise e

    return exists
