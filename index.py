from pywebio import output, pin, start_server
from sqlfmt.api import format_string
from sqlfmt.mode import Mode
import os

def greeting() -> str:

    greeting = [
        "# sqlfmt: The Opinionated SQL Formatter",
        "sqlfmt enforces a single style in SQL, similar to black for Python.",
        "## Getting Started with sqlfmt",
        (
            "If you want to use the sqlfmt cli, visit the [Github Repo]"
            "(https://github.com/tconbeer/sqlfmt) for more information, "
            "or `pipx install shandy-sqlfmt`"
        ),
        "## Or you can try it out here",
        (
            "Type or paste SQL into the box below, then click the button to "
            "see your code beautifully formatted"
        ),
    ]

    return "\n".join(greeting)


def update_textarea() -> None:
    mode = Mode()
    source_sql = pin.pin["source_sql"]
    formatted = format_string(source=source_sql, mode=mode)
    pin.pin_update("source_sql", value=formatted)
    return formatted


def main(value="") -> None:
    output.put_markdown(greeting(), lstrip=True)
    pin.put_textarea(
        "source_sql", rows=20, code={"mode": "sql", "indentUnit": 4}, value=value
    )
    output.put_button(
        label="sqlfmt!",
        onclick=update_textarea,
        color="primary",
    )


if __name__ == "__main__":
    port = os.environ.get('PORT', 8080)
    start_server(main, port=port, websocket_ping_interval=30)
