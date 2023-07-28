from abc import ABC, abstractmethod
from src.vacancy import Vacancy


class BaseFileHandler(ABC):
    """Абстрактный базовый класс для обработки файлов"""

    @abstractmethod
    def add_vacancy(self, vacancy: Vacancy, filename: str) -> None:
        """
        Абстрактный метод для добавления вакансии в файл.

        :param filename: Название файла.
        :param vacancy: Вакансия для добавления.
        """
        pass

    @abstractmethod
    def get_vacancies(self, filename: str) -> [Vacancy]:
        """
        Абстрактный метод для получения вакансий из файла

        :param filename: Название файла.
        :return: Список вакансий из заданного файла
        """
        pass