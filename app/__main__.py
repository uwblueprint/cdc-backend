import asyncio

import tornado.httpserver
import tornado.ioloop
import tornado.web
from config import config
from routes.admin.asset import AdminAssetHandler, AdminAssetPostHandler
from routes.admin.scenario import AdminScenarioHandler, AdminScenarioPostHandler
from routes.base import NotFoundHandler
from routes.user.asset import UserAssetHandler
from routes.user.loading_screen import UserLoadingScreen
from routes.user.scenario import UserScenarioHandler
from routes.user.scene import UserSceneHandler
from routes.user.solved import UserSolvedHandler
from routes.user.text import UserTextHandler
from tornado.platform.asyncio import AsyncIOMainLoop


def get_routes():
    routes = [
        (r"/api/user/v1/text/([0-9]{1,16})", UserTextHandler),
        (r"/api/user/v1/solved/([0-9]{1,16})", UserSolvedHandler),
        (r"/api/user/v1/asset/([0-9]{1,16})", UserAssetHandler),
        (r"/api/user/v1/scene/([0-9]{1,16})", UserSceneHandler),
        (r"/api/user/v1/scenario/([0-9]{1,16})", UserScenarioHandler),
        (r"/api/user/v1/loading_screen", UserLoadingScreen),
        (r"/api/admin/v1/asset", AdminAssetPostHandler),
        (r"/api/admin/v1/asset/([0-9]{1,16})", AdminAssetHandler),
        (r"/api/admin/v1/scenario", AdminScenarioPostHandler),
        (r"/api/admin/v1/scenario/([0-9]{1,16})", AdminScenarioHandler),
    ]
    return routes


def make_app():
    app = tornado.web.Application(
        get_routes(),
        debug=config.get("tornado.debug"),
        xsrf_cookies=config.get("tornado.xsrf"),
        default_handler_class=NotFoundHandler,
    )
    return app


def main():
    if "dev" in config.get("app-env"):
        # Print out config for dev environments
        print(" --------------------- SERVER SETTINGS ---------------------")
        print("tornado port:", config.get("tornado.port"))
        print("tornado debug:", config.get("tornado.debug"))
        print("postgres hostname:", config.get("postgres.hostname"))
        print("postgres database:", config.get("postgres.database"))
        print("postgres user:", config.get("postgres.user"))
        print(" --------------------- SERVER STARTED ---------------------")

    app = make_app()
    server = tornado.httpserver.HTTPServer(app)

    port = config.get("tornado.port")
    if port:
        server.bind(port, address=config.get("tornado.address"))

    server.start()
    asyncio.get_event_loop().run_forever()


if __name__ == "__main__":
    AsyncIOMainLoop().install()
    main()
