from pywebio import input, output, pin, start_server
from sqlfmt.api import format_string
from sqlfmt.mode import Mode


def greeting() -> str:

    greeting = [
        "# Automatically format your SQL files",
        (
            "sqlfmt enforces a single style in SQL, similar to black for "
            "Python. You can install it with `pip install shandy-sqlfmt`, "
            "or try it out below "
        ),
        "## Enter SQL below",
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
        "source_sql",
        rows=20,
        code={"mode": "sql", "indentUnit": 4},
        value=value
    )
    output.put_button(
        label="sqlfmt!",
        onclick=update_textarea,
        color="primary",
    )

if __name__ == "__main__":
    start_server(main)
