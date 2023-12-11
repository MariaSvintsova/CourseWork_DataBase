from api.HH_API import HeadHunterAPI
from database_manager.DBmanager import DBManager


def main():
    print("Добрый день! Welcome to vacancies database!")
    keyword = input("Введите ключевое слово: ")

    manager = DBManager()
    print(manager.create_tables())
    print(manager.inserting_data(HeadHunterAPI().get_vacancies()))

    print("A list of all companies and the number of vacancies each company has: \n", manager.get_companies_and_vacancies_count())

    print("A list of all vacancies with all information of them: \n", manager.get_all_vacancies())
    print("The average salary for all of the vacancies: ", round(manager.get_avg_salary(), 2), "RUB")
    print("A list of all jobs with a salary higher than the average for all the vacancies: \n", manager.get_vacancies_with_higher_salary())
    print("A list of all vacancies whose titles contain your keyword: \n", manager.get_vacancies_with_keyword(keyword))

    manager.close_connection()


if __name__ == "__main__":
    main()