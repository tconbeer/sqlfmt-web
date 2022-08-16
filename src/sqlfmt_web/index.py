import os

from pywebio import config, output, pin, start_server
from sqlfmt.api import format_string
from sqlfmt.exception import SqlfmtError
from sqlfmt.mode import Mode
from sqlfmt_web.example import EXAMPLE
from sqlfmt_web.greeting import GREETING
from sqlfmt_web.script import SCRIPT


def details_template() -> str:
    tpl = """
    <details>
        <summary style="background-color: #ffffff">{{title}}</summary>
        {{#contents}}
            {{& pywebio_output_parse}}
        {{/contents}}
    </details>
    """
    return tpl


def load_example() -> None:
    pin.pin_update("source_sql", value=EXAMPLE)


def format_textarea() -> None:
    kwargs = {
        "line_length": pin.pin["line_length"],
        "no_jinjafmt": False if "jinjafmt" in pin.pin["flags"] else True,
    }
    mode = Mode(**kwargs)
    source_sql = pin.pin["source_sql"]
    try:
        formatted: str = format_string(source_string=source_sql, mode=mode)
    except SqlfmtError as e:
        output.toast(
            content=str(e),
            color="error",
            duration=2,
        )
    else:
        pin.pin_update("source_sql", value=formatted)
        if source_sql != formatted:
            output.toast(
                content="Success! Formatting applied",
                color="success",
                duration=1,
            )
        else:
            output.toast(
                content="SQL already formatted",
                color="info",
                duration=1,
            )


def index() -> None:
    output.put_markdown(GREETING, lstrip=True)
    output.put_button(
        label="Load example query", onclick=load_example, small=True, link_style=True
    )

    pin.put_textarea("source_sql", rows=20, code={"mode": "sql", "indentUnit": 4})
    output.put_row(
        [
            output.put_button(
                label="sqlfmt!",
                onclick=format_textarea,
                color="primary",
            ),
            output.put_widget(
                details_template(),
                {
                    "title": "Configure Formatting",
                    "contents": [
                        pin.put_slider(
                            "line_length",
                            label="Maximum line length",
                            value=88,
                            min_value=40,
                            max_value=140,
                            step=1,
                        ),
                        pin.put_checkbox(
                            "flags",
                            options=[
                                {
                                    "label": "Format jinja tags",
                                    "value": "jinjafmt",
                                    "selected": True,
                                }
                            ],
                        ),
                    ],
                },
            ),
        ],
        size="25% 75%",
    )


def serve_index() -> None:
    config(
        title="sqlfmt: The autoformatter for dbt SQL",
        description=(
            "sqlfmt formats your dbt SQL files so you don't have to. "
            "It is similar in nature to black, gofmt, and rustfmt."
        ),
        css_style="footer {display: none;}",
        js_code=SCRIPT,
    )
    port = os.environ.get("PORT", 5000)
    start_server(index, port=port, websocket_ping_interval=30)


if __name__ == "__main__":
    serve_index()
