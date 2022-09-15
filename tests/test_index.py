import time

import pytest
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait


def get_active_textarea(context):
    # we select the text box (this is brittle and has to be done
    # exactly like this)

    code_div = WebDriverWait(context, timeout=5).until(
        lambda d: d.find_element(By.CLASS_NAME, "CodeMirror")
    )
    assert code_div
    code_line = code_div.find_element(By.CLASS_NAME, "CodeMirror-line")
    assert code_line
    code_line.click()

    textarea = code_div.find_element(By.TAG_NAME, "textarea")
    return textarea


def get_submit_button(context, do_click=True):
    submit_button = context.find_element(By.CSS_SELECTOR, ".btn-primary")
    assert submit_button
    if do_click:
        submit_button.click()
    return submit_button


def get_example_button(context, do_click=True):
    example_button = context.find_element(By.CSS_SELECTOR, ".btn-link")
    assert example_button
    if do_click:
        example_button.click()
    return example_button


def scroll_and_move_to_element(context, element):
    if "firefox" in context.capabilities["browserName"]:
        window_rect = context.get_window_rect()
        y = element.location["y"]
        scroll_amount = y - window_rect["y"] - (window_rect["height"] / 2)
        context.execute_script(f"window.scrollBy(0, {scroll_amount});")
    ActionChains(context).move_to_element(element).perform()
    return element


@pytest.mark.nondestructive
def test_index_title_and_header(selenium, base_url) -> None:
    # given that we go to sqlfmt.com
    selenium.get(base_url)

    # we see that the title of the page contains sqlfmt
    assert "sqlfmt" in selenium.title

    # we see that the header includes the word sqlfmt
    h1_tag = WebDriverWait(selenium, timeout=5).until(
        lambda d: d.find_element(By.TAG_NAME, "h1")
    )
    assert "sqlfmt" in h1_tag.text


@pytest.mark.nondestructive
def test_index_tracking(selenium, base_url) -> None:
    # given that we go to sqlfmt.com
    selenium.get(base_url)

    # we see that there is a script tag that includes code with the word "posthog"
    script_tags = WebDriverWait(selenium, timeout=5).until(
        lambda d: d.find_elements(By.TAG_NAME, "script")
    )
    assert any(["posthog" in tag.get_attribute("innerHTML") for tag in script_tags])


def test_index_end_to_end(selenium, base_url) -> None:

    # given that we go to sqlfmt.com
    selenium.get(base_url)

    textarea = get_active_textarea(selenium)
    # we type some poorly formatted sql into it
    textarea.send_keys(
        "select a,"
        + Keys.ENTER
        + "b,"
        + Keys.ENTER
        + "c"
        + Keys.ENTER
        + "    from my_table"
    )

    first_line = selenium.find_element(By.CLASS_NAME, "CodeMirror-line")
    assert first_line.text == "select a,"

    # we see that there is a button that says "sqlfmt!"
    submit_button = get_submit_button(selenium, do_click=False)
    assert submit_button.text == "sqlfmt!"

    # we click the button
    submit_button.click()

    # we see that there is a new banner on the page
    banner = WebDriverWait(selenium, timeout=5).until(
        lambda d: d.find_element(By.CLASS_NAME, "toastify")
    )
    assert banner.text == "Success! Formatting applied"

    # and we see that the code has been formatted
    new_first_line = selenium.find_element(By.CLASS_NAME, "CodeMirror-line")
    assert new_first_line.text == "select a, b, c from my_table"

    # the banner disappears after a few seconds
    time.sleep(3)

    # we click the button again
    submit_button.click()

    # and see a different banner
    info_banner = WebDriverWait(selenium, timeout=5).until(
        lambda d: d.find_element(By.CLASS_NAME, "toastify")
    )
    assert info_banner.text == "SQL already formatted"


