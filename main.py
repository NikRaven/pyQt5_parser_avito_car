# Импортируйте необходимые классы для создания окна и элементов управления:
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QTextEdit
from PyQt5 import QtWidgets
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import time


# Создадим основной класс приложения, который будет содержать главное окно:
class WebParserApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # Создание элементов управления
        layout = QVBoxLayout()
        self.url_input = QLineEdit()  # QLineEdit()
        self.url_input.setText('https://www.avito.ru/all/avtomobili?cd=1')
        self.key_world = QLineEdit()
        self.parse_button = QPushButton('Parse')
        self.result_output = QTextEdit()

        # Добавление элементов управления на окно
        layout.addWidget(self.url_input)
        layout.addWidget(self.key_world)
        layout.addWidget(self.parse_button)
        layout.addWidget(self.result_output)

        # Связывание кнопки с функцией парсинга
        self.parse_button.clicked.connect(self.parse_website)

        self.setLayout(layout)
        self.setWindowTitle('Web Parser')

        # Message Box
        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle("Pyqt5 Alert")
        msg.setText("Программа предназначена для тестового использования!"
                    "Для продолжения нажмите OK")
        msg.setIcon(QtWidgets.QMessageBox.Critical)
        msg.exec_()

    # parse_website будет выполнять парсинг сайта при нажатии кнопки:
    # https://www.avito.ru/all/avtomobili?cd=1
    # код для парсинга сайта avito с использованием BeautifulSoup
    # Результат парсинга можно выводить в QTextEdit с помощью метода self.result_output.setText()
    def parse_website(self):
        itog = set()
        url = self.url_input.text()  # ('https://www.avito.ru/all/avtomobili?cd=1')
        n = self.key_world.text()
        # Программа выведет:
        driver = webdriver.Chrome()
        driver.get(url)  # загружаем страницу с поиском авто по категориям
        assert "Купить авто" in driver.title  # регистрируем текстовое поле и имитируем ввод строки "Купить авто"
        search = driver.find_element(By.CLASS_NAME, "input-input-Zpzc1")
        search.send_keys(n)
        open_search = driver.find_element(By.CLASS_NAME, "desktop-15w37ob")
        open_search.click()
        time.sleep(10)  # ставим на паузу, чтобы страница прогрузилась
        soup = BeautifulSoup(driver.page_source, 'lxml')
        # загружаем страницу и извлекаем ссылки через атрибут class
        all_publications2 = \
            soup.find_all('a', {'class': 'iva-item-sliderLink-uLz1v'})
        print(len(all_publications2))
        # форматируем результат
        for article in all_publications2:
            obj_i = "https://www.avito.ru" + article['href']
            itog.add(obj_i)
        # Открываем или создаем файл с именем "example.txt" в режиме записи ("w")
        with open('./file/example.txt', 'w') as file:
            for index, value in enumerate(itog):
                # Записываем текст в файл
                file.write(f'{index}:{value}' + '\n')
        out_result = self.result_output.setText('В папке file Вы обнаружите ссылки по искомому запросу!')


if __name__ == '__main__':
    app = QApplication([])
    window = WebParserApp()
    window.show()
    app.exec()
