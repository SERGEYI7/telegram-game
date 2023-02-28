import json
import typing

from aiohttp.web_exceptions import (
    HTTPException,
    HTTPUnprocessableEntity,
    HTTPForbidden,
    HTTPNotImplemented,
    HTTPConflict,
    HTTPNotFound,
    HTTPBadRequest,
)
from aiohttp.web_middlewares import middleware
from aiohttp_apispec import validation_middleware
from aiohttp_session import get_session

from app.admin.models import Admin
from app.web.utils import error_json_response

if typing.TYPE_CHECKING:
    from app.web.app import Application, Request


@middleware
async def auth_middleware(request: "Request", handler: callable):
    session = await get_session(request)
    if session:
        request.admin = Admin.from_session(session)
    return await handler(request)


# @middleware


HTTP_ERROR_CODES = {
    400: "bad_request",
    401: "unauthorized",
    403: "forbidden",
    404: "not_found",
    405: "not_implemented",
    409: "conflict",
    500: "internal_server_error",
}


def data_error(error):
    status, text = error.text.split(":")
    return {status: text}


@middleware
async def error_handling_middleware(request: "Request", handler):
    try:
        response = await handler(request)
        return response
    except HTTPUnprocessableEntity as e:
        # print(data_error(e))
        return error_json_response(
            http_status=400,
            status="bad_request",
            message=e.reason,
            data=json.loads(e.text),
        )
    except HTTPForbidden as e:
        return error_json_response(
            http_status=403,
            status="forbidden",
            message=e.reason,
            data=data_error(e),
        )
    except HTTPNotFound as e:
        return error_json_response(
            http_status=404,
            status="not_found",
            message=e.reason,
            data=data_error(e),
        )
    except HTTPNotImplemented as e:
        return error_json_response(
            http_status=405,
            status="not_implemented",
            message=e.reason,
            data=data_error(e),
        )
    except HTTPConflict as e:
        return error_json_response(
            http_status=409,
            status="conflict",
            message=e.reason,
            data=data_error(e),
        )
    except HTTPException as e:
        return error_json_response(
            http_status=e.status,
            status=HTTP_ERROR_CODES[e.status],
            message=str(e),
        )
    except Exception as e:
        request.app.logger.error("Exception", exc_info=e)
        return error_json_response(
            http_status=500, status="internal server error", message=str(e)
        )


def setup_middlewares(app: "Application"):
    app.middlewares.append(auth_middleware)
    app.middlewares.append(error_handling_middleware)
    app.middlewares.append(validation_middleware)
