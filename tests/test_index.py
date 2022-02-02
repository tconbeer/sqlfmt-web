import time

import pytest
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
    submit_button = context.find_element(By.TAG_NAME, "button")
    assert submit_button
    if do_click:
        submit_button.click()
    return submit_button


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

    # we see that the code has been formatted
    new_first_line = WebDriverWait(selenium, timeout=5).until(
        lambda d: d.find_element(By.CLASS_NAME, "CodeMirror-line")
    )
    assert new_first_line.text == "select a, b, c from my_table"

    # and that there is a new banner on the page
    banner = selenium.find_element(By.CLASS_NAME, "toastify")
    assert banner.text == "Success! Formatting applied"

    # the banner disappears after a few seconds
    time.sleep(3)

    # we click the button again
    submit_button.click()

    # and see a different banner
    info_banner = selenium.find_element(By.CLASS_NAME, "toastify")
    assert info_banner.text == "SQL already formatted"


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
