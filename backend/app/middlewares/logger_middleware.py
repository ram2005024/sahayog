import time
import uuid

from fastapi import Request
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.logger import console

METHOD_COLORS = {
    "GET": "bold bright_green",
    "POST": "bold bright_blue",
    "PUT": "bold bright_yellow",
    "PATCH": "bold bright_cyan",
    "DELETE": "bold bright_red",
}


def method_badge(method: str) -> str:
    color = METHOD_COLORS.get(method, "white")
    return f"[{color}] {method} [/]"


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid.uuid4())[:8].upper()
        start = time.perf_counter()

        request.state.request_id = request_id

        # ── Incoming ──────────────────────────────────────────
        incoming = Text()
        incoming.append("  ⬆  INCOMING  ", style="bold white on dark_blue")
        incoming.append(
            f"  {request.method}  ", style=METHOD_COLORS.get(request.method, "white")
        )
        incoming.append(f"{request.url.path}  ", style="bold white")
        incoming.append(f"id: {request_id}", style="dim cyan")

        console.print()
        console.rule(style="dim blue")
        console.print(incoming)

        try:
            response = await call_next(request)
        except Exception:
            console.print(
                Panel(
                    f"[critical] 💥 CRASH [/]  [bold white]{request.method} "
                    f"{request.url.path}[/]  [dim]id: {request_id}[/]",
                    border_style="red",
                    expand=False,
                )
            )
            console.print_exception(show_locals=True)
            raise

        duration = (time.perf_counter() - start) * 1000
        status = response.status_code

        if status >= 500:
            status_style = "bold white on red"
            icon = "🔴"
            rule_style = "red"
        elif status >= 400:
            status_style = "bold black on yellow"
            icon = "🟡"
            rule_style = "yellow"
        else:
            status_style = "bold black on green"
            icon = "🟢"
            rule_style = "green"

        # ── Summary table ─────────────────────────────────────
        table = Table.grid(padding=(0, 2))
        table.add_column(no_wrap=True)
        table.add_column(no_wrap=True)
        table.add_column(no_wrap=True)
        table.add_column(no_wrap=True)
        table.add_column(no_wrap=True)

        table.add_row(
            f" {icon} ",
            f"[{METHOD_COLORS.get(request.method, 'white')}] {request.method} [/]",
            f"[bold white]{request.url.path}[/]",
            f"[{status_style}]  {status}  [/]",
            f"[dim]{duration:.1f} ms  ·  id: {request_id}[/]",
        )

        console.print(table)
        console.rule(style=rule_style)
        console.print()

        response.headers["X-Request-ID"] = request_id
        return response
