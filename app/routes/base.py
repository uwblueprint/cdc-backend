from typing import Any

import tornado.httputil as httputil
import tornado.web
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
