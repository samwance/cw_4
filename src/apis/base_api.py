from abc import ABC, abstractmethod


class BaseAPI(ABC):
    def __init__(self, base_url: str):
        """
        Инициализация базового класса для API.

        :param base_url: Базовый URL для API.
        """
        self._base_url = base_url

    @abstractmethod
    def search_vacancies(self, job_title: str, number_of_vacancies: int) -> list:
        """
        Метод для поиска вакансий.

        :param number_of_vacancies: Количество вакансий для поиска
        :param job_title: Заголовок вакансии.
        :return: Список найденных вакансий.
        """
        pass

    @staticmethod
    def get_title(vacancy) -> str:
        pass

    @staticmethod
    def get_url(vacancy) -> str:
        pass

    @staticmethod
    def get_salary(vacancy) -> dict:
        pass

    @staticmethod
    def get_pub_date(vacancy) -> str:
        pass

    @staticmethod
    def get_requirements(vacancy) -> str:
        pass