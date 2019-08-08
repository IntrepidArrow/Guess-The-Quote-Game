import requests
from bs4 import BeautifulSoup

url = "http://quotes.toscrape.com/"
game_data = [] # All quotes, author and author bio links will be here for game

while True:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Getting all Quotes from current page and storing in a list
    quotes = soup.find_all(class_="quote")
    for quote in quotes:
        text = quote.find(class_="text").get_text()
        author = quote.find(class_="author").get_text()
        href = quote.find("a")["href"]
        
        author_data = [text, author, href]
        # Adding scraped information in list for game logic
        game_data.append(author_data)

    # Navigation to next page 
    next_page_button = soup.find(class_="next")
    #if there is a next page then scrape the next page or else quit loop
    if next_page_button:
        next_page_link = next_page_button.find("a")["href"]
        url = f"http://quotes.toscrape.com/{next_page_link}"
    else:
        break

