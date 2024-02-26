import logging
import socket
import uuid
from contextvars import ContextVar

from fastapi import Request, Response
from pydantic import BaseModel, Field
from starlette.middleware.base import BaseHTTPMiddleware

local = ContextVar("LogInfo")


class EndpointFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        return record.args and len(record.args) >= 3 and record.args[2] != "/ping"


class LogInfo(BaseModel):
    hostname: str = Field(description="Host name")
    dest_ip: str = Field(description="The server IP")
    caller: str = Field(description="caller id")
    source_ip: str = Field(description="client IP")
    uow: str = Field(description="Unit of Work ID")
    request_id: str = Field(description="Request ID")


class LoggingFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        log_info: LogInfo = local.get()
        record.hostname = log_info.hostname
        record.dest_ip = log_info.dest_ip
        record.caller = log_info.caller
        record.source_ip = log_info.source_ip
        record.uow = log_info.uow
        record.request_id = log_info.request_id
        return True


class LoggingMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        self.__process_request(request)

        # process the request and get the response
        response = await call_next(request)

        # Code to be executed for each request/response after
        # the view is called.
        self.__process_response(request, response)

        return response

    def __process_request(self, request: Request):
        try:
            x_forwarded_for = request.headers.get("HTTP_X_FORWARDED_FOR", "")
            if x_forwarded_for:
                source_ip = x_forwarded_for.split(",")[0]  # So this is real ip
            else:
                source_ip = request.headers.get("REMOTE_ADDR")  # Get an agent here ip

            hook_id = request.get("hook_id", "")
            store_id = request.get("store_id", "")
            order_id = request.get("order_id", "")
            client_id = request.headers.get("x-clicoh-client-id")
            caller = f" hook={hook_id} " if hook_id else ""
            caller += f" store={store_id} " if hook_id else ""
            caller += f" order={order_id} " if hook_id else ""
            caller += f" client={client_id} " if client_id else ""
            host_name = socket.gethostname()
            log_info = LogInfo(
                hostname=host_name,
                dest_ip=socket.gethostbyname(host_name),
                caller=caller or "Anonymous",
                source_ip=source_ip or "noip",
                uow=request.headers.get("X-UOW", str(uuid.uuid4())),
                request_id=str(uuid.uuid4()),
            )

            local.set(log_info)
        except Exception as e:
            print(e)

    def __process_response(self, request: Request, response: Response):
        try:
            log_info: LogInfo = local.get()
            response.headers["X-UOW"] = log_info.uow
        except Exception as e:
            print(e)

FORMAT = "[%(asctime)s] [%(hostname)s] [%(source_ip)s] [%(caller)s] [%(uow)s] [%(request_id)s] " \
         "[%(levelname)s] [%(module)s:%(lineno)d] %(message)s"

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,  # Whether to disable the existing logger
    "formatters": {  # The format of log information display
        "clicOH": {"format": FORMAT}
    },
    "filters": {
        "new_add": {
            "()": "settings.config_logging.LoggingFilter",
        },
    },
    "handlers": {  # Log processing method
        "console": {  # Output logs to the terminal
            "level": "INFO",
            "filters": ["new_add"],
            "class": "logging.StreamHandler",
            "formatter": "clicOH",
        },
    },
    "loggers": {
        "": {  # Defines a default logger
            "handlers": ["console"],  # It can output log to terminal and file at the same time
            "level": "INFO",  # The lowest log level that the logger receives
            "propagate": False,  # Whether to inherit the log Information ,0: no 1: yes
        },
    },
}
