from selenium.webdriver.common.by import By


def test_page_initial(driver):
    text = driver.find_element(By.ID, 'inputarea')
    score = driver.find_element(By.ID, 'playerScore')
    assert 50 <= len(text.text) <= 100
    assert score.text == '0'


def test_wrong_key(driver):
    text = driver.find_element(By.ID, 'inputarea')
    score = driver.find_element(By.ID, 'playerScore')
    page = driver.find_element(By.TAG_NAME, 'html')

    page.send_keys(chr(ord(text.text[0]) + 1))

    assert score.text == '0'


def test_required_key(driver, client, runner):
    text = driver.find_element(By.ID, 'inputarea')
    score = driver.find_element(By.ID, 'playerScore')
    page = driver.find_element(By.TAG_NAME, 'html')

    page.send_keys(text.text[0])
    page.send_keys(text.text[0])
    page.send_keys(text.text[0])
    page.send_keys(text.text[0])
    assert score.text == '1'


def test_connection(client):
    response = client.get("/")
    assert response.default_status == 200
    assert response.status_code == 302
