import asyncio

import tornado.httpserver
import tornado.ioloop
import tornado.web
from config import config
from routes.admin.asset import AdminAssetPostHandler
from routes.base import NotFoundHandler
from routes.user.solved import UserSolvedHandler
from routes.user.text import UserTextHandler
from tornado.platform.asyncio import AsyncIOMainLoop


def get_routes():
    routes = [
        (r"/api/user/v1/text/([0-9]{1,16})", UserTextHandler),
        (r"/api/user/v1/solved/([0-9]{1,16})", UserSolvedHandler),
        (r"/api/admin/v1/asset", AdminAssetPostHandler),
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
