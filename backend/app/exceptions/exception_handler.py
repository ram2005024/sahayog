from fastapi import FastAPI, Request
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.responses import JSONResponse
from rich.panel import Panel
from rich.table import Table

from app.core.logger import console
from app.exceptions.custom_base_exception import AppException
from app.schemas.common import ErrorResponse


def _req_id(request: Request) -> str:
    return getattr(request.state, "request_id", "N/A")


def exception_handler_caller(app: FastAPI):

    # ── App Exception ──────────────────────────────────────────
    @app.exception_handler(AppException)
    async def custom_exception(request: Request, exc: AppException):
        rid = _req_id(request)
        console.print(
            Panel(
                f"[warning]⚠  APP EXCEPTION[/]\n\n"
                f"[bold white]Route  :[/]  {request.method} {request.url.path}\n"
                f"[bold white]Code   :[/]  [{exc.status_code}]\n"
                f"[bold white]Error  :[/]  [yellow]{exc.error_code}[/]\n"
                f"[bold white]Message:[/]  {exc.message}\n"
                f"[bold white]Req ID :[/]  [dim]{rid}[/]",
                title="[yellow]App Error[/]",
                border_style="yellow",
                expand=False,
            )
        )
        return JSONResponse(
            status_code=exc.status_code,
            content=ErrorResponse(
                error_code=exc.error_code,
                message=exc.message,
            ).model_dump(),
        )

    # ── HTTP Exception ─────────────────────────────────────────
    @app.exception_handler(HTTPException)
    async def http_error_handler(request: Request, exc: HTTPException):
        rid = _req_id(request)
        console.print(
            Panel(
                f"[warning]🌐  HTTP EXCEPTION[/]\n\n"
                f"[bold white]Route  :[/]  {request.method} {request.url.path}\n"
                f"[bold white]Code   :[/]  {exc.status_code}\n"
                f"[bold white]Detail :[/]  {exc.detail}\n"
                f"[bold white]Req ID :[/]  [dim]{rid}[/]",
                title="[yellow]HTTP Error[/]",
                border_style="yellow",
                expand=False,
            )
        )
        return JSONResponse(
            status_code=exc.status_code,
            content=ErrorResponse(
                error_code="HTTP_ERROR",
                message=exc.detail,
            ).model_dump(),
        )

    # ── Validation Exception ───────────────────────────────────
    @app.exception_handler(RequestValidationError)
    async def validation_error_handler(request: Request, exc: RequestValidationError):
        rid = _req_id(request)

        table = Table(
            "Field",
            "Message",
            "Type",
            style="yellow",
            header_style="bold yellow",
            border_style="dim yellow",
            show_lines=True,
        )
        formatted = []
        for err in exc.errors():
            field = ".".join(str(l) for l in err.get("loc", []))
            message = err.get("msg", "")
            etype = err.get("type", "")
            table.add_row(field, message, etype)
            formatted.append({"field": field, "message": message, "type": etype})

        console.print(
            Panel(
                f"[warning]📋  VALIDATION ERROR[/]\n\n"
                f"[bold white]Route  :[/]  {request.method} {request.url.path}\n"
                f"[bold white]Req ID :[/]  [dim]{rid}[/]\n",
                title="[yellow]Validation Error[/]",
                border_style="yellow",
                expand=False,
            )
        )
        console.print(table)

        return JSONResponse(
            status_code=422,
            content=ErrorResponse(
                error_code="VALIDATION_ERROR",
                message="Request validation failed",
                details=formatted,
            ).model_dump(),
        )

    # ── Global / Unhandled Exception ───────────────────────────
    @app.exception_handler(Exception)
    async def global_error_handler(request: Request, exc: Exception):
        rid = _req_id(request)
        console.print(
            Panel(
                f"[critical] 💥 UNHANDLED EXCEPTION [/]\n\n"
                f"[bold white]Route  :[/]  {request.method} {request.url.path}\n"
                f"[bold white]Type   :[/]  [red]{type(exc).__name__}[/]\n"
                f"[bold white]Req ID :[/]  [dim]{rid}[/]",
                title="[red]Server Error[/]",
                border_style="red",
                expand=False,
            )
        )
        console.print_exception(show_locals=True)
        return JSONResponse(
            status_code=500,
            content=ErrorResponse(
                error_code="SERVER_ERROR",
                message="Something went wrong on the server",
            ).model_dump(),
        )
