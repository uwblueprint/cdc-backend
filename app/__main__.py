import asyncio
import os
import ssl
import uuid

import firebase_admin
import tornado.autoreload
import tornado.httpserver
import tornado.ioloop
import tornado.web
from cache.update_cache import update_cache
from config import config
from firebase_admin import credentials
from routes.admin.asset import (
    AdminAssetHandler,
    AdminAssetPostHandler,
    AdminAssetScreenshotHandler,
    AdminAssetsHandler,
)
from routes.admin.aws import AdminJigsawHelper, AdminUploadHandler
from routes.admin.object import (
    AdminObjectPostHandler,
    AdminObjectPutHandler,
    AdminPuzzleHandler,
)
from routes.admin.scenario import (
    AdminScenarioDuplicateHandler,
    AdminScenarioHandler,
    AdminScenarioPostHandler,
    AdminScenariosHandler,
)
from routes.admin.scene import (
    AdminSceneDuplicateHandler,
    AdminSceneHandler,
    AdminScenePostHandler,
    AdminSceneScreenshotHandler,
    AdminScenesHandler,
)
from routes.base import (
    BaseAuthHandler,
    BaseLogoutHandler,
    BaseProfileHandler,
    LandingPageUIHandler,
    NotFoundHandler,
    NotFoundUIHandler,
    UIStaticHandler,
)
from routes.ui.admin_scene import UIAdminSceneHandler
from routes.ui.completed_page import UIScenarioCompletedPageHandler
from routes.ui.landing_page import UIScenarioLandingPageHandler
from routes.ui.scenario import UIScenarioHandler
from routes.ui.tutorial import UITutorialPageHandler

# from routes.user.asset import UserAssetHandler
# from routes.user.loading_screen import UserLoadingScreen
# from routes.user.scenario import UserScenarioHandler
# from routes.user.scene import UserSceneHandler
# from routes.user.solved import UserSolvedHandler
from tornado.platform.asyncio import AsyncIOMainLoop


def get_routes():
    routes = [
        # (
        #     r"/api/user/v1/solved/([0-9]{1,16})",
        #     UserSolvedHandler,
        # ),
        # (r"/api/user/v1/asset/([0-9]{1,16})", UserAssetHandler),
        # (r"/api/user/v1/scene/([0-9]{1,16})", UserSceneHandler),
        # (r"/api/user/v1/scenario/([0-9]{1,16})", UserScenarioHandler),
        # (r"/api/user/v1/loading_screen", UserLoadingScreen),
        (r"/api/admin/v1/upload", AdminUploadHandler),
        (r"/api/admin/v1/jigsaw", AdminJigsawHelper),
        (r"/api/admin/v1/asset", AdminAssetPostHandler),
        (r"/api/admin/v1/asset/([0-9]{1,16})", AdminAssetHandler),
        (r"/api/admin/v1/assets", AdminAssetsHandler),
        (r"/api/admin/v1/asset/([0-9]{1,16})/screenshot", AdminAssetScreenshotHandler),
        (r"/api/admin/v1/scenario", AdminScenarioPostHandler),
        (r"/api/admin/v1/scenario/([0-9]{1,16})", AdminScenarioHandler),
        (
            r"/api/admin/v1/scenario/([0-9]{1,16})/duplicate",
            AdminScenarioDuplicateHandler,
        ),
        (r"/api/admin/v1/scenarios", AdminScenariosHandler),
        (r"/api/admin/v1/scene", AdminScenePostHandler),
        (r"/api/admin/v1/scenes", AdminScenesHandler),
        (r"/api/admin/v1/scene/([0-9]{1,16})", AdminSceneHandler),
        (r"/api/admin/v1/scene/([0-9]{1,16})/object", AdminObjectPostHandler),
        (
            r"/api/admin/v1/scene/([0-9]{1,16})/object/([0-9]{1,16})",
            AdminObjectPutHandler,
        ),
        (
            r"/api/admin/v1/scene/([0-9]{1,16})/object/([0-9]{1,16})/puzzle",
            AdminPuzzleHandler,
        ),
        (r"/api/admin/v1/scene/([0-9]{1,16})/duplicate", AdminSceneDuplicateHandler),
        (r"/api/admin/v1/scene/([0-9]{1,16})/screenshot", AdminSceneScreenshotHandler),
        (
            r"/static/(.*)",
            UIStaticHandler,
            dict(path=f"{os.path.dirname(__file__)}/public/static/"),
        ),
        (r"/admin/scene/([0-9]{1,16})", UIAdminSceneHandler),
        (r"/admin_login", BaseAuthHandler),
        (r"/api/admin/v1/admin_logout", BaseLogoutHandler),
        (r"/api/admin/v1/user_profile", BaseProfileHandler),
        # if no match before this, match all /api/* routes with a 404 error
        (r"/api/\S*", NotFoundHandler),
        (r"/([a-zA-Z_-]{1,50})/?", UIScenarioLandingPageHandler),
        (r"/([a-zA-Z_-]{1,50})/tutorial", UITutorialPageHandler),
        (r"/([a-zA-Z_-]{1,50})/([0-9]{0,16})", UIScenarioHandler),
        (r"/([a-zA-Z_-]{1,50})/completed", UIScenarioCompletedPageHandler),
        (r"/?", LandingPageUIHandler),
    ]
    return routes


def make_app():
    app = tornado.web.Application(
        get_routes(),
        debug=config.get("tornado.debug"),
        xsrf_cookies=config.get("tornado.xsrf"),
        default_handler_class=NotFoundUIHandler,
        template_path=f"{os.path.dirname(__file__)}/public/templates",
        cookie_secret=uuid.uuid4().hex,
    )
    return app


def init_firebase():
    cred_path = credentials.Certificate(
        f"{os.path.dirname(__file__)}/../secrets/service_account_key.json"
    )
    firebase_admin.initialize_app(cred_path)


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

        # Autoreload server for HTML file changes
        for directory, _, files in os.walk("public"):
            [
                tornado.autoreload.watch(directory + "/" + f)
                for f in files
                if not f.startswith(".")
            ]

    app = make_app()
    init_firebase()

    port = config.get("tornado.port")
    if port == 443:
        ssl_ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        ssl_ctx.load_cert_chain(
            f"{os.path.dirname(__file__)}/../secrets/domain.crt",
            f"{os.path.dirname(__file__)}/../secrets/domain.key",
        )
        server = tornado.httpserver.HTTPServer(
            app,
            ssl_options=ssl_ctx,
        )
        server.bind(port, address=config.get("tornado.address"))
    else:
        server = tornado.httpserver.HTTPServer(app)
        server.bind(port, address=config.get("tornado.address"))

    server.start()

    cache_update_time = config.get("cache.update_time") * 1000
    cache_periodic_callback_enabled = config.get("cache.periodic_callback_enabled")
    if cache_periodic_callback_enabled:
        tornado.ioloop.PeriodicCallback(update_cache, cache_update_time).start()
    asyncio.get_event_loop().run_forever()


if __name__ == "__main__":
    AsyncIOMainLoop().install()
    main()
