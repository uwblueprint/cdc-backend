import datetime
import logging
import time
from typing import Any

import firebase_admin.auth as auth
import tornado.escape
import tornado.httputil as httputil
import tornado.web
from cache.cache import get_all_cached_scenarios
from config import config
from models import get_session, return_session

logger = logging.getLogger("houdini")


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
        self.remote_ip = self.request.headers.get("X-Real-IP", self.request.remote_ip)

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
    Base handler for all invalid routes that are served on the api: /api/*
    """

    async def prepare(self):
        self.set_header("Content-Type", "application/problem+json")
        title = "Not Found"
        message = "Invalid Path"
        status_code = 404
        self.set_status(status_code)
        response_error = {"status": status_code, "title": title, "message": message}
        await self.finish(response_error)


class NotFoundUIHandler(tornado.web.RequestHandler):
    """
    Base handler for all invalid routes that are served on the UI
    """

    async def prepare(self):
        title = "Not Found"
        self.set_status(404)
        await self.render("error_404.html", error_title=title)


class BaseUIHandler(tornado.web.RequestHandler):
    """
    Base handler for all UI routes
    """

    def prepare(self):
        self.db_session = None
        self.remote_ip = self.request.headers.get("X-Real-IP", self.request.remote_ip)

    def write_error(self, status_code: int, **kwargs: Any) -> None:
        title = httputil.responses.get(status_code, "Unknown")
        message = kwargs.get("message", self._reason)
        if status_code == 404:
            self.render("error_404.html", error_title=title)
        else:
            self.render("error.html", error_title=title, error_message=message)

    def on_finish(self):
        if hasattr(self, "db_session") and self.db_session:
            return_session(self.db_session)


class BaseAdminUIHandler(BaseUIHandler):
    def prepare(self):
        # Auth check: you shall not pass
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
            logger.warning(
                {"message": "error logging in", "error": str(e), "ip": self.remote_ip}
            )
            return self.write_error(status_code=403, message=str(e))
        except Exception:
            # Session cookie is invalid, expired or revoked. Force user to login.
            logger.warning({"message": "error logging in", "ip": self.remote_ip})
            return self.write_error(status_code=403, message="Forbidden")


class UIStaticHandler(tornado.web.StaticFileHandler):
    """
    Base handler for /public/static/*
    """

    def write_error(self, status_code, *args, **kwargs):
        title = httputil.responses.get(status_code, "Unknown")
        message = kwargs.get("message", self._reason)
        self.render("error_404.html", error_title=title, error_message=message)


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
        remote_ip = self.request.headers.get("X-Real-IP", self.request.remote_ip)
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
                set_secure = False
                domain = None
                if "https" in config.get("frontend_domain"):
                    set_secure = True
                    domain = config.get("frontend_domain")
                    domain = domain.lstrip(domain.split(".")[0])
                self.set_secure_cookie(
                    cookie_name,
                    session_cookie,
                    httponly=True,
                    samesite="Strict",
                    secure=set_secure,
                    domain=domain,
                )
                self.set_cookie(
                    "_xsrf",
                    self.xsrf_token,
                    samesite="Strict",
                    secure=set_secure,
                    domain=domain,
                )
                logger.info(
                    {
                        "message": "admin logged in successfully",
                        "user": self.user,
                        "ip": remote_ip,
                    }
                )
                await self.finish(resp_json)
            else:
                raise ValueError("User signed in too long ago")
        except ValueError as e:
            self.set_header("Content-Type", "application/problem+json")
            self.set_status(403)
            response_error = {"status": 403, "message": str(e)}
            logger.warning(
                {
                    "message": "error logging in",
                    "route": "admin_login",
                    "error": str(e),
                    "ip": remote_ip,
                }
            )
            await self.finish(response_error)
        except Exception:
            # Don't give any reason as this is a sensitive route
            self.set_header("Content-Type", "application/problem+json")
            message = "Forbidden"
            self.set_status(403)
            response_error = {"status": 403, "message": message}
            logger.warning(
                {"message": "error logging in", "route": "admin_login", "ip": remote_ip}
            )
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
        logger.info(
            {
                "message": "admin logged out successfully",
                "user": self.user,
                "ip": self.remote_ip,
            }
        )
        await self.finish(resp_json)


class BaseProfileHandler(BaseAdminAPIHandler):
    """
    Base handler for getting an user profile
    """

    async def get(self):
        try:
            display_name = auth.get_user_by_email(self.user).display_name
        except Exception:
            display_name = ""
        resp_json = {
            "status": 200,
            "message": "success",
            "email": self.user,
            "display_name": display_name,
        }
        await self.finish(resp_json)


class LandingPageUIHandler(BaseUIHandler):
    """
    Base handler for the landing page
    """

    async def get(self):
        self.set_status(200)
        cached_scenarios = await get_all_cached_scenarios()
        res_scenarios = []
        for scenario in cached_scenarios.values():
            scenario_dict = scenario["obj_dict"]
            if scenario_dict["is_published"]:
                res_scenarios.append(
                    {
                        "title": scenario_dict["name"],
                        "link": f"/{scenario_dict['friendly_name']}",
                        "description": scenario_dict["description"],
                    }
                )
        logger.info(
            {
                "message": "Rendering all scenarios",
                "number_of_scenarios": len(res_scenarios),
                "ip": self.remote_ip,
            }
        )
        await self.render("home.html", res_scenarios=res_scenarios)
