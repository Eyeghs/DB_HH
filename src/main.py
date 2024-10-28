from DB import DBManager
import psycopg2
from hh_api import Headhunter_API


if __name__ == "__main__":
    hh_api = Headhunter_API()
    db_manager = DBManager()
    db_manager.build_db()
    db_manager.create_tables()
    hh_api = Headhunter_API()
    conn = psycopg2.connect(dbname="headhunter", user='postgres', password='12345', host="127.0.0.1")
    cursor = conn.cursor()
    conn.autocommit = True
    db_manager.insert_vacancies()
    while True:
        user_input = input("""Это база данных вакансий на hh.ru. В приложении реализованы следующие функции:
1. Получить список компаний и количество вакансий для каждой компании;
2. Получить список всех вакансий;
3. Получить среднюю зарплату по вакансиям;
4. Получить список вакансий с заработной платой больше средней;
5. Получить список всех вакансий с ключевым словом.
Введите номер функции или нажмите Enter для выхода.
""")
        if user_input == "1":
            db_manager.get_companies_and_vacancies_count()
        elif user_input == "2":
            db_manager.get_all_vacancies()
        elif user_input == "3":
            db_manager.get_avg_salary()
        elif user_input == "4":
            db_manager.get_vacancies_with_higher_salary()
        elif user_input == "5":
            db_manager.get_vacancies_with_keyword(input("Введите ключевое слово: "))
        else:
            exit(0)
