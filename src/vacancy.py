import requests
from datetime import datetime


class Vacancy:
    """Класс, представляющий информацию о вакансии"""

    def __init__(self, title: str, url: str, salary: dict, pub_date: str, requirements: str):
        """
        Инициализация объекта Vacancy.

        :param title: Название вакансии.
        :param url: Ссылка на вакансию.
        :param salary: Зарплата {'min': int, 'max': int, 'currency': str}
        :param pub_date: Дата размещения вакансии в формате ISO
        :param requirements: Требования к вакансии
        """

        self.__title = self.validate_title(title)
        self.__url = self.validate_url(url)
        self.__salary = self.validate_salary(salary)
        self.__pub_date = self.validate_pub_date(pub_date)
        self.__requirements = self.validate_requirements(requirements)

    @property
    def title(self):
        return self.__title

    @property
    def url(self):
        return self.__url

    @property
    def salary(self):
        return self.__salary

    @property
    def medium_salary(self):
        return round((self.salary['min'] + self.salary['max']) / 2)

    @property
    def pub_date(self):
        return self.__pub_date

    @property
    def requirements(self):
        return self.__requirements

    def __str__(self) -> str:
        """
        Возвращает строковое представление вакансии.

        :return: Строковое представление вакансии.
        """
        return f'Вакансия "{self.title}" от {self.__pub_date}, зарплата от {self.salary["min"]} ' \
               f'до {self.salary["max"]} {self.salary["currency"]}'

    def __repr__(self) -> str:
        """
        Возвращает представление вакансии в виде строки.

        :return: Представление вакансии в виде строки.
        """
        return f"Vacancy({self.__dict__()})"

    def __dict__(self):
        return {
            'title': self.title,
            'url': self.url,
            'salary': self.salary,
            'pub_date': self.pub_date,
            'requirements': self.requirements
        }

    def __eq__(self, other: 'Vacancy') -> bool:
        """
        Проверяет, равны ли две вакансии по зарплате.

        :param other: Другая вакансия для сравнения.
        :return: True, если зарплаты равны, иначе False.
        """
        return self.medium_salary == other.medium_salary

    def __lt__(self, other: 'Vacancy') -> bool:
        """
        Определяет порядок сортировки вакансий по зарплате.

        :param other: Другая вакансия для сравнения.
        :return: True, если текущая вакансия имеет меньшую зарплату, иначе False.
        """
        return self.medium_salary < other.medium_salary

    def __gt__(self, other: 'Vacancy') -> bool:
        """
        Определяет порядок сортировки вакансий по зарплате.

        :param other: Другая вакансия для сравнения.
        :return: True, если текущая вакансия имеет большую зарплату, иначе False.
        """
        return self.medium_salary > other.medium_salary

    @salary.setter
    def salary(self, value: dict) -> None:
        """
        Устанавливает зарплату вакансии.

        :param value: Значение зарплаты.
        """
        self.__salary = self.validate_salary(value)

    @staticmethod
    def validate_title(title: str) -> str:
        """
        Валидирует название вакансии

        :param title: название вакансии
        :return: название вакансии или ошибка
        """
        if title:
            return title
        else:
            raise Exception('Пустое название вакансии')

    @staticmethod
    def validate_url(url: str) -> str:
        """
        Валидирует ссылку на вакансию

        :param url: ссылка на вакансию
        :return: ссылка на вакансию или ошибка
        """
        status_code = requests.get(url=url).status_code
        if status_code == 200:
            return url
        else:
            raise Exception(f'Неверная ссылка, status code {status_code}')

    @staticmethod
    def validate_salary(salary: dict) -> dict:
        """
        Валидирует зарплату вакансии

        :param salary: словарь с минимальной и максимальной зарплатой
        :return: словарь с минимальной и максимальной зарплатой
        """
        if salary:
            if salary['min'] and salary['max'] and salary['currency']:
                if salary['min'] <= salary['max']:
                    return salary
                else:
                    max_salary = salary['min']
                    salary['min'] = salary['max']
                    salary['max'] = max_salary
                    return salary
            else:
                raise Exception(f'Одно или оба поля зарплаты не заполнены, {salary}')
        else:
            raise Exception("Формат зарплаты {'min': int, 'max': int, 'currency': str}")

    @staticmethod
    def validate_pub_date(pub_date: str) -> str:
        """
        Валидирует дату публикации вакансии

        :param pub_date: дата публикации вакансии в формате ISO
        :return: дата публикации вакансии в формате ISO
        """

        if pub_date == str(datetime.fromisoformat(pub_date).date()):
            return pub_date
        else:
            raise Exception('Неверный формат даты')

    @staticmethod
    def validate_requirements(requirements: str) -> str:
        """
        Валидирует требования к вакансии

        :param requirements: дата публикации вакансии в формате ISO
        :return: требования к вакансии
        """

        if requirements:
            return requirements
        else:
            raise Exception('Требования отсутствуют')

    def validate_data(self) -> bool:
        """
        Проверяет, являются ли все данные вакансии валидными.

        :return: True, если все данные валидны, иначе False.
        """
        if not all([self.title, self.url, self.salary, self.pub_date, self.requirements]):
            return False
        raise Exception('Некоторые атрибуты вакансии не заданы')