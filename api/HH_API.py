import json
from pprint import pprint
import requests


class HeadHunterAPI():

    def get_vacancies(self):
        url = "https://api.hh.ru"
        params = {
            "only_with_salary": 'true'
        }

        all_vacancies = []
        data = requests.get(f"{url}/vacancies", params=params).json()
        for vacancy in data['items']:

            company_name = vacancy.get("employer", {}).get("name", "Не указано")
            new_vacancy = {
                "name": vacancy.get("name", "Не указано"),
                "salary": vacancy.get("salary", "Не указано"),
                "url": vacancy.get("url", "Не указано"),
                "company_name": company_name
            }

            if len(all_vacancies) == 0:
                all_vacancies.append({"company_name": company_name, "vacancies": [new_vacancy]})
            else:
                is_found = False
                for vac in all_vacancies:
                    if company_name == vac['company_name']:
                        is_found = True
                if is_found:
                    for vac in all_vacancies:
                        if company_name == vac['company_name']:
                            vac['vacancies'].append(new_vacancy)
                else:
                    all_vacancies.append({"company_name": company_name, "vacancies": [new_vacancy]})


        for vacancy in data['items']:
            if vacancy['salary']['currency'] == 'BYR':
                if vacancy['salary']['from'] is not None:
                    vacancy['salary']['from'] *= 28
                elif vacancy['salary']['to'] is not None:
                    vacancy['salary']['to'] *= 28
                vacancy['salary']['currency'] = 'RUB'

            elif vacancy['salary']['currency'] == 'UZS':
                if vacancy['salary']['from'] is not None:
                    vacancy['salary']['from'] = int(vacancy['salary']['from'] * 0.0075)
                elif vacancy['salary']['to'] is not None:
                    vacancy['salary']['to'] = int(vacancy['salary']['from'] * 0.0075)
                vacancy['salary']['currency'] = 'RUB'

            elif vacancy['salary']['currency'] == 'KZT':
                if vacancy['salary']['from'] is not None:
                    vacancy['salary']['from'] *= 5
                elif vacancy['salary']['to'] is not None:
                    vacancy['salary']['to'] *= 5
                vacancy['salary']['currency'] = 'RUB'


        return all_vacancies


# uhfhf = HeadHunterAPI()
# pprint(uhfhf.get_vacancies())










