import requests
from bs4 import BeautifulSoup
import pandas as pd

data = []

base_url = "http://books.toscrape.com/catalogue/page-{}.html"

for page in range(1, 6):
    url = base_url.format(page)
    
    response = requests.get(url)
    
    # DEBUG
    print("Page:", page, "Status:", response.status_code)
    
    soup = BeautifulSoup(response.text, "html.parser")
    
    books = soup.find_all("article", class_="product_pod")
    
    print("Books found:", len(books))  # DEBUG
    
    for book in books:
        title = book.h3.a["title"]
        price = book.find("p", class_="price_color").text
        rating = book.p["class"][1]
        
        data.append({
            "Title": title,
            "Price": price,
            "Rating": rating
        })

print("Total data:", len(data))

df = pd.DataFrame(data)
df.to_csv("books_output.csv", index=False)

print("✅ Done! Check books_output.csv")