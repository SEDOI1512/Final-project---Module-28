from selenium import webdriver
from selenium.webdriver.common.by import By

import time
import pytest
import pytest

not_reg_email = 'fatmabuenos@gmail.com'
reg_password_email = 'qwertQA124'

is_reg_phone = '+79271230866'
password_phone = 'qwertQA125'

is_reg_email = 'ivankinovich123@gmail.com'
password_email = 'qwertQA123'

email_for_reg='asf12300123@gmail.com'
password_for_reg='qwertQA134'

@pytest.fixture(autouse=True)
def testing():
    pytest.driver = webdriver.Chrome('./chromedriver.exe')
    pytest.driver.get('https://b2c.passport.rt.ru')

    pytest.driver.implicitly_wait(8)
    time.sleep(5)

    yield

    pytest.driver.quit()

# Вспомогательная функция для регистрации
def input_reg_par(reg_par, password, password_confirm=None):
    if password_confirm is None:
        password_confirm = password

    pytest.driver.find_element(By.ID, 'kc-register').click()

    pytest.driver.find_element(By.NAME, 'firstName').send_keys('Олег')
    pytest.driver.find_element(By.NAME, 'lastName').send_keys('Пупкин')

    pytest.driver.find_element(By.ID, 'address').send_keys(reg_par)
    pytest.driver.find_element(By.ID, 'password').send_keys(password)
    pytest.driver.find_element(By.ID, 'password-confirm').send_keys(password_confirm)

    pytest.driver.find_element(By.NAME, 'register').click()
    time.sleep(3)

# Проверяем наличие логотипа сбоку после нажатия кнопки для регистрации
def test_02_true_find_logo_in_reg():
    pytest.driver.find_element(By.ID, 'kc-register').click()
    time.sleep(3)

    try:
        logo_and_other = pytest.driver.find_element(By.CSS_SELECTOR, 'what-is-container')
    except:
        logo_and_other = None

    assert logo_and_other is not None

# Проверяем процесс регистрации
def test_03_registration():
    input_reg_par(email_for_reg, password_for_reg)

    # Здесь наш код встает в ожидание, пока мы в ручную не введем код в браузере
    while True:
        try:
            pytest.driver.find_element(By.ID, f'rt-code-0')
            time.sleep(3)
            continue
        except:
            break

    time.sleep(3)

    try:
        find_user_table = pytest.driver.find_element(By.CLASS_NAME, 'card-title')
    except:
        find_user_table = None

    assert find_user_table is not None

# Пытаемся зарегистрироваться с паролем из 5 символов
def test_04_less_8_password(password='qwert'):
    input_reg_par(not_reg_email, password)

    try:
        find_error_span = pytest.driver.find_element(By.CLASS_NAME, 'rt-input-container__meta--error')
        text = find_error_span.text.strip()
    except:
        find_error_span = None
        text = ''

    assert find_error_span is not None
    assert text == 'Длина пароля должна быть не менее 8 символов'

# Пытаемся зарегистрироваться с паролем только из строчных букв
def test_05_password_only_lower(password='qwertyuiop'):
    input_reg_par(not_reg_email, password)

    try:
        find_error_span = pytest.driver.find_element(By.CLASS_NAME, 'rt-input-container__meta--error')
        text = find_error_span.text.strip()
    except:
        find_error_span = None
        text = ''

    assert find_error_span is not None
    assert text == 'Пароль должен содержать хотя бы 1 спецсимвол или хотя бы одну цифру'

# Пытаемся зарегистрироваться с паролем из ру-символов
def test_06_password_ru(password='йцукенгшщРв'):
    input_reg_par(not_reg_email, password)

    try:
        find_error_span = pytest.driver.find_element(By.CLASS_NAME, 'rt-input-container__meta--error')
        text = find_error_span.text.strip()
    except:
        find_error_span = None
        text = ''

    assert find_error_span is not None
    assert text == 'Пароль должен содержать только латинские буквы'

# Пытаемся зарегистрироваться с паролем и не таким же паролем в графе "подтверждение пароля"
def test_07_password_not_confirm(password='qwertQA123', password_confirm='qwertQA1234'):
    input_reg_par(not_reg_email, password, password_confirm)

    try:
        find_error_span = pytest.driver.find_element(By.CLASS_NAME, 'rt-input-container__meta--error')
        text = find_error_span.text.strip()
    except:
        find_error_span = None
        text = ''

    assert find_error_span is not None
    assert text == 'Пароли не совпадают'