def test_index_with_config(selenium, base_url) -> None:

    # given that we go to sqlfmt.com
    selenium.get(base_url)

    textarea = get_active_textarea(selenium)
    # we type some poorly formatted sql into it
    fifty_three_chars = "select something_long, something_long, something_long"
    textarea.send_keys(fifty_three_chars)

    first_line = selenium.find_element(By.CLASS_NAME, "CodeMirror-line")
    assert first_line.text == fifty_three_chars

    # we see there is a toggle for formatting options
    details = selenium.find_element(By.TAG_NAME, "details")
    assert details
    assert not details.get_property("open")
    summary = details.find_element(By.TAG_NAME, "summary")
    assert summary.text == "Configure Formatting"

    # we click the toggle and it opens
    scroll_and_move_to_element(selenium, details)
    details.click()
    assert details.get_property("open")

    # we see the default line length is 88
    slider_value = selenium.find_element(By.CLASS_NAME, "form-control-range-value")
    assert slider_value
    assert slider_value.text == "88"

    # we set the line_length slider to minimum (40)
    slider = selenium.find_element(By.CLASS_NAME, "form-control-range")
    assert slider
    ActionChains(selenium).drag_and_drop_by_offset(slider, -400, 0).perform()
    assert slider_value.text == "40"

    # we click the button that says "sqlfmt!"
    _ = get_submit_button(selenium, do_click=True)

    # we see that there is a new banner on the page
    banner = WebDriverWait(selenium, timeout=5).until(
        lambda d: d.find_element(By.CLASS_NAME, "toastify")
    )
    assert banner.text == "Success! Formatting applied"

    # and we see that the code has been formatted with a short line length
    new_first_line = selenium.find_element(By.CLASS_NAME, "CodeMirror-line")
    assert new_first_line.text == "select"


@pytest.mark.parametrize("bad_sql", [")", "$", "select /*"])
def test_index_error(selenium, base_url, bad_sql) -> None:

    # given that we go to sqlfmt.com
    selenium.get(base_url)

    # we get an active text box
    textarea = get_active_textarea(selenium)

    # we type something that is not valid sql
    textarea.send_keys(bad_sql)

    # we click the button
    _ = get_submit_button(selenium, do_click=True)

    # we see an error banner, with a helpful message
    error_banner = selenium.find_element(By.CLASS_NAME, "toastify")
    assert "sqlfmt encountered an error:" in error_banner.text


def test_index_example(selenium, base_url) -> None:

    # given that we go to sqlfmt.com
    selenium.get(base_url)

    # we see that the textarea is empty
    first_line = selenium.find_element(By.CLASS_NAME, "CodeMirror-line")
    assert first_line.text == ""

    # we click the load example button
    btn = get_example_button(selenium, do_click=True)
    assert btn.text == "Load example unformatted query"

    time.sleep(0.1)

    # we see that the textarea has the example query
    first_line = selenium.find_element(By.CLASS_NAME, "CodeMirror-line")
    assert (
        first_line.text
        == "with source as (select * from {{ source('my_application', 'users') }}),"
    )


def test_dark_mode(selenium, base_url) -> None:
    # given that we go to sqlfmt.com
    selenium.get(base_url)

    # we see that the html tag has a data-theme property set to light
    html = selenium.find_element(By.TAG_NAME, "html")
    assert html.get_attribute("data-theme") == "light"

    # we see the theme toggle button
    toggle_button = WebDriverWait(selenium, timeout=5).until(
        lambda d: d.find_element(By.CLASS_NAME, "toggleButton")
    )
    assert toggle_button

    # we click it
    toggle_button.click()
    time.sleep(0.1)

    # and we see that the theme has changed to dark
    assert html.get_attribute("data-theme") == "dark"


def test_logo(selenium, base_url) -> None:
    # given that we go to sqlfmt.com
    selenium.get(base_url)

    # we see that there is a logo in the nav bar
    logo = WebDriverWait(selenium, timeout=5).until(
        lambda d: d.find_element(By.CSS_SELECTOR, ".navbar__logo>img")
    )
    assert logo

    # the logo is not a broken image
    assert logo.get_property("naturalWidth") > 0
