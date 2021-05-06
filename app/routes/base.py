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
        if hasattr(self, "db_session") and self.db_session:
            return_session(self.db_session)


class BaseAdminAPIHandler(BaseAPIHandler):
    """
    Base handler for all api/admin/* routes
    """

    async def options(self, *args):
        self.set_status(204)
        await self.finish()

    def set_default_headers(self) -> None:
        self.set_header("Content-Type", "application/json")
        frontend_domain = config.get("frontend_domain")
        self.set_header("Access-Control-Allow-Origin", frontend_domain)
        self.set_header(
            "Access-Control-Allow-Headers",
            "x-requested-with, content-type, X-Xsrftoken",
        )
        self.set_header(
            "Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS"
        )
        self.set_header("Access-Control-Allow-Credentials", "true")

    def prepare(self):
        # AUTH, check to make sure the user is authenticated
        self.db_session = None
        self.user = ""

        # only need to do auth check if it is not OPTIONS
        if self.request.method != "OPTIONS":
            cookie_name = config.get("auth.cookie_name")
            session_cookie = self.get_secure_cookie(cookie_name)
            if not session_cookie:
                return self.write_error(status_code=403, message="Forbidden")

            # Verify the session cookie. In this case an additional check is added to detect
            # if the user's Firebase session was revoked, user deleted/disabled, etc.
            try:
                decoded_claims = auth.verify_session_cookie(
                    session_cookie, check_revoked=True
                )
                # save the user (for audit purposes, we can use this later)
                self.user = decoded_claims["email"]
                self.sub = decoded_claims["sub"]
                # Ensure that the email is verified, so not anyone can make fake accounts
                if not decoded_claims["email_verified"]:
                    raise ValueError(
                        "The email address is not verified. Please verify it first!"
                    )
                # if not user or not valid domain email, let's not provide description of error
                if self.user.split("@")[-1] not in config.get("auth.allowed_domains"):
                    raise Exception
            except ValueError as e:
                return self.write_error(status_code=403, message=str(e))
            except Exception:
                # Session cookie is invalid, expired or revoked. Force user to login.
                return self.write_error(status_code=403, message="Forbidden")

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
        frontend_domain = config.get("frontend_domain")
        self.set_header("Access-Control-Allow-Origin", frontend_domain)
        self.set_header(
            "Access-Control-Allow-Headers", "x-requested-with, content-type"
        )
        self.set_header("Access-Control-Expose-Headers", "set-cookie")
        self.set_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.set_header("Access-Control-Allow-Credentials", "true")

    async def options(self):
        self.set_status(204)
        await self.finish()

    def check_xsrf_cookie(self) -> None:
        # XSRF cookie won't be on this request, as it would be set on this request
        # All other handlers other than this will check it by default (Tornado does that)
        pass

    async def post(self):
        try:
            data = tornado.escape.json_decode(self.request.body)
            id_token = data["idToken"]
            decoded_claims = auth.verify_id_token(id_token)
            # save the user (for audit purposes, we can use this later)
            self.user = decoded_claims["email"]
            # Ensure that the email is verified, so not anyone can make fake accounts
            if not decoded_claims["email_verified"]:
                raise ValueError(
                    "The email address is not verified. Please verify it first!"
                )
            # if not user or not valid domain email, let's not provide description of error
            if self.user.split("@")[-1] not in config.get("auth.allowed_domains"):
                raise ValueError("The domain is not allowed")
            # Only process if the user signed in within the last X min based on config.
            if (
                time.time() - decoded_claims["auth_time"]
                < config.get("auth.min_since_login") * 60
            ):
                expiry_hours = config.get("auth.expiry_hours")
                expires_in = datetime.timedelta(hours=expiry_hours)
                session_cookie = auth.create_session_cookie(
                    id_token, expires_in=expires_in
                )
                resp_json = {"status": 200, "message": "success"}
                cookie_name = config.get("auth.cookie_name")
                self.set_secure_cookie(
                    cookie_name,
                    session_cookie,
                    httponly=True,
                    samesite=None,
                    secure=True,
                )
                self.set_cookie(
                    "_xsrf",
                    self.xsrf_token,
                )
                await self.finish(resp_json)
            else:
                raise ValueError("User signed in too long ago")
        except ValueError as e:
            self.set_header("Content-Type", "application/problem+json")
            self.set_status(403)
            response_error = {"status": 403, "message": str(e)}
            await self.finish(response_error)
        except Exception:
            # Don't give any reason as this is a sensitive route
            self.set_header("Content-Type", "application/problem+json")
            message = "Forbidden"
            self.set_status(403)
            response_error = {"status": 403, "message": message}
            await self.finish(response_error)


class BaseLogoutHandler(BaseAdminAPIHandler):
    """
    Base handler for logout
    """

    async def get(self):
        cookie_name = config.get("auth.cookie_name")
        cookies_to_clear = [cookie_name, "_xsrf"]
        for cookie in cookies_to_clear:
            self.clear_cookie(cookie)

        # revoke firebase refresh token
        auth.revoke_refresh_tokens(self.sub)

        resp_json = {"status": 200, "message": "success"}
        await self.finish(resp_json)
