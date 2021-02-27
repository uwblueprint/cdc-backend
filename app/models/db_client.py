from models.asset import Asset
from models.object import Object
from models.scenario import Scenario
from models.scene import Scene
from models.statistics import Statistics
from models.text import Text

from . import Base, Session, engine


# TODO: move session creating and closing out of these individual calls
def create_entity(data):
    # create the session
    Base.metadata.create_all(engine)
    session = Session()

    # add the entity to the session
    session.add(data)

    # commit the change to the database
    session.commit()

    # refresh the data to get the id autopopulated in database
    session.refresh(data)

    # close the session
    session.close()

    # return the id to the caller
    return data


# TODO: move session creating and closing out of these individual calls
def get_assets():
    session = Session()
    assets = session.query(Asset).all()
    session.close()
    return assets


# TODO: move session creating and closing out of these individual calls
def get_asset(id):
    session = Session()
    asset = session.query(Asset).get(id)
    session.close()
    return asset


# TODO: move session creating and closing out of these individual calls
def delete_asset(id):
    try:
        session = Session()

        exists = session.query(Asset).filter(Asset.id == id).first() is not None
        if exists:
            session.query(Asset).filter(Asset.id == id).delete()
            session.commit()

        session.close()
    except Exception as e:
        raise e

    return exists


# TODO: move session creating and closing out of these individual calls
def get_objects():
    session = Session()
    objects = session.query(Object).all()
    session.close()
    return objects


# TODO: move session creating and closing out of these individual calls
def get_object(id):
    session = Session()
    obj = session.query(Object).get(id)
    session.close()
    return obj


# TODO: move session creating and closing out of these individual calls
def delete_object(id):
    try:
        session = Session()

        exists = session.query(Object).filter(Object.id == id).first() is not None
        if exists:
            session.query(Object).filter(Object.id == id).delete()
            session.commit()

        session.close()
    except Exception as e:
        raise e

    return exists


# TODO: move session creating and closing out of these individual calls
def get_scenarios():
    session = Session()
    scenarios = session.query(Scenario).all()
    session.close()
    return scenarios


# TODO: move session creating and closing out of these individual calls
def get_scenario(id):
    session = Session()
    scenario = session.query(Scenario).get(id)
    session.close()
    return scenario


# TODO: move session creating and closing out of these individual calls
def delete_scenario(id):
    try:
        session = Session()

        exists = session.query(Scenario).filter(Scenario.id == id).first() is not None
        if exists:
            session.query(Scenario).filter(Scenario.id == id).delete()
            session.commit()

        session.close()
    except Exception as e:
        raise e

    return exists


# TODO: move session creating and closing out of these individual calls
def get_scenes():
    session = Session()
    scenes = session.query(Scene).all()
    session.close()
    return scenes


# TODO: move session creating and closing out of these individual calls
def get_scene(id):
    session = Session()
    scene = session.query(Scene).get(id)
    session.close()
    return scene


# TODO: move session creating and closing out of these individual calls
def delete_scene(id):
    try:
        session = Session()

        exists = session.query(Scene).filter(Scene.id == id).first() is not None
        if exists:
            session.query(Scene).filter(Scene.id == id).delete()
            session.commit()

        session.close()
    except Exception as e:
        raise e

    return exists


# TODO: move session creating and closing out of these individual calls
def get_statistics():
    session = Session()
    stats = session.query(Statistics).all()
    session.close()
    return stats


# TODO: move session creating and closing out of these individual calls
def get_statistic(id):
    session = Session()
    stat = session.query(Statistics).get(id)
    session.close()
    return stat


# TODO: move session creating and closing out of these individual calls
def delete_statistic(id):
    try:
        session = Session()

        exists = (
            session.query(Statistics).filter(Statistics.id == id).first() is not None
        )
        if exists:
            session.query(Statistics).filter(Statistics.id == id).delete()
            session.commit()

        session.close()
    except Exception as e:
        raise e

    return exists


# TODO: move session creating and closing out of these individual calls
def get_texts():
    session = Session()
    texts = session.query(Text).all()
    session.close()
    return texts


# TODO: move session creating and closing out of these individual calls
def get_text(id):
    session = Session()
    text = session.query(Text).get(id)
    session.close()
    return text


# TODO: move session creating and closing out of these individual calls
def put_asset(id, data):
    try:
        session = Session()
        asset = (
            session.query(Asset)
            .filter(Asset.id == id)
            .update(data, synchronize_session="fetch")
        )
        session.commit()
        session.close()
    except Exception as e:
        raise e
    return asset


# TODO: move session creating and closing out of these individual calls
def put_object(id, data):
    try:
        session = Session()
        obj = (
            session.query(Object)
            .filter(Object.id == id)
            .update(data, synchronize_session="fetch")
        )
        session.commit()
        session.close()
    except Exception as e:
        raise e
    return obj


# TODO: move session creating and closing out of these individual calls
def put_scenario(id, data):
    try:
        session = Session()
        scenario = (
            session.query(Scenario)
            .filter(Scenario.id == id)
            .update(data, synchronize_session="fetch")
        )
        session.commit()
        session.close()
    except Exception as e:
        raise e
    return scenario


# TODO: move session creating and closing out of these individual calls
def put_scene(id, data):
    try:
        session = Session()
        scene = (
            session.query(Scene)
            .filter(Scene.id == id)
            .update(data, synchronize_session="fetch")
        )
        session.commit()
        session.close()
    except Exception as e:
        raise e
    return scene


# TODO: move session creating and closing out of these individual calls
def put_statistics(id, data):
    try:
        session = Session()
        statistics = (
            session.query(Statistics)
            .filter(Statistics.id == id)
            .update(data, synchronize_session="fetch")
        )
        session.commit()
        session.close()
    except Exception as e:
        raise e
    return statistics


# TODO: move session creating and closing out of these individual calls
def put_text(id, data):
    try:
        session = Session()
        text = (
            session.query(Text)
            .filter(Text.id == id)
            .update(data, synchronize_session="fetch")
        )
        session.commit()
        session.close()
    except Exception as e:
        raise e
    return text


def delete_text(id):
    try:
        session = Session()

        exists = session.query(Text).filter(Text.id == id).first() is not None
        if exists:
            session.query(Text).filter(Text.id == id).delete()
            session.commit()

        session.close()
    except Exception as e:
        raise e

    return exists
