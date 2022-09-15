import os

from pywebio import config, output, pin, start_server
from sqlfmt.api import Mode, format_string
from sqlfmt.exception import SqlfmtError
from sqlfmt_web.assets import load_asset


def load_example() -> None:
    pin.pin_update("source_sql", value=load_asset("example.sql"))


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
    body_style = (
        "max-width: 880px; display: block; "
        "margin-left: auto; margin-right: auto; "
        "padding-left: 15px; padding-right: 15px;"
    )
    output.put_html(load_asset("nav.html"))
    output.put_markdown(load_asset("greeting.md"), lstrip=True).style(body_style)
    output.put_button(
        label="Load example unformatted query",
        onclick=load_example,
        small=True,
        link_style=True,
    ).style(body_style)

    pin.put_textarea(
        "source_sql",
        rows=20,
        code={"mode": "sql", "indentUnit": 4, "theme": "base16-dark"},
    ).style(body_style)
    output.put_row(
        [
            output.put_button(
                label="sqlfmt!",
                onclick=format_textarea,
                color="primary",
            ),
            output.put_widget(
                load_asset("details_template.html"),
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
    ).style(body_style)
    output.put_html(load_asset("footer.html"))
    output.put_html("<script>set_theme(get_theme_from_storage())</script>")


def serve_index() -> None:
    config(
        title="sqlfmt: The autoformatter for dbt SQL",
        description=(
            "sqlfmt formats your dbt SQL files so you don't have to. "
            "It is similar in nature to black, gofmt, and rustfmt."
        ),
        css_style=load_asset("index.css"),
        js_code=load_asset("script.js"),
    )
    port = os.environ.get("PORT", 5000)
    start_server(index, port=port, websocket_ping_interval=30)


if __name__ == "__main__":
    serve_index()
