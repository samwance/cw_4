from src.vacancy import Vacancy
import json


class JSONFileHandler:
    """Класс для обработки файлов"""

    def add_vacancies(self, filename: str, vacancies: [Vacancy]) -> None:
        """
        Метод для добавления одной или нескольких вакансий в файл

        :param filename: Название файла.
        :param vacancies: Список вакансий для добавления
        """
        try:
            existing_vacancies = self.get_vacancies(filename=filename)
            for vacancy in vacancies:
                if vacancy not in existing_vacancies:
                    existing_vacancies.append(vacancy)
            vacancies_to_save = [vacancy.__dict__() for vacancy in existing_vacancies]
            with open(filename, "w", encoding="utf-8") as file:
                json.dump(vacancies_to_save, file, ensure_ascii=False, indent=2)

        except FileNotFoundError:
            vacancies_to_save = [vacancy.__dict__() for vacancy in vacancies]
            with open(filename, "x", encoding="utf-8") as file:
                json.dump(vacancies_to_save, file, ensure_ascii=False, indent=2)

    @staticmethod
    def get_vacancies(filename: str) -> [Vacancy]:
        """
        Метод для получения вакансий из файла

        :param filename: Название файла.
        :return: Список вакансий из заданного файла
        """
        vacancies = []
        with open(filename, "r", encoding="utf-8") as file:
            vacancies_data = json.load(file)
            for vacancy_data in vacancies_data:
                try:
                    vacancy = Vacancy(title=vacancy_data['title'], url=vacancy_data['url'],
                                      salary=vacancy_data['salary'], pub_date=vacancy_data['pub_date'],
                                      requirements=vacancy_data['requirements'])
                    vacancies.append(vacancy)
                except:
                    pass

        return vacancies
