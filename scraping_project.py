import requests
from bs4 import BeautifulSoup

# http://quotes.toscrape.com
url = "http://quotes.toscrape.com/page/1/"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

quote = soup.find(class_="quote")
text = quote.find(class_="text").get_text()
author = quote.find(class_="author").get_text()
href = quote.find("a")["href"]
print(text)
print(author)
print(href)