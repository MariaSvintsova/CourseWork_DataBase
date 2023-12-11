import psycopg2
from api.HH_API import HeadHunterAPI
from database_manager.implemented import host, database, password, user


class DBManager():
    """
      Класс для управления базой данных, включая создание таблиц, вставку данных и выполнение запросов.

      Атрибуты:
          conn: Объект соединения с базой данных.
          cur: Объект курсора для выполнения SQL-запросов.

      Методы:
          __init__(): Инициализация объекта DBManager, устанавливает соединение с базой данных.
          create_tables(): Создание таблиц в базе данных.
          inserting_data(data): Вставка данных о компаниях и вакансиях в базу данных.
          get_companies_and_vacancies_count(): Получение количества вакансий для каждой компании.
          get_all_vacancies(): Получение всех вакансий с указанием компании.
          get_avg_salary(): Получение средней зарплаты для вакансий.
          get_vacancies_with_higher_salary(): Получение вакансий с зарплатой выше средней.
          get_vacancies_with_keyword(keyword): Получение вакансий по ключевому слову в названии.

    """

    def __init__(self):
        """
        Инициализация объекта DBManager.

        Устанавливает соединение с базой данных и создает курсор для выполнения SQL-запросов.

        """
        self.conn = psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password
        )
        self.cur = self.conn.cursor()

    def create_tables(self):
        """
        Создание таблиц в базе данных.

        Удаляет существующие таблицы и создает новые таблицы companies и vacancies.

        """
        self.cur.execute("""
        DROP TABLE IF EXISTS companies CASCADE;
        DROP TABLE IF EXISTS vacancies CASCADE;
        
        CREATE TABLE companies(
            company_id SERIAL PRIMARY KEY,
            company_name text UNIQUE NOT NULL
        );
        
        CREATE TABLE vacancies(
            vacancy_id SERIAL PRIMARY KEY,
            company_id int REFERENCES companies(company_id) NOT NULL,
            vacancy_name varchar(250),
            salary_to int,
            salary_from int,
            currency text
        );
        """)
        self.conn.commit()
        return "## БАЗА ДАННЫХ СОЗДАНА ## "

    def inserting_data(self, data):
        """
        Вставка данных о компаниях и вакансиях в базу данных.

        Принимает данные в формате словаря и вставляет их в таблицы companies и vacancies.

        """
        for dict in data:
            company_name = dict['company_name']
            vacancies = dict['vacancies']

        # Вставка данных в таблицу "companies"
            self.cur.execute("INSERT INTO companies (company_name) VALUES (%s) ON CONFLICT (company_name) DO NOTHING", (company_name,))
            self.conn.commit()

            # Получение id компании
            self.cur.execute("SELECT company_id FROM companies WHERE company_name = %s", (company_name,))
            company_id = self.cur.fetchone()[0]

            # Выделение всех характеристик вакансий
            for vac in vacancies:
                vacancy_name = vac.get('name')
                if vacancy_name is None:
                    vacancy_name = ""
                salary_to = vac['salary']['to']
                salary_from = vac['salary']['from']
                currency = vac['salary']['currency']
                link = vac.get('url')

            # Вставка данных в таблицу "vacancies"
                self.cur.execute('INSERT INTO vacancies (company_id, vacancy_name, salary_to, salary_from, currency) VALUES (%s, %s, %s, %s, %s)',
                             (company_id, vacancy_name, salary_to, salary_from, currency))
                self.conn.commit()
        return "## База данных заполнена ## "

    def get_companies_and_vacancies_count(self):
        """
        Получение количества вакансий для каждой компании.

        Возвращает список кортежей с информацией о компаниях и их количестве вакансий.

        """
        self.cur.execute("""
        SELECT companies.company_id, companies.company_name, COUNT(vacancies.vacancy_id) 
        FROM companies 
        LEFT JOIN vacancies ON companies.company_id = vacancies.company_id 
        GROUP BY companies.company_id, companies.company_name;
        """)
        return self.cur.fetchall()

    def get_all_vacancies(self):
        """
        Получение всех вакансий с указанием компании.

        Возвращает список кортежей с информацией о компаниях и соответствующих вакансиях.

        """
        self.cur.execute("""
        SELECT DISTINCT v.vacancy_id, c.company_name, v.vacancy_name, v.salary_to, v.salary_from
        FROM vacancies v
        LEFT JOIN companies c ON c.company_id = v.company_id        
        """)
        return self.cur.fetchall()

    def get_avg_salary(self):
        """
        Получение средней зарплаты для вакансий.

        Возвращает среднюю зарплату в виде списка кортежей.

        """
        self.cur.execute("""
        SELECT AVG((COALESCE(salary_from, 0) + COALESCE(salary_to, 0))) AS average_salary
        FROM vacancies
        """)
        return self.cur.fetchall()[0][0]

    def get_vacancies_with_higher_salary(self):
        """
        Получение вакансий с зарплатой выше средней.

        Возвращает список кортежей с информацией о компаниях и соответствующих вакансиях.

        """
        try:
            self.cur.execute("""
            SELECT DISTINCT company_name, vacancy_name, salary_to, salary_from, currency
            FROM vacancies v
            JOIN companies c ON v.company_id = c.company_id
            WHERE v.salary_to > %s OR v.salary_from > %s;
            """, (self.get_avg_salary(), self.get_avg_salary()))
            return self.cur.fetchall()
        except:
            return []


    def get_vacancies_with_keyword(self, keyword):
        """
        Получение вакансий по ключевому слову в названии.

        Принимает ключевое слово и возвращает список кортежей с информацией о компаниях и соответствующих вакансиях.

        """
        self.cur.execute("""
        SELECT DISTINCT vacancy_id, company_name, vacancy_name, salary_to, salary_from, currency
        FROM vacancies v
        JOIN companies c ON v.company_id = v.company_id
        WHERE v.vacancy_name LIKE %s
        """, (f'%{keyword}%',))
        return self.cur.fetchall()


    def close_connection(self):
        """
        Закрытие соединения с базой данных.

        Закрывает курсор и соединение с базой данных.

        """
        self.cur.close()
        self.conn.close()

# manager = DBManager()
# print(manager.create_tables()) # works good
# manager.inserting_data(HeadHunterAPI().get_vacancies())  # works good
# print(manager.get_companies_and_vacancies_count()) # works good
# print(manager.get_all_vacancies()) # works good
# print(round(manager.get_avg_salary(), 2)) # works good
# print(manager.get_vacancies_with_higher_salary()) # works good
# print(manager.get_vacancies_with_keyword('Менеджер')) # works good

