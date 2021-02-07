import asyncio

import tornado.httpserver
import tornado.ioloop
import tornado.web
from config import config
from routes.sample import SampleHandler, SampleHandler2
from tornado.platform.asyncio import AsyncIOMainLoop


def get_routes():
    routes = [
        (r"/", SampleHandler),
        (r"/sample", SampleHandler2),
    ]
    return routes


def make_app():
    app = tornado.web.Application(
        get_routes(),
        debug=config.get("tornado.debug"),
        xsrf_cookies=config.get("tornado.xsrf"),
    )
    return app


def main():
    if "dev" in config.get("app-env"):
        # Print out config for dev environments
        print("tornado port:", config.get("tornado.port"))
        print("tornado debug:", config.get("tornado.debug"))
        print("postgres hostname:", config.get("postgres.hostname"))
        print("postgres database:", config.get("postgres.database"))
        print("postgres user:", config.get("postgres.user"))

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
