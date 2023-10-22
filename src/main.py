from src.dbmanager import DBManager
from src.vacancies_api_manager import APIManager


def fill_db():
    """Функция по сбору данных о вакансиях"""
    api = APIManager()
    vacs = api.get_vacancies()
    dbm = DBManager()
    for vac in vacs:
        employer = vac['employer']
        salary = vac['salary']
        if not salary:
            salary_currency = None
            salary_from = None
            salary_to = None
        else:
            salary_currency = salary['currency']
            salary_from = salary['from']
            salary_to = salary['to']
        if not vac['snippet']['requirement']:
            requirement = ''
        else:
            requirement = vac['snippet']['requirement']
        if dbm.get_company_by_id(int(employer['id'])) == []:
            dbm.create_company((int(employer['id']), employer['name'], employer['alternate_url']))
        if dbm.get_vacancy_by_id(int(vac['id'])) == []:
            dbm.create_vacancy(
                (int(vac['id']), vac['name'], vac['alternate_url'], vac['area']['name'], int(employer['id']),
                 vac['experience']['name'], salary_currency, salary_from,
                 salary_to, requirement, vac['created_at']))


def main():
    """Основное поведение программы"""
    fill_db()
    dbm = DBManager()
    for company in dbm.get_companies_and_vacancies_count():
        print(*company)

    for vacancy in dbm.get_all_vacancies():
        print(*vacancy, sep=', ')

    print(*dbm.get_avg_salary())

    for vacancy in dbm.get_vacancies_with_higher_salary():
        print(*vacancy)

    keyword = input("Enter keyword: ")
    for vacancy in dbm.get_vacancies_with_keyword(f'%{keyword.lower()}%'):
        print(*vacancy)


if __name__ == "__main__":
    main()
