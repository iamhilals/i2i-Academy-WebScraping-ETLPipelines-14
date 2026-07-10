import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import psycopg2
from psycopg2.extras import execute_values

def extract_data():
    print("1. Adım: Veriler web sitesinden çekiliyor (Extract)...")
    url = "https://books.toscrape.com/"
    response = requests.get(url)
    
    soup = BeautifulSoup(response.content, "html.parser")
    books = soup.find_all("article", class_="product_pod")
    
    raw_data = []
    
    for book in books:
        title = book.h3.a["title"]
        price = book.find("p", class_="price_color").text
        rating = book.p["class"][1]
        
        raw_data.append({
            "Title": title,
            "Price": price,
            "Rating": rating
        })
        
    print(f"Başarılı! Toplam {len(raw_data)} adet kitap verisi çekildi.\n")
    return raw_data

def transform_data(raw_data):
    print("2. Adım: Veriler Pandas ile temizleniyor (Transform)...")
    df = pd.DataFrame(raw_data)
    
    df['Price'] = df['Price'].str.replace('£', '').astype(float)
    df.dropna(inplace=True)
    df['Execution_Timestamp'] = datetime.now()
    
    print("Başarılı! Veriler temizlendi, fiyatlar float tipine çevrildi ve timestamp eklendi.\n")
    return df

def load_data(df):
    print("3. Adım: Veriler PostgreSQL veritabanına yükleniyor (Load)...")
    
    conn_params = {
        "host": "localhost",
        "port": 5433,
        "database": "etl_db",
        "user": "hilal",
        "password": "hilal"
    }
    
    try:
        conn = psycopg2.connect(**conn_params)
        cursor = conn.cursor()
        
        create_table_query = """
        CREATE TABLE IF NOT EXISTS scraped_books (
            id SERIAL PRIMARY KEY,
            title VARCHAR(255) UNIQUE,
            price FLOAT,
            rating VARCHAR(50),
            execution_timestamp TIMESTAMP
        );
        """
        cursor.execute(create_table_query)
        
        data_tuples = [tuple(x) for x in df.to_numpy()]
        
        insert_query = """
        INSERT INTO scraped_books (title, price, rating, execution_timestamp)
        VALUES %s
        ON CONFLICT (title) 
        DO UPDATE SET 
            price = EXCLUDED.price,
            rating = EXCLUDED.rating,
            execution_timestamp = EXCLUDED.execution_timestamp;
        """
        
        execute_values(cursor, insert_query, data_tuples)
        conn.commit()
        
        inserted_rows = len(df)
        print("Başarılı! Veriler veritabanına başarıyla aktarıldı.\n")
        
        cursor.close()
        conn.close()
        return inserted_rows
        
    except Exception as e:
        print(f"Veritabanı hatası: {e}")
        return 0

if __name__ == "__main__":
    print("--- ETL Pipeline Başlatılıyor ---\n")
    
    ham_veriler = extract_data()
    scraped_count = len(ham_veriler)
    
    temiz_df = transform_data(ham_veriler)
    transformed_count = len(temiz_df)
    
    inserted_count = load_data(temiz_df)
    
    print("--- ETL Süreci Tamamlandı Özeti ---")
    print(f"Çekilen Satır Sayısı (Scraped)     : {scraped_count}")
    print(f"Temizlenen Satır Sayısı (Transformed): {transformed_count}")
    print(f"DB'ye İşlenen Satır Sayısı (Loaded)  : {inserted_count}")
    print("-----------------------------------\n")