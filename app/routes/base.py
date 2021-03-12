from typing import Any

import tornado.httputil as httputil
import tornado.web
from models import get_session, return_session


class BaseAPIHandler(tornado.web.RequestHandler):
    """
    Base handler for all api/* routes
    """

    def prepare(self):
        self.session = get_session()

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
        return_session(self.session)


class BaseAdminAPIHandler(BaseAPIHandler):
    """
    Base handler for all api/admin/* routes
    """


#     Add AUTH stuff here


class BaseUserAPIHandler(BaseAPIHandler):
    """
    Base handler for all api/user/* routes
    """


class NotFoundHandler(BaseAPIHandler):
    """
    Base handler for all invalid routes
    """

    async def prepare(self):
        self.write_error(status_code=404, message="Invalid Path")
