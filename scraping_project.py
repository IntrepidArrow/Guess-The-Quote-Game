import requests
from bs4 import BeautifulSoup

main_url = "http://quotes.toscrape.com/"

def scrape_quote_data(url):
    """Mehtod returns quote, author of the quote and link to author bio 
    in a list of lists, for all quotes in the website"""

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
            url = f"http://quotes.toscrape.com/{next_page_link}"
        else:
            break
    
    return game_data

# Game Logic
# Select random quote from the list
# Ask user to guess the person who said it - check against the quote author
# If correct:
#   Victory message and ask to play the game again 
# If wrong:
#   Reduce 1 life, provide hint for quote and ask user input for author name again
# If number of lives remaining is 0:
#   End the game and display the current answer
#   Defeat message
#   Ask user for another game
# Hints list:
# 1 - Author birth date and location
# 2 - Number of letters in their first and last name
# 3 - Author first and last name initials #

