import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

@pytest.fixture(autouse=True)
def driver():
    pytest.driver = webdriver.Chrome()
    # Переходим на страницу авторизации
    pytest.driver.get('https://petfriends.skillfactory.ru/login')

    yield

    pytest.driver.quit()

# @pytest.fixture()
def test_show_my_pets(driver):
    # Вводим email
    pytest.driver.find_element(By.ID, 'email').send_keys('dimka-1302@yandex.ru')

    # Вводим пароль
    pytest.driver.find_element(By.ID, 'pass').send_keys('olya0610')

    time.sleep(5)
    # Нажимаем на кнопку входа в аккаунт
    pytest.driver.find_element(By.XPATH, '//body/div[1]/div[1]/form[1]/div[3]/button[1]').click()
    #  Пререходим на страницу Мои питомцы
    pytest.driver.find_element(By.CSS_SELECTOR, 'A[href="/my_pets"]').click()
    """Проверяем, что мы оказались на странице пользователя"""

    assert pytest.driver.find_element(By.TAG_NAME, 'h2').text == "Дмитрий Егоров"


    # Сохраняем элементы изображений
    images = pytest.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/th')
    # Записываем строки таблицы Мои питомцы
    lines_of_tabel = pytest.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr')
    number_of_pets = len(lines_of_tabel)
    # descriptions = driver.find_elements(By.XPATH, '.card-deck .card-text')

    # Сохряняем данные статистики
    statistics = pytest.driver.find_element(By.CSS_SELECTOR, '.\\.col-sm-4.left')
    # Берем из статистики значение общего количества питомцев
    number = statistics.text.split('\n')
    number = number[1].split(' ')
    number = int(number[1])
    """Сравниваем количество питомцев со статистикой"""
    assert number == number_of_pets


    pytest.driver.implicitly_wait(10)
    # Находим половину от всего списка питомцев
    half = number//2

    # находим количество питомцев с фото
    images_count = 0

    for i in range(len(images)):
        if images[i].get_attribute('src') != '':
            images_count += 1

    # Проверем, что количество фото питомцев больше или равно половине
    assert images_count >= half

    """ Проверка что у всех разные имена"""
    try:
        list_names = []

        wait = WebDriverWait(pytest.driver, 5)
        for i in range(len(lines_of_tabel)):
            assert wait.until(EC.visibility_of(lines_of_tabel[i]))

        for i in range(len(lines_of_tabel)):
            list_names.append(lines_of_tabel[i].text)

        # преобразовываем список в множество
        set_pet_data = set(list_names)

        # Cравниваем длину списка и множества: без повторов должны совпасть
        assert len(list_names) == len(set_pet_data)

    except AssertionError:
        print('В списке есть повторяющиеся имена питомцев')

    """Проверяем, что в списке нет повторяющихся питомцев:"""
    try:
        list_data_my_pets = []  # создаем список для хранения информации о питомцах
        for i in range(len(lines_of_tabel)):
          list_data = lines_of_tabel[i].text.split("\n")  # отделяем от данных питомца "х" удаления питомца
          list_data_my_pets.append(list_data[0])  # выбираем элемент с данными питомца и добавляем его в список
        set_data_my_pets = set(list_data_my_pets)  # преобразовываем список в множество для избежания дубликатов

        # сравниваем длину списка и множества
        assert len(list_data_my_pets) == len(set_data_my_pets)
    except AssertionError:
        print('В списке есть повторяющиеся питомцы')


