from pywebio import input, output
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


def display_textarea(value="") -> str:
    mode = Mode()
    source_sql = input.textarea(
        rows=20,
        code={"mode": "sql", "indentUnit": 4},
        value=value
    )
    formatted = format_string(source=source_sql, mode=mode)
    return formatted

def main(value="") -> None:
    output.put_markdown(greeting(), lstrip=True)
    formatted = value
    while True:
        with output.use_scope('playground', clear=True):
            formatted = display_textarea(value=formatted)
            output.put_code(formatted, language="sql")


if __name__ == "__main__":
    main()
