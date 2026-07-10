import requests
from bs4 import BeautifulSoup

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

if __name__ == "__main__":
    ham_veriler = extract_data()
    print("Örnek 2 veri:")
    print(ham_veriler[:2])