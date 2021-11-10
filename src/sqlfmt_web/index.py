import os

from pywebio import config, output, pin, start_server
from sqlfmt.api import format_string
from sqlfmt.mode import Mode


def greeting() -> str:

    greeting = [
        "# sqlfmt: The Opinionated SQL Formatter",
        "sqlfmt enforces a single style in SQL, similar to black for Python.",
        "## Getting Started with sqlfmt",
        (
            "If you want to use the sqlfmt CLI, "
            "on MacOS, Linux, or Windows, "
            "visit the [Github Repo](https://github.com/tconbeer/sqlfmt) "
            "for more information, "
            "or `pipx install shandy-sqlfmt`"
        ),
        "## Or you can try it out here",
        (
            "Type or paste SQL into the box below, then click the button to "
            "see your code beautifully formatted"
        ),
    ]

    return "\n".join(greeting)


def update_textarea() -> str:
    mode = Mode()
    source_sql = pin.pin["source_sql"]
    formatted: str = format_string(source=source_sql, mode=mode)
    pin.pin_update("source_sql", value=formatted)
    return formatted


def index() -> None:
    output.put_markdown(greeting(), lstrip=True)
    pin.put_textarea("source_sql", rows=20, code={"mode": "sql", "indentUnit": 4})
    output.put_button(
        label="sqlfmt!",
        onclick=update_textarea,
        color="primary",
    )


def serve_index() -> None:
    config(
        title="sqlfmt: The Opinionated SQL Formatter",
        description=(
            "sqlfmt is an opinionated CLI tool that formats your dbt sql "
            "files. It is similar in nature to black, gofmt, and rustfmt."
        ),
    )
    port = os.environ.get("PORT", 5000)
    start_server(index, port=port, websocket_ping_interval=30)


if __name__ == "__main__":
    serve_index()
