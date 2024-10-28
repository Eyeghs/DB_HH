import psycopg2
from hh_vacancy import HHvacancy
from hh_api import Headhunter_API


class DBManager:
    """
    Класс для работы с базой данных
    """
    def __init__(self):
        pass

    def build_db(self):
        """
        Метод для создания базы данных
        """
        conn = psycopg2.connect(dbname="postgres", user='postgres', password='12345', host="127.0.0.1")
        cursor = conn.cursor()
        conn.autocommit = True
        cursor.execute("SELECT 1 FROM pg_database WHERE datname='headhunter'")
        if cursor.fetchone():
            print('Такая база данных уже есть. Перехожу в нее.')
            return None
        cursor.execute("CREATE DATABASE headhunter")
        print("База данных успешно создана")
        cursor.close()
        conn.close()

    def create_tables(self):
        """
        Метод для создания таблиц
        """
        conn = psycopg2.connect(dbname="headhunter", user='postgres', password='12345', host="127.0.0.1")
        cursor = conn.cursor()
        conn.autocommit = True
        cursor.execute("DROP TABLE IF EXISTS companies CASCADE")
        cursor.execute("DROP TABLE IF EXISTS vacancies CASCADE")
        cursor.execute("""CREATE TABLE companies
                    (
                        id integer PRIMARY KEY,
                        company_name varchar(100) UNIQUE NOT NULL,
                        vacancies_count integer
                    );
                    INSERT INTO companies (company_name, id) VALUES
                        ('Black Star', 748940),
                        ('Sports', 223566),
                        ('Rambler&Co', 8620),
                        ('ВЕРТЕКС', 1800569),
                        ('Иви', 136929),
                        ('Okko', 1375441),
                        ('Москвариум', 1383228),
                        ('Онлайн-школа Фоксфорд', 5744540),
                        ('Сеть кинотеатров Синема Парк и Формула Кино', 75380),
                        ('РБК', 563765);
                    """)
        cursor.execute("""CREATE TABLE vacancies
                    (
                        vacancy_id serial PRIMARY KEY,
                        company_id integer NOT NULL,
                        vacancy_name varchar(100) NOT NULL,
                        salary integer,
                        url varchar(100) NOT NULL
                        );
                    """)
        cursor.execute("ALTER TABLE vacancies ADD CONSTRAINT fk_vacancies_company_name FOREIGN KEY (company_id) REFERENCES companies(id)")
        print('Таблицы созданы.')
        cursor.close()
        conn.close()

    def insert_vacancies(self):
        """
        Метод для вставки вакансий в таблицы
        """
        hh_api = Headhunter_API()
        conn = psycopg2.connect(dbname="headhunter", user='postgres', password='12345', host="127.0.0.1")
        cursor = conn.cursor()
        companies_list = []
        conn.autocommit = True
        cursor.execute("SELECT id FROM companies")
        companies = cursor.fetchall()
        for company in companies:
            vacancies_company = hh_api.get_vacancies(company[0])
            companies_list.append(len(vacancies_company['items']))
            vacancies_list = HHvacancy.make_vacancy(vacancies_company)
            for vacancy in vacancies_list:
                cursor.execute("INSERT INTO vacancies (company_id, vacancy_name, salary, url) VALUES (%s, %s, %s, %s)", (company[0], vacancy._Vacancy__name, vacancy._Vacancy__salary, vacancy._Vacancy__url))
        cursor.close()
        conn.close()

    def get_companies_and_vacancies_count(self):
        """
        Метод для получения компаний и количества вакансий
        """
        conn = psycopg2.connect(dbname="headhunter", user='postgres', password='12345', host="127.0.0.1")
        cursor = conn.cursor()
        conn.autocommit = True
        cursor.execute("""SELECT company_name, COUNT(*) as vacancies_count 
                       FROM companies 
                       INNER JOIN vacancies ON companies.id = vacancies.company_id
                       GROUP BY company_name
                       """)
        companies = cursor.fetchall()
        cursor.close()
        conn.close()
        for company in companies:
            print(f"{company[0]}, {company[1]}")
        return companies

    def get_all_vacancies(self):
        """
        Метод для получения всех вакансий
        """
        conn = psycopg2.connect(dbname="headhunter", user='postgres', password='12345', host="127.0.0.1")
        cursor = conn.cursor()
        conn.autocommit = True
        cursor.execute("""SELECT companies.company_name, vacancy_name, salary, url
                       FROM vacancies
                       INNER JOIN companies ON companies.id = vacancies.company_id
                       """)
        vacancies = cursor.fetchall()
        cursor.close()
        conn.close()
        for vacancy in vacancies:
            print(f"{vacancy[0]}, {vacancy[1]}, {vacancy[2]}, {vacancy[3]}")
        return vacancies

    def get_avg_salary(self):
        """
        Метод для получения средней зарплаты
        """
        conn = psycopg2.connect(dbname="headhunter", user='postgres', password='12345', host="127.0.0.1")
        cursor = conn.cursor()
        conn.autocommit = True
        cursor.execute("SELECT AVG(salary) FROM vacancies")
        avg = cursor.fetchall()
        cursor.close()
        conn.close()
        print(f"Средняя зарплата - {float(avg[0][0])}")
        return float(avg[0][0])

    def get_vacancies_with_higher_salary(self):
        """
        Метод для получения вакансий с зарплатой выше средней
        """
        conn = psycopg2.connect(dbname="headhunter", user='postgres', password='12345', host="127.0.0.1")
        cursor = conn.cursor()
        conn.autocommit = True
        cursor.execute("""SELECT company_name, vacancy_name, salary, url
                       FROM vacancies
                       INNER JOIN companies ON companies.id = vacancies.company_id
                       WHERE salary > (SELECT AVG(salary) FROM vacancies)
                       GROUP BY company_name, vacancy_name, salary, url
                       ORDER BY company_name
                       """)
        vacancies = cursor.fetchall()
        cursor.close()
        conn.close()
        for vacancy in vacancies:
            print(f"{vacancy[0]}, {vacancy[1]}, {vacancy[2]}, {vacancy[3]}")
        return vacancies

    def get_vacancies_with_keyword(self, keyword):
        """
        Метод для получения вакансий по ключевому слову
        """
        conn = psycopg2.connect(dbname="headhunter", user='postgres', password='12345', host="127.0.0.1")
        cursor = conn.cursor()
        conn.autocommit = True
        cursor.execute(f"SELECT company_name, vacancy_name, salary, url FROM vacancies WHERE LOWER(vacancy_name) LIKE LOWER('%{keyword}%')")
        vacancies = cursor.fetchall()
        cursor.close()
        conn.close()
        for vacancy in vacancies:
            print(f"{vacancy[0]}, {vacancy[1]}, {vacancy[2]}, {vacancy[3]}")
        return vacancies
