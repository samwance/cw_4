from src.vacancy import Vacancy
from src.apis.hh_api import HeadHunterAPI
from src.apis.sj_api import SuperJobAPI
from src.file_handler.file_handler import JSONFileHandler


class ParserApp:
    def __init__(self):
        self.__vacancies: list['Vacancy'] = []
        self.__job_title: str | None = None
        self.__amount_vacancy: int | None = None
        self.__available_sites = {'1': 'HeadHunter', '2': 'SuperJob'}
        self.__site_to_parse = None
        self.__file_handler = JSONFileHandler()

    def interact_with_user(self) -> None:
        """ Взаимодействие с пользователем. """
        while True:
            print("\n1. Поиск вакансий\n2. Отобразить вакансии\n3. Сохранить вакансии в файл\n"
                  "4. Импортировать вакансии из файла\n5. Выход")
            choice_menu = input("Выберите действие: ")

            if choice_menu == "1":
                self.search_vacancies()
                self.sort_vacancies()

            elif choice_menu == "2":
                self.display_vacancies()

            elif choice_menu == "3":
                self.save_vacancies_to_file()

            elif choice_menu == "4":
                self.import_vacancies_from_file()

            elif choice_menu == "5":
                break
            else:
                print("Ошибка ввода")

    def search_vacancies(self) -> None:
        """Собирает вакансии по выбранным критериям"""

        while True:
            job_title = input("\nВведите должность для поиска: ")
            if job_title:
                self.__job_title = job_title
                break
            else:
                print("Ошибка ввода")

        while True:
            amount_vacancy = input("\nВведите количество вакансий для поиска: ")
            if amount_vacancy.isdigit():
                self.__amount_vacancy = int(amount_vacancy)
                break
            else:
                print("Ошибка ввода")

        self.choose_platform()

        self.__vacancies = self.__site_to_parse.search_vacancies(job_title=self.__job_title,
                                                                 number_of_vacancies=self.__amount_vacancy)

    def choose_platform(self) -> None:
        """Выбор онлайн-платформы"""

        while True:
            print("\nДоступные платформы:")
            for number, site in self.__available_sites.items():
                print(f"{number}. {site}")
            site_to_parse = input("Выберите платформу: ")
            if site_to_parse == '1':
                self.__site_to_parse = HeadHunterAPI()
                break
            elif site_to_parse == '2':
                self.__site_to_parse = SuperJobAPI()
                break
            else:
                print("Ошибка ввода")

    def sort_vacancies(self) -> None:
        """Сортировка вакансий по выбранным критериям"""

        while True:
            print("""\n1. Сортировка по дате\n2. Сортировка по окладу""")
            choice_sorted = input("Выберите сортировку: ")
            if choice_sorted == "1":
                self.sort_vacancies_by_date()
                break
            elif choice_sorted == "2":
                self.sort_vacancies_by_salary()
                break
            else:
                print("Ошибка ввода")

    def filter_vacancies_by_keyword_in_requirements(self, keyword) -> None:
        """Фильтрация вакансий по названию профессии"""
        self.__vacancies = list(filter(lambda x: keyword.lower() in x.requirements.lower(),
                                       self.__vacancies))

    def sort_vacancies_by_salary(self) -> None:
        """Сортировка вакансий по окладу."""
        self.__vacancies = sorted(self.__vacancies, key=lambda x: x.medium_salary, reverse=True)

    def sort_vacancies_by_date(self) -> None:
        """Сортировка вакансий по дате публикации."""
        self.__vacancies = sorted(self.__vacancies, key=lambda x: x.pub_date, reverse=True)[
                           :self.__amount_vacancy]

    def display_vacancies(self) -> None:
        """Отображение вакансий"""
        if self.__vacancies:
            for vacancy in self.__vacancies:
                print(vacancy)
            self.filter_vacancies()
        else:
            print("\nНет доступных вакансий.")

    def filter_vacancies(self) -> None:
        """Фильтрует вакансии по ключевому слову"""

        while True:
            print("\n1. Отфильтровать вакансии\n2. Оставить как есть")
            choice_filter = input('Выберите действие: ')
            if choice_filter == "1":
                keyword = input("Введите ключевое слово: ")
                self.filter_vacancies_by_keyword_in_requirements(keyword)
                break
            elif choice_filter == "2":
                break
            else:
                print("Ошибка ввода")

    def save_vacancies_to_file(self) -> None:
        """Сохраняет вакансии в файл"""

        if self.__vacancies:
            filename = input("\nВведите название файла: ")
            self.__file_handler.add_vacancies(vacancies=self.__vacancies, filename=filename)
            print("\nВакансии сохранены в файл.")
        else:
            print("\nНет доступных вакансий для сохранения.")

    def import_vacancies_from_file(self):
        try:
            filename = input("\nВведите название файла: ")
            self.__vacancies = self.__file_handler.get_vacancies(filename=filename)
        except FileNotFoundError:
            print("Файла не существует")