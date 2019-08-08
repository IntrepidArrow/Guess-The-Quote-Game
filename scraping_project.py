import requests
from bs4 import BeautifulSoup

# http://quotes.toscrape.com
url = "http://quotes.toscrape.com/"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

# Getting all Quotes from current page and storing in a list
quotes = soup.find_all(class_="quote")
game_data = []
for quote in quotes:
    text = quote.find(class_="text").get_text()
    author = quote.find(class_="author").get_text()
    href = quote.find("a")["href"]
    
    author_data = [text, author, href]
    # Adding scraped information in list for game logic
    game_data.append(author_data)
