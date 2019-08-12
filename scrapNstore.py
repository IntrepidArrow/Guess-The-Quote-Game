import requests
from bs4 import BeautifulSoup
from csv import DictWriter

main_url = "http://quotes.toscrape.com/"

def scrape_quote_data(url):
    """Mehtod returns quote, author of the quote and link to author bio 
    in a list of lists, for all quotes in the website"""
    count = 1
    game_data = []  # All quotes, author and author bio links will be here for game
    while True:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        # Getting all Quotes from current page and storing in a list
        quotes = soup.find_all(class_="quote")
        for quote in quotes:
            text = quote.find(class_="text").get_text()
            author = quote.find(class_="author").get_text()
            href = quote.find("a")["href"]

            author_data = {"quote": text, "author": author, "about": href}
            # Adding scraped information in list for game logic
            game_data.append(author_data)

        # Navigation to next page
        next_page_button = soup.find(class_="next")
        #if there is a next page then scrape the next page or else quit loop
        if next_page_button:
            next_page_link = next_page_button.find("a")["href"]
            url = f"{main_url}{next_page_link}"
        else:
            break

    return game_data

quotes_data = scrape_quote_data(url=main_url)

# Make CSV file and store all info about scraped quotes
def write_file():
    with open("quotes_data.csv", "w", encoding="utf-8") as csvfile:
        file_headers = ["quote", "author", "about"]
        writer = DictWriter(csvfile, fieldnames=file_headers)
        writer.writeheader()

        for quote in quotes_data:
            writer.writerow(quote)