import datetime
import time
from typing import Any

import firebase_admin.auth as auth
import tornado.escape
import tornado.httputil as httputil
import tornado.web
from config import config
from models import get_session, return_session


class BaseAPIHandler(tornado.web.RequestHandler):
    """
    Base handler for all api/* routes
    """

    def prepare(self):
        self.db_session = None

    def set_default_headers(self) -> None:
        self.set_header("Content-Type", "application/json")

    def write_error(self, status_code: int, **kwargs: Any) -> None:
        self.set_header("Content-Type", "application/problem+json")
        title = httputil.responses.get(status_code, "Unknown")
        message = kwargs.get("message", self._reason)
        self.set_status(status_code)
        response_error = {"status": status_code, "title": title, "message": message}
        self.finish(response_error)

    def on_finish(self):
        if self.db_session:
            return_session(self.db_session)


class BaseAdminAPIHandler(BaseAPIHandler):
    """
    Base handler for all api/admin/* routes
    """

    def prepare(self):
        # TODO: check auth cookie before creating session

        # Admins always get a brand new session
        self.db_session = get_session()


class BaseUserAPIHandler(BaseAPIHandler):
    """
    Base handler for all api/user/* routes
    """


class NotFoundHandler(tornado.web.RequestHandler):
    """
    Base handler for all invalid routes
    """

    async def prepare(self):
        self.set_header("Content-Type", "application/problem+json")
        title = "Not Found"
        message = "Invalid Path"
        status_code = 404
        self.set_status(status_code)
        response_error = {"status": status_code, "title": title, "message": message}
        await self.finish(response_error)


class BaseUIHandler(tornado.web.RequestHandler):
    """
    Base handler for all UI routes
    """

    def prepare(self):
        self.db_session = None

    def write_error(self, status_code: int, **kwargs: Any) -> None:
        title = httputil.responses.get(status_code, "Unknown")
        message = kwargs.get("message", self._reason)
        self.render("error.html", error_title=title, error_message=message)

    def on_finish(self):
        if self.db_session:
            return_session(self.db_session)


class UIStaticHandler(tornado.web.StaticFileHandler):
    """
    Base handler for /public/static/*
    """

    def write_error(self, status_code, *args, **kwargs):
        title = httputil.responses.get(status_code, "Unknown")
        message = kwargs.get("message", self._reason)
        self.render("error.html", error_title=title, error_message=message)


class BaseAuthHandler(tornado.web.RequestHandler):
    """
    Base handler for login
    """

    def set_default_headers(self) -> None:
        self.set_header("Content-Type", "application/json")

    async def post(self):
        try:
            data = tornado.escape.json_decode(self.request.body)
            id_token = data["idToken"]
            decoded_claims = auth.verify_id_token(id_token)
            # Only process if the user signed in within the last 5 minutes.
            if time.time() - decoded_claims["auth_time"] < 5 * 60:
                expires_in = datetime.timedelta(days=config.get("auth.expiry_days"))
                session_cookie = auth.create_session_cookie(
                    id_token, expires_in=expires_in
                )
                response = {"status": 200, "message": "success"}
                cookie_name = config.get("auth.cookie_name")
                self.set_secure_cookie(
                    cookie_name,
                    session_cookie,
                    expires_days=config.get("auth.expiry_days"),
                    httponly=True,
                )
                await self.finish(response)
        except Exception:
            # Don't give any reason as this is a sensitive route
            self.set_header("Content-Type", "application/problem+json")
            message = "Forbidden"
            self.set_status(403)
            response_error = {"status": 403, "message": message}
            await self.finish(response_error)
