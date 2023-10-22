import psycopg2

from src import settings


class DBManager:
    """Класс, который подключается к БД PostgreSQL"""

    def select_from_db(self, query: str, query_params: tuple):
        conn = psycopg2.connect(**settings.DB)
        try:
            with conn.cursor() as curs:
                curs.execute(query, query_params)
                result = curs.fetchall()
        finally:
            conn.close()
        return result

    def insert_to_db(self, query: str, query_params: tuple):
        conn = psycopg2.connect(**settings.DB)
        try:
            with conn.cursor() as curs:
                curs.execute(query, query_params)
                conn.commit()
        finally:
            conn.close()

    def get_company_by_id(self, id_):
        """Получает конкретную компанию по ID"""
        return self.select_from_db('SELECT * FROM employers WHERE id = %s', (id_,))

    def create_company(self, data):
        """Создает конкретную компанию по ID в таблицу"""
        self.insert_to_db('INSERT INTO employers(id, name, hh_url) VALUES(%s, %s, %s)', data)

    def get_vacancy_by_id(self, id_):
        """Получает конкретную вакансию по ID"""
        return self.select_from_db('SELECT * FROM vacancies WHERE id = %s', (id_,))

    def create_vacancy(self, data):
        """Создает конкретную вакансию по ID в таблицу"""
        self.insert_to_db('INSERT INTO vacancies('
                          'id, name, hh_url, area, employer_id, experience, salary_currency, salary_from, salary_to, requirement, created_at'
                          ') VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', data)

    def get_companies_and_vacancies_count(self):
        """Получает список всех компаний и количество вакансий у каждой компании."""
        return self.select_from_db('select employers.name, count(*) from vacancies '
                                   'INNER JOIN employers ON vacancies.employer_id = employers.id '
                                   'group by employers.name', ())

    def get_all_vacancies(self):
        """Получает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию."""
        return self.select_from_db(
            'select employers.name as employer_name, vacancies.name, vacancies.salary_from, vacancies.hh_url from vacancies '
            'INNER JOIN employers ON vacancies.employer_id = employers.id', ())

    def get_avg_salary(self):
        """Получает среднюю зарплату по вакансиям."""
        return self.select_from_db('select round(avg(salary_from),2) from vacancies', ())[0]

    def get_vacancies_with_higher_salary(self):
        """Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям."""
        return self.select_from_db('select name from vacancies '
                                   'where salary_from > (select avg(salary_from) from vacancies)', ())

    def get_vacancies_with_keyword(self, keyword: str):
        """Получает список всех вакансий, в названии которых содержатся переданные в метод слова,
        например python."""
        return self.select_from_db("select name, requirement from vacancies "
                                   "where lower(requirement) like %s", (keyword, ))
