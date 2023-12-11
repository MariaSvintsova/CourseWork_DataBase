# HeadHunter Vacancies Parser

My project is designed to fetch and organize job vacancies using the HeadHunter API. The collected data is categorized by companies, and salaries are converted to Russian rubles. All parsed information is stored in a PostgreSQL database managed by pgAdmin4.

## Dependencies
**The project relies on the following Python packages:**

- requests: For making HTTP requests to the HeadHunter API.
- psycopg2: For connecting to and interacting with the PostgreSQL database.
- other_dependency: [Description of the dependency, if applicable]

## Reviewing Results
Check the parsed results by examining the entries in the PostgreSQL database. You can use pgAdmin4 to conveniently view and query the stored data.

## Project Structure
- main.py: The main script for initiating the parsing process and handling data.
- DBmanager.py: A module for interacting with the PostgreSQL database.
- HH_API: A module for interfacing with the HeadHunter API.
- requirements.txt: The file containing the project's dependencies.

**That's all :)**