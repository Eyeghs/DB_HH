import requests
from abc import ABC, abstractmethod


class AbstractClass_api_use(ABC):
    """
    Абстрактный класс для работы с api
    """
    @abstractmethod
    def get_vacancies(self, search_word: str):
        return search_word


class Headhunter_API(AbstractClass_api_use):
    """
    Класс для работы с api hh.ru
    """

    __url_headhunter = 'https://api.hh.ru/'

    def get_vacancies(self, employer_id: int) -> dict:
        response = requests.get(f'{self.__url_headhunter}/vacancies?employer_id={employer_id}&per_page=100')
        if response.status_code == 200:
            return response.json()
        return None