# Пытаемся зарегистрироваться на уже существующий email
def test_08_user_email_already_reg():
    input_reg_par(is_reg_email, password_email)

    try:
        find_join_button = pytest.driver.find_element(By.NAME, 'gotoLogin')
        text_join = find_join_button.text.strip()
    except:
        find_join_button = None
        text_join = ''

    try:
        find_reset_href = pytest.driver.find_element(By.ID, 'reg-err-reset-pass')
        text_reset = find_reset_href.text.strip()
    except:
        find_reset_href = None
        text_reset = ''

    assert find_join_button is not None
    assert find_reset_href is not None
    assert text_join == 'Войти'
    assert text_reset == 'Восстановить пароль'

# Пытаемся зарегистрироваться на уже существующий телефон
def test_09_user_phone_already_reg():
    input_reg_par(is_reg_phone, password_phone)

    try:
        find_join_button = pytest.driver.find_element(By.NAME, 'gotoLogin')
        text_join = find_join_button.text.strip()
    except:
        find_join_button = None
        text_join = ''

    try:
        find_reset_href = pytest.driver.find_element(By.NAME, 'registration_confirm_btn')
        text_reset = find_reset_href.text.strip()
    except:
        find_reset_href = None
        text_reset = ''

    assert find_join_button is not None
    assert find_reset_href is not None
    assert text_join == 'Войти'
    assert text_reset == 'Зарегистрироваться'

# Авторизация с помощью телефона
def test_10_phone_auth():
    pytest.driver.find_element(By.ID, 'username').send_keys(is_reg_phone)
    pytest.driver.find_element(By.ID, 'password').send_keys(password_phone)
    pytest.driver.find_element(By.ID, 'kc-login').click()
    time.sleep(3)

    try:
        find_user_table = pytest.driver.find_element(By.CLASS_NAME, 'card-title')
    except:
        find_user_table = None

    assert find_user_table is not None

# Попытка авторизации через телефон с неправильным телефоном
def test_11_phone_auth_wrong_phone(reg_par='+79001001010', password='qwertQA125'):
    pytest.driver.find_element(By.ID, 'username').send_keys(reg_par)
    pytest.driver.find_element(By.ID, 'password').send_keys(password)
    pytest.driver.find_element(By.ID, 'kc-login').click()
    time.sleep(3)

    try:
        find_error_span = pytest.driver.find_element(By.ID, 'form-error-message')
        text = find_error_span.text.strip()
    except:
        find_error_span = None
        text = ''

    try:
        find_class_atr = pytest.driver.find_element(By.CLASS_NAME, 'rt-link--muted')
    except:
        find_class_atr = None

    assert find_error_span is not None
    assert text == 'Неверный логин или пароль'
    assert find_class_atr is None

# Попытка авторизации через телефон с пустым телефоном
def test_12_phone_auth_not_phone(reg_par='', password='qwertQA125'):
    pytest.driver.find_element(By.ID, 'username').send_keys(reg_par)
    pytest.driver.find_element(By.ID, 'password').send_keys(password)
    pytest.driver.find_element(By.ID, 'kc-login').click()
    time.sleep(3)

    try:
        find_error_span = pytest.driver.find_element(By.CLASS_NAME, 'rt-input-container__meta--error')
        text = find_error_span.text.strip()
    except:
        find_error_span = None
        text = ''

    assert find_error_span is not None
    assert text == 'Введите номер телефона'

# Авторизация с помощью email
def test_13_email_auth():
    pytest.driver.find_element(By.ID, 't-btn-tab-mail').click()
    time.sleep(2)
    pytest.driver.find_element(By.ID, 'username').send_keys(is_reg_email)
    pytest.driver.find_element(By.ID, 'password').send_keys(password_email)
    pytest.driver.find_element(By.ID, 'kc-login').click()
    time.sleep(3)

    try:
        find_user_table = pytest.driver.find_element(By.CLASS_NAME, 'card-title')
    except:
        find_user_table = None

    assert find_user_table is not None

# Попытка авторизации через email с неправильным email
def test_14_email_auth_wrong_email(reg_par='ivankefwefgweinovich123@gmawgewegil.comweg', password='qwertQA123'):
    pytest.driver.find_element(By.ID, 't-btn-tab-mail').click()
    time.sleep(2)
    pytest.driver.find_element(By.ID, 'username').send_keys(reg_par)
    pytest.driver.find_element(By.ID, 'password').send_keys(password)
    pytest.driver.find_element(By.ID, 'kc-login').click()
    time.sleep(3)

    try:
        find_error_span = pytest.driver.find_element(By.ID, 'form-error-message')
        text = find_error_span.text.strip()
    except:
        find_error_span = None
        text = ''

    try:
        find_class_atr = pytest.driver.find_element(By.CLASS_NAME, 'rt-link--muted')
    except:
        find_class_atr = None

    assert find_error_span is not None
    assert text == 'Неверный логин или пароль'
    assert find_class_atr is None

