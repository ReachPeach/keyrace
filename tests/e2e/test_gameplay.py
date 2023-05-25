import time

from selenium.webdriver.common.by import By


def test_connection(client):
    response = client.get("/")
    assert response.default_status == 200
    assert response.status_code == 302


def click_button_by_id(driver, id):
    button = driver.find_element(By.ID, id)
    button.click()
    time.sleep(1)


def test_gameplay_interactions(driver):
    base_url = driver.current_url
    click_button_by_id(driver, 'newGameButton')

    assert driver.current_url == base_url.replace("index.html", "game.html")

    click_button_by_id(driver, 'playerReady')
    score = driver.find_elements(By.CLASS_NAME, 'score')[0]
    assert score.text == '0'

    text = driver.find_element(By.ID, 'remainingText')
    page = driver.find_element(By.TAG_NAME, 'html')

    page.send_keys(str(chr(ord(text.text[0]) + 1)))
    assert score.text == '0'

    page.send_keys(str(text.text[0]))
    time.sleep(1)
    assert score.text != '0'
