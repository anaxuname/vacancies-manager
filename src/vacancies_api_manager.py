import requests

from src import settings


class APIManager:

    def get_vacancies(self):
        r = self.load_vacancies()
        pages = r.get('pages')
        items = r.get('items')
        for i in range(pages):
            r = self.load_vacancies(i+1)
            items += r.get('items')
        return items

    def load_vacancies(self, page=0):
        url = settings.HH_URL + '/vacancies'
        params = {
            "employer_id": settings.employer_ids,
            "per_page": 100,
            "page": page,
        }
        result = requests.get(url, params=params)
        return result.json()