# Попытка авторизации через email с пустым email
def test_15_email_auth_not_email(reg_par='', password='qwertQA123'):
    pytest.driver.find_element(By.ID, 't-btn-tab-mail').click()
    time.sleep(2)
    pytest.driver.find_element(By.ID, 'username').send_keys(reg_par)
    pytest.driver.find_element(By.ID, 'password').send_keys(password)
    pytest.driver.find_element(By.ID, 'kc-login').click()
    time.sleep(3)

    try:
        find_error_span = pytest.driver.find_element(By.CLASS_NAME, 'rt-input-container__meta--error')
        text = find_error_span.text.strip()
    except:
        find_error_span = None
        text = ''

    assert find_error_span is not None
    assert text == 'Введите адрес, указанный при регистрации'

# Попытка авторизации через login с неправильным login
def test_16_login_auth_wrong_login(reg_par='asdasdasdasd', password='qwertQA123'):
    pytest.driver.find_element(By.ID, 't-btn-tab-login').click()
    time.sleep(2)
    pytest.driver.find_element(By.ID, 'username').send_keys(reg_par)
    pytest.driver.find_element(By.ID, 'password').send_keys(password)
    pytest.driver.find_element(By.ID, 'kc-login').click()
    time.sleep(3)

    try:
        find_error_span = pytest.driver.find_element(By.ID, 'form-error-message')
        text = find_error_span.text.strip()
    except:
        find_error_span = None
        text = ''

    try:
        find_class_atr = pytest.driver.find_element(By.CLASS_NAME, 'rt-link--muted')
    except:
        find_class_atr = None

    assert find_error_span is not None
    assert text == 'Неверный логин или пароль'
    assert find_class_atr is None

# Попытка авторизации через login с пустым login
def test_17_login_auth_not_login(reg_par='', password='qwertQA123'):
    pytest.driver.find_element(By.ID, 't-btn-tab-login').click()
    time.sleep(2)
    pytest.driver.find_element(By.ID, 'username').send_keys(reg_par)
    pytest.driver.find_element(By.ID, 'password').send_keys(password)
    pytest.driver.find_element(By.ID, 'kc-login').click()
    time.sleep(3)

    try:
        find_error_span = pytest.driver.find_element(By.CLASS_NAME, 'rt-input-container__meta--error')
        text = find_error_span.text.strip()
    except:
        find_error_span = None
        text = ''

    assert find_error_span is not None
    assert text == 'Введите логин, указанный при регистрации'

# Попытка авторизации через bill с неправильным bill
def test_18_bill_auth_wrong_bill(reg_par='ewgesgsg', password='qwertQA123'):
    pytest.driver.find_element(By.ID, 't-btn-tab-ls').click()
    time.sleep(2)
    pytest.driver.find_element(By.ID, 'username').send_keys(reg_par)
    pytest.driver.find_element(By.ID, 'password').send_keys(password)
    pytest.driver.find_element(By.ID, 'kc-login').click()
    time.sleep(3)

    try:
        find_error_span = pytest.driver.find_element(By.ID, 'form-error-message')
        text = find_error_span.text.strip()
    except:
        find_error_span = None
        text = ''

    try:
        find_class_atr = pytest.driver.find_element(By.CLASS_NAME, 'rt-link--muted')
    except:
        find_class_atr = None

    assert find_error_span is not None
    assert text == 'Неверный логин или пароль'
    assert find_class_atr is None

# Попытка авторизации через bill с пустым bill
def test_19_bill_auth_not_bill(reg_par='', password='qwertQA123'):
    pytest.driver.find_element(By.ID, 't-btn-tab-ls').click()
    time.sleep(2)
    pytest.driver.find_element(By.ID, 'username').send_keys(reg_par)
    pytest.driver.find_element(By.ID, 'password').send_keys(password)
    pytest.driver.find_element(By.ID, 'kc-login').click()
    time.sleep(3)

    try:
        find_error_span = pytest.driver.find_element(By.CLASS_NAME, 'rt-input-container__meta--error')
        text = find_error_span.text.strip()
    except:
        find_error_span = None
        text = ''

    assert find_error_span is not None
    assert text == 'Введите номер вашего лицевого счета'

