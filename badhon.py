import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

base_url = "https://books.toscrape.com/catalogue/page-{}.html"

data = []

for page in range(1, 51):
    url = base_url.format(page)

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    books = soup.select("article.product_pod")

    for book in books:
        title = book.h3.a["title"]
        price = book.select_one(".price_color").text.strip()
        availability = book.select_one(".availability").text.strip()
        rating = book.p["class"][1]

        data.append({
            "title": title,
            "price": price,
            "availability": availability,
            "rating": rating
        })

    print(f"Page {page} completed")
    time.sleep(1)

df = pd.DataFrame(data)

df.to_csv("books_dataset.csv", index=False)

print("Total records:", len(df))
print(df.head())