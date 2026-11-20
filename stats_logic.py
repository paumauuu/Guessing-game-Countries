import math
import streamlit as st
from countries import countries

def hint_fits(hint, country): #basic function that tells you whether hint fits a country
    data = countries[country]

    hint_type = hint["kind"]

    if hint_type == "continent": #tests for continents if wanted = guessed
        wanted_continent = hint["value"]
        actual_continent = data["continent"]
        return actual_continent == wanted_continent

    if hint_type == "letter": #tests for letters if wanted = guessed
        wanted_letter = hint["value"].upper()
        country_name_upper = country.upper()
        return wanted_letter in country_name_upper

    stat_name = hint_type #this part is for numbers, divides in to above and not above then compares based on that in the if-else statement below
    actual_number = data[stat_name]
    limit_number = hint["limit"]
    must_be_above = hint["above"]

    if must_be_above:
        return actual_number >= limit_number
    else:
        return actual_number < limit_number

def check_hints(hint_list, guess): #cycles through hints for one country (the guess)
    results = []
    for hint in hint_list:
        results.append(hint_fits(hint, guess))
    return results

def judge_guess(index, hint_results): #rates a guess based on if it fits all the hints or only some/none
    if all(hint_results):
        return "Good"

    if any(hint_results):
        return "Okay"

    return "Bad"

# make sure we have games (list of finished games) in the session state
def init_state():
    if "games" not in st.session_state:
        st.session_state["games"] = []


def record_game(country, hints, jokers, won, hint_checks): #record a finished game, to work with it and save it in to the list
    init_state()

    labels = [] #label the guesses as good, okay or bad
    for i in range(len(hint_checks)):
        results = hint_checks[i]
        labels.append(judge_guess(i, results))

    game = {
        "country": country,
        "guesses": len(hint_checks),
        "hints": hints,
        "jokers": jokers,
        "labels": labels,
        "hint_checks": list(hint_checks),
        "won": won,
    }
    st.session_state["games"].append(game)