# Попытка изменить пароль с помощью "восстановление пароля" на пароль с 5 символами
def test_20_recover_password_by_phone_less_8_symbols(password='qwert'):
    pytest.driver.find_element(By.ID, 'forgot_password').click()
    time.sleep(2)

    while True:
        try:
            pytest.driver.find_element(By.ID, 'username').send_keys(is_reg_phone)
            now_text = pytest.driver.find_element(By.CLASS_NAME, 'card-container__desc').text.strip()
            if now_text != 'Введите данные и нажмите «Продолжить»': break
            time.sleep(10)
            pytest.driver.find_element(By.NAME, 'reset').click()
        except: break

    # Здесь наш код встаем в режим ожидания и ждем, пока мы не введем код для продолжения попытки изменения пароля
    while True:
        try:
            pytest.driver.find_element(By.CLASS_NAME, 'code-input-container__timeout')
        except:
            break

    pytest.driver.find_element(By.NAME, 'password-new').send_keys(password)
    pytest.driver.find_element(By.NAME, 'password-confirm').send_keys(password)
    time.sleep(2)

    pytest.driver.find_element(By.ID, 't-btn-reset-pass').click()
    time.sleep(2)

    try:
        find_error_span = pytest.driver.find_element(By.CLASS_NAME, 'rt-input-container__meta--error')
        text = find_error_span.text.strip()
    except:
        find_error_span = None
        text = ''

    assert find_error_span is not None
    assert text == 'Длина пароля должна быть не менее 8 символов'

# Попытка изменить пароль с помощью "восстановление пароля" на пароль такой же, как и предыдущий
def test_21_recover_password_by_phone_old_password():
    pytest.driver.find_element(By.ID, 'forgot_password').click()
    time.sleep(2)

    while True:
        try:
            pytest.driver.find_element(By.ID, 'username').send_keys(is_reg_phone)
            now_text = pytest.driver.find_element(By.CLASS_NAME, 'card-container__desc').text.strip()
            if now_text != 'Введите данные и нажмите «Продолжить»': break
            time.sleep(10)
            pytest.driver.find_element(By.NAME, 'reset').click()
        except:
            break

    # Здесь наш код встаем в режим ожидания и ждем, пока мы не введем код для продолжения попытки изменения пароля
    while True:
        try:
            pytest.driver.find_element(By.CLASS_NAME, 'code-input-container__timeout')
        except:
            break

    pytest.driver.find_element(By.NAME, 'password-new').send_keys(password_phone)
    pytest.driver.find_element(By.NAME, 'password-confirm').send_keys(password_phone)
    time.sleep(2)

    pytest.driver.find_element(By.ID, 't-btn-reset-pass').click()
    time.sleep(2)

    try:
        find_error_span = pytest.driver.find_element(By.ID, 'form-error-message')
        text = find_error_span.text.strip()
    except:
        find_error_span = None
        text = ''

    assert find_error_span is not None
    assert text == 'Этот пароль уже использовался, укажите другой пароль'

# Попытка изменить пароль с помощью "восстановление пароля" на пароль с ру-символами
def test_22_recover_password_by_phone_ru(password='йцукенгшщз'):
    pytest.driver.find_element(By.ID, 'forgot_password').click()
    time.sleep(2)

    while True:
        try:
            pytest.driver.find_element(By.ID, 'username').send_keys(is_reg_phone)
            now_text = pytest.driver.find_element(By.CLASS_NAME, 'card-container__desc').text.strip()
            if now_text != 'Введите данные и нажмите «Продолжить»': break
            time.sleep(10)
            pytest.driver.find_element(By.NAME, 'reset').click()
        except:
            break

    # Здесь наш код встаем в режим ожидания и ждем, пока мы не введем код для продолжения попытки изменения пароля
    while True:
        try:
            pytest.driver.find_element(By.CLASS_NAME, 'code-input-container__timeout')
        except:
            break

    pytest.driver.find_element(By.NAME, 'password-new').send_keys(password)
    pytest.driver.find_element(By.NAME, 'password-confirm').send_keys(password)
    time.sleep(2)

    pytest.driver.find_element(By.ID, 't-btn-reset-pass').click()
    time.sleep(2)

    try:
        find_error_span = pytest.driver.find_element(By.CLASS_NAME, 'rt-input-container__meta--error')
        text = find_error_span.text.strip()
    except:
        find_error_span = None
        text = ''

    assert find_error_span is not None
    assert text == 'Пароль должен содержать только латинские буквы'
