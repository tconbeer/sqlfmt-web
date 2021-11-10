import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait


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
def test_index_end_to_end(selenium, base_url) -> None:

    # given that we go to sqlfmt.com
    selenium.get(base_url)

    # there is a CodeMirror div
    code_div = WebDriverWait(selenium, timeout=5).until(
        lambda d: d.find_element(By.CLASS_NAME, "CodeMirror")
    )
    assert code_div

    # we select the text box (this is brittle and has to be done
    # exactly like this)
    code_line = code_div.find_element(By.CLASS_NAME, "CodeMirror-line")
    assert code_line
    code_line.click()

    # we type some poorly formatted sql into it
    textarea = code_div.find_element(By.TAG_NAME, "textarea")
    textarea.send_keys(
        "select a,"
        + Keys.ENTER
        + "b,"
        + Keys.ENTER
        + "c"
        + Keys.ENTER
        + "    from my_table"
    )

    first_line = code_div.find_element(By.CLASS_NAME, "CodeMirror-line")
    assert first_line.text == "select a,"

    # we see that there is a button that says "sqlfmt!"
    submit_button = selenium.find_element(By.TAG_NAME, "button")
    assert submit_button
    assert submit_button.text == "sqlfmt!"

    # we click the button
    submit_button.click()

    # we see that the code has been formatted
    new_first_line = WebDriverWait(selenium, timeout=5).until(
        lambda d: d.find_element(By.CLASS_NAME, "CodeMirror-line")
    )
    assert new_first_line.text == "select a, b, c from my_table"
