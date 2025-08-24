import pytest
import allure
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

@allure.step("Ввод логина: {username}")
def enter_username(element, username):
    element.send_keys(username)

@allure.step("Ввод пароля")
def enter_password(element, password):
    element.send_keys(password)

@allure.step("Нажатие кнопки входа")
def click_submit(button):
    button.click()

@allure.title("Тест успешной авторизации")
@allure.description("""
Проверка корректной авторизации с валидными учетными данными:
- Ввод корректного имени пользователя
- Ввод корректного пароля
- Проверка успешного сообщения
""")
@allure.feature("Авторизация")
def test_successful_login(driver):
    # Открываем страницу авторизации
    driver.get("https://the-internet.herokuapp.com/login")

    # Вводим имя пользователя и пароль
    username = driver.find_element(By.ID, "username")
    password = driver.find_element(By.ID, "password")
    submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")

    enter_username(username, "tomsmith")
    enter_password(password, "SuperSecretPassword!")
    click_submit(submit_button)

    # Проверяем, авторизованы
    success_message = driver.find_element(By.ID, "flash")
    assert "You logged into a secure area!" in success_message.text
    assert driver.current_url == "https://the-internet.herokuapp.com/secure"

@allure.title("Тест неуспешной авторизации")
@allure.description("""
Проверка обработки ошибки при вводе невалидных учетных данных:
- Ввод некорректного имени пользователя
- Ввод некорректного пароля
- Проверка сообщения об ошибке
""")
@allure.feature("Авторизация")
def test_unsuccessful_login(driver):
    # Открываем страницу авторизации
    driver.get("https://the-internet.herokuapp.com/login")

    # Вводим неправильные имя пользователя и пароль
    username = driver.find_element(By.ID, "username")
    password = driver.find_element(By.ID, "password")
    submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")

    enter_username(username, "tomsmithhhhh")
    enter_password(password, "SuperSecretPassworddddddd")
    click_submit(submit_button)

    # Проверяем, что ввели ошибочные данные
    error_message = driver.find_element(By.ID, "flash")
    assert "Your username is invalid!" in error_message.text
    assert driver.current_url == "https://the-internet.herokuapp.com/login"