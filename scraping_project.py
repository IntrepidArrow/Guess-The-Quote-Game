import requests
from bs4 import BeautifulSoup
from random import choice

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


def display_message(choice_quote, num_of_lives):
    # Get author io page link to navigate for hints
    author_bio_link = choice_quote["about"]
    bio_response = requests.get(f"{main_url}{author_bio_link}")
    bio_soup = BeautifulSoup(bio_response.text, "html.parser")

    #Getting details to build hints
    birth_date = bio_soup.find(class_="author-born-date").get_text()
    birth_location = bio_soup.find(class_="author-born-location").get_text()

    author_name_split = (choice_quote["author"]).split()
    first_initial = author_name_split[0][0]
    last_initial = author_name_split[-1][0]

    if num_of_lives == 3:
        return "Author was born on " + birth_date + " " + birth_location
    elif num_of_lives == 2:
        return "Author's first name initial is: " + first_initial
    elif num_of_lives == 1:
        return "Author's last name initial is: " + last_initial
    else:
        return "You are all out of guesses :(\nThe correct answer is " + choice_quote["author"] + "\n"


def run_game():
    game_data = scrape_quote_data(main_url)
    num_of_lives = 4

    random_quote = choice(game_data)
    print("Who said the following words!: \n")
    print(random_quote["quote"] + "\n")

    while True:
        user_input = input("Who said this? Guesses remaining: " +
                        str(num_of_lives) + ". ")

        if user_input.lower() == (random_quote["author"]).lower():
            print("Congratulations! You guessed correct! The above words were indeed said by " +
                random_quote["author"] + "\n")
            break
        else:
            num_of_lives -= 1
            if num_of_lives == 0:
                print("\n" + display_message(random_quote, 0))
                break
            print("Incorrect. Here's a hint: " +
                display_message(random_quote, num_of_lives) + "\n")


# Playing game!
run_game()


