import requests
from src.apis.base_api import BaseAPI
from datetime import datetime
from src.vacancy import Vacancy


class HeadHunterAPI(BaseAPI):
    """Класс для запроса вакансий на HeadHunter API"""

    url: str = 'https://api.hh.ru/vacancies'

    def __init__(self, url: str = url):
        """
        Инициализация класса HeadHunterAPI.

        :param url: URL для запросов к HeadHunter API.
        """
        super().__init__(url)

    def search_vacancies(self, job_title: str, number_of_vacancies: int = 10) -> list:
        """
        Поиск вакансий на HeadHunter API.

        :param number_of_vacancies:
        :param job_title: Заголовок вакансии для поиска.
        :return: Список найденных вакансий.
        """
        params = {
            'text': job_title,
            'per_page': number_of_vacancies,
            'pages': 1,
            'page': 0,
            'only_with_salary': True
        }

        response = requests.get(url=self._base_url, params=params)
        response_json = response.json()

        vacancies = []

        for item in response_json.get("items", []):
            try:
                vacancy = Vacancy(title=self.get_title(item), url=self.get_url(item), salary=self.get_salary(item),
                                  pub_date=self.get_pub_date(item), requirements=self.get_requirements(item))
                vacancies.append(vacancy)
            except:
                pass

        return vacancies

    @staticmethod
    def get_title(vacancy) -> str:
        return vacancy['name']

    @staticmethod
    def get_url(vacancy) -> str:
        return vacancy['url']

    @staticmethod
    def get_salary(vacancy) -> dict:
        salary = {'min': int(vacancy['salary']['from']), 'currency': vacancy['salary']['currency']}
        if vacancy['salary']['to'] is None:
            salary['max'] = salary['min']
        else:
            salary['max'] = int(vacancy['salary']['from'])
        return salary

    @staticmethod
    def get_pub_date(vacancy) -> str:
        return str(datetime.fromisoformat(vacancy['published_at'][:10]).date())

    @staticmethod
    def get_requirements(vacancy) -> str:
        return vacancy['snippet']['requirement']