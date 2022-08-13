import os

from pywebio import config, output, pin, start_server
from sqlfmt.api import format_string
from sqlfmt.exception import SqlfmtError
from sqlfmt.mode import Mode

# from sqlfmt_web.header import HEADER

# flake8: noqa
_POSTHOG = """
!function(t,e){var o,n,p,r;e.__SV||(window.posthog=e,e._i=[],e.init=function(i,s,a){function g(t,e){var o=e.split(".");2==o.length&&(t=t[o[0]],e=o[1]),t[e]=function(){t.push([e].concat(Array.prototype.slice.call(arguments,0)))}}(p=t.createElement("script")).type="text/javascript",p.async=!0,p.src=s.api_host+"/static/array.js",(r=t.getElementsByTagName("script")[0]).parentNode.insertBefore(p,r);var u=e;for(void 0!==a?u=e[a]=[]:a="posthog",u.people=u.people||[],u.toString=function(t){var e="posthog";return"posthog"!==a&&(e+="."+a),t||(e+=" (stub)"),e},u.people.toString=function(){return u.toString(1)+".people (stub)"},o="capture identify alias people.set people.set_once set_config register register_once unregister opt_out_capturing has_opted_out_capturing opt_in_capturing reset isFeatureEnabled onFeatureFlags".split(" "),n=0;n<o.length;n++)g(u,o[n]);e._i.push([i,s,a])},e.__SV=1)}(document,window.posthog||[]);
posthog.init('phc_JvcbkJ52TJpVaMxGHRGOxYrcOuTKU05949sLeVp8r7g',{api_host:'https://app.posthog.com'})
"""
HEADER = "\n".join([_POSTHOG])


def greeting() -> str:

    greeting = [
        "# sqlfmt",
        (
            "sqlfmt formats your dbt SQL files so you don't have to. It is similar "
            "in nature to black, gofmt, and rustfmt (but for SQL)."
        ),
        "When you use sqlfmt:",
        (
            "1. You never have to mention (or argue about) code style in code "
            "reviews again"
        ),
        (
            "1. You make it easier to collaborate and solicit contributions from "
            "new people"
        ),
        "1. You will be able to read your team's code as if you wrote it",
        (
            "1. You can forget about formatting your code, and spend your time on "
            "business logic instead"
        ),
        "",
        "## Installing sqlfmt",
        (
            "If you want to use the sqlfmt command-line tool "
            "on MacOS, Linux, or Windows, "
            "visit the [Github Repo](https://github.com/tconbeer/sqlfmt) "
            "for more information, "
            "or `pipx install shandy-sqlfmt`"
        ),
        "## Or you can try it out here",
        (
            "Type or paste SQL into the box below, then click the button to "
            "see your code in the sqlfmt style"
        ),
    ]

    return "\n".join(greeting)


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


def update_textarea() -> None:
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
    output.put_markdown(greeting(), lstrip=True)

    pin.put_textarea("source_sql", rows=20, code={"mode": "sql", "indentUnit": 4})
    output.put_row(
        [
            output.put_button(
                label="sqlfmt!",
                onclick=update_textarea,
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
        js_code=HEADER,
    )
    port = os.environ.get("PORT", 5000)
    start_server(index, port=port, websocket_ping_interval=30)


if __name__ == "__main__":
    serve_index()
