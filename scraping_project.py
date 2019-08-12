import requests
from bs4 import BeautifulSoup
from random import choice
from csv import DictReader
import os.path

main_url = "http://quotes.toscrape.com/"

def readfile(filename):
    cwd = os.getcwd()
    file_status = os.path.exists(cwd + "\\" + filename)
  
    if not file_status: # Make file in the current directory if it does not exist
        try:
            import scrapNstore
        except ImportError:
            print("Something went wrong when trying to scrape and create data_file. Try Again.")
    
    with open(file=filename, mode="r", encoding="utf-8") as csvfile:
        reader = DictReader(csvfile)
        return list(reader)

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


def run_game(game_data): 

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


if __name__ == "__main__":
    file = readfile("quotes_data.csv")
    run_game(game_data=file)



