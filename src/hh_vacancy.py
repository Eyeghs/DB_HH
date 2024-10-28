class Vacancy:
    """
    Класс для работы с вакансиями.
    """
    def __init__(self, name: str, salary: int, url: str, company_name: str):
        self.__name = name
        self.__salary = salary
        self.__url = url
        self.__company_name = company_name

    def __repr__(self) -> str:
        return f"Вакансия: {self.__name}\nЗарплата: {self.__salary}\nСсылка: {self.__url}\nНазвание компании: {self.__company_name}\n"

    def __str__(self) -> str:
        return f"Вакансия: {self.__name}\nЗарплата: {self.__salary}\nСсылка: {self.__url}\nНазвание компании: {self.__company_name}\n"

    def __lt__(self, other) -> bool:
        return self.__salary < other.__salary

    def __gt__(self, other) -> bool:
        return self.__salary > other.__salary

    def __le__(self, other) -> bool:
        return self.__salary <= other.__salary

    def __ge__(self, other) -> bool:
        return self.__salary >= other.__salary

    def __iter__(self):
        self.value = 0
        return self

    def __next__(self):
        if self.value < self.count:
            self.value += 1
        else:
            raise StopIteration


class HHvacancy(Vacancy):
    """
    Класс для работы с вакансиями с сайта hh.ru.
    """
    def __init__(self, name, salary, url, company_name):
        super().__init__(name, salary, url, company_name)
        self.company_name = company_name

    @classmethod
    def make_vacancy(cls, data):
        """
        Метод для создания списка вакансий с сайта hh.ru.
        """
        cls.vacancies_list = []
        for item in data['items']:
            hh_name = item['name']
            hh_url = item.get('alternate_url')
            hh_company_name = item['employer']['name']
            try:
                hh_salary = item['salary'].get('from')
                if hh_salary is None:
                    hh_salary = 0
            except AttributeError:
                hh_salary = 0
            cls.vacancies_list.append(HHvacancy(hh_name, hh_salary, hh_url, hh_company_name))
        return cls.vacancies_list
