import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


@pytest.fixture
def driver():
    # Selenium Manager will auto-download the appropriate driver
    options = Options()
    options.add_argument("--headless")  # run without UI
    options.add_argument("--no-sandbox")  # required in many CI environments
    options.add_argument("--disable-dev-shm-usage")  # overcome limited /dev/shm size on Linux

    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

def test_successful_login(driver):
    # Открываем страницу авторизации
    driver.get("https://the-internet.herokuapp.com/login")

    # Вводим имя пользователя и пароль
    username = driver.find_element(By.ID, "username")
    password = driver.find_element(By.ID, "password")
    submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")

    username.send_keys("tomsmith")
    password.send_keys("SuperSecretPassword!")
    submit_button.click()

    # Проверяем, авторизованы
    success_message = driver.find_element(By.ID, "flash")
    assert "You logged into a secure area!" in success_message.text
    assert driver.current_url == "https://the-internet.herokuapp.com/secure"


def test_unsuccessful_login(driver):
    # Открываем страницу авторизации
    driver.get("https://the-internet.herokuapp.com/login")

    # Вводим неправильные имя пользователя и пароль
    username = driver.find_element(By.ID, "username")
    password = driver.find_element(By.ID, "password")
    submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")

    username.send_keys("tomsmithhhhh")
    password.send_keys("SuperSecretPassworddddddd")
    submit_button.click()

    # Проверяем, что ввели ошибочные данные
    error_message = driver.find_element(By.ID, "flash")
    assert "Your username is invalid!" in error_message.text
    assert driver.current_url == "https://the-internet.herokuapp.com/login"