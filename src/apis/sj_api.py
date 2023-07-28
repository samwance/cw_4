import os
import requests
from datetime import datetime
from src.vacancy import Vacancy
from src.apis.base_api import BaseAPI


class SuperJobAPI(BaseAPI):
    """Класс запроса вакансий на SuperJob API"""
    url: str = "https://api.superjob.ru/2.0"

    def __init__(self, url: str = url):
        """
        Инициализация класса SuperJobAPI.

        :param url: URL для запросов к SuperJob API.
        """
        super().__init__(url)

    def search_vacancies(self, job_title: str, number_of_vacancies: int = 10) -> list:
        """
        Поиск вакансий на HeadHunter API.

        :param number_of_vacancies:
        :param job_title: Заголовок вакансии для поиска.
        :return: Список найденных вакансий.
        """
        url = f"{self._base_url}/vacancies/"
        headers = {
            "X-Api-App-Id": os.getenv("API_SUPERJOB_KEY")
        }
        params = {
            "keywords": [[1, job_title]],
            "count": number_of_vacancies,
        }

        response = requests.get(url, headers=headers, params=params)
        data = response.json()

        vacancies = []

        try:
            for item in data.get("objects", []):
                vacancy = Vacancy(title=self.get_title(item), url=self.get_url(item), salary=self.get_salary(item),
                                  pub_date=self.get_pub_date(item), requirements=self.get_requirements(item))
                vacancies.append(vacancy)
        except:
            pass

        return vacancies

    @staticmethod
    def get_title(vacancy) -> str:
        return vacancy['profession']

    @staticmethod
    def get_url(vacancy) -> str:
        return vacancy['link']

    @staticmethod
    def get_salary(vacancy) -> dict:
        salary = {'min': int(vacancy['payment_from']), 'currency': vacancy['currency']}
        if salary['min'] is None:
            salary['min'] = 0
        if vacancy['payment_to'] == (None or 0):
            salary['max'] = salary['min']
        else:
            salary['max'] = int(vacancy['payment_to'])
        return salary

    @staticmethod
    def get_pub_date(vacancy) -> str:
        return str(datetime.utcfromtimestamp(vacancy["date_published"]).date())

    @staticmethod
    def get_requirements(vacancy) -> str:
        return vacancy['candidat']