Web Scraping & ETL Pipeline Project

This project demonstrates a complete, standalone Data Engineering workflow (ETL - Extract, Transform, Load) built entirely in Python. It extracts unstructured data from a web source, cleans and transforms it using Pandas, and loads it into an isolated PostgreSQL database running on Docker.

 🚀 Project Overview

1. **Extract (Web Scraping):** Uses `requests` and `BeautifulSoup4` to scrape book data (Title, Price, Rating) from a public, scrape-friendly e-commerce environment (books.toscrape.com).
2. **Transform (Data Cleaning):** Uses `Pandas` to clean the raw data. Currency symbols are stripped, strings are converted to `float`, missing values are dropped, and an execution timestamp is attached to each record.
3. **Load (Database Storage):** Connects to a Dockerized `PostgreSQL` database via `psycopg2` and dynamically inserts the cleaned Pandas DataFrame.
4. **Idempotency:** Implements an `ON CONFLICT DO UPDATE` SQL architecture to ensure that multiple executions update existing records rather than duplicating them.

🛠️ Tech Stack

* **Language:** Python
* **Data Transformation:** Pandas
* **Web Scraping:** BeautifulSoup4, Requests
* **Database:** PostgreSQL
* **Infrastructure:** Docker
* **Database Management:** DBeaver / pgAdmin

⚙️ How to Run Locally

1. Start the PostgreSQL Container
Ensure Docker is running on your machine, then spin up the database:
```bash
docker run --name etl-postgres -e POSTGRES_USER=hilal -e POSTGRES_PASSWORD=hilal -e POSTGRES_DB=etl_db -p 5433:5432 -d postgres

(Note: Port 5433 is used on the host to prevent conflicts with local PostgreSQL installations).

2. Install Dependencies
Bash
pip install requests beautifulsoup4 pandas psycopg2-binary
3. Execute the Pipeline
Run the main script to trigger the ETL process:

Bash
python etl_pipeline.py
📊 Execution Logging
Upon successful execution, the script will output a summary to the console verifying the number of rows scraped, transformed, and loaded successfully into the database.
