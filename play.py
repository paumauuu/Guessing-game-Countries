import streamlit as st
import random, math
import json
import base64
from countries import countries, countries2
from ai_chat import ask_ai
from openai import AuthenticationError, OpenAIError
from stats_logic import record_game, check_hints   

#Load background image 

with open("background_play.png", "rb") as image:
    encoded_image = base64.b64encode(image.read()).decode()

#Background styling

st.markdown(f"""
<style>

.stApp {{
    background-image: url("data:image/png;base64,{encoded_image}");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
}}
</style>
""", unsafe_allow_html=True)

#loading custom fonts and define title style

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fraunces:wght@400;500;600;700&display=swap');
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("""
    <div style="text-align: center; padding: 30px 0 20px 0;">
        <h1 style="
            color: #000000;
            font-size: 55px;
            font-family: Fraunces;
            font-weight: bold;
            margin-bottom: -5px;
            margin-top: -15px;
        ">
            Guess the Country!
        </h1>
    </div>
""", unsafe_allow_html=True)

#use inline-block and text-align to keep the bullet points text aligned while centering the list.

st.markdown(
    """
    <div style="
        font-family: 'Manrope', sans-serif;
        color: #000000;
        font-size: 15px;
        text-align: center;
    ">
        <ul style="
            display: inline-block;
            text-align: left;
        ">
            <li>You have 6 guesses to find the mystery country.</li>
            <li>After each incorrect guess, you'll receive a hint.</li>
            <li>You can also ask the AI yes/no questions about the country in the chat.</li>
            <li>Good luck! :)</li>
        </ul>
    </div>
    """,
    unsafe_allow_html=True
)

#saves the API key in session_state so it remains available when switching between pages

def save_api_key():
    st.session_state["saved_api_key"] = st.session_state["api_key_input"]


with st.sidebar:
    api_key = st.text_input(
        "UOS AI API-Key",
        type="password",
        key="api_key_input",
        value=st.session_state.get("saved_api_key", ""),
        on_change=save_api_key,
        placeholder="sk-...",
    )

    if api_key:
        st.session_state["saved_api_key"] = api_key

if not api_key:
    st.info("Please enter your Uni Osnabrück API key.")
    st.stop()

if "history" not in st.session_state:
    st.session_state["history"] = []


#memory for the scores, AI questions and hint rules for statistics.py, also for the chat history so we can display it in the chat

if "qualities" not in st.session_state:
    st.session_state["qualities"] = []
if "jokers" not in st.session_state:
    st.session_state["jokers"] = 0
if "hint_data" not in st.session_state:
    st.session_state["hint_data"] = []
if "hint_checks" not in st.session_state:
    st.session_state["hint_checks"] = []

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

#function that resets game state by clearing up the session_state variables and generating a new first hint

def game_initialize():  
    st.session_state["country"] = random.choice(list(countries))
    st.session_state["hints"] = []
    st.session_state["used_letterhints"] = []
    st.session_state["used_facthints"] = []
    st.session_state["guess_count"] = 0
    st.session_state["game_over"] = False
    st.session_state["won"] = False
    st.session_state["chat_history"] = []
    generate_hint() #So you get a new first hint even when you restart
    st.session_state["qualities"] = []
    st.session_state["jokers"] = 0
    st.session_state["hint_data"] = []
    st.session_state["hint_checks"] = []

# function that generates a hint, based on which hints we have so far

def generate_hint(): 
    #we first get the country and its data after what we compile all the types of hints that are still possible
    country = st.session_state["country"]

    data = countries[country]
    fact_types = []

    for i in ["gdp", "population", "area", "continent"]: #this for loop checks all the fact hint types wether we already used them individually
        if i not in st.session_state["used_facthints"]:
            fact_types.append(i)

    available_letters = list(set(country.upper()))
    new_available_letters = []
    for i in available_letters:
        if i.isalpha() and i not in st.session_state["used_letterhints"]:
            new_available_letters.append(i)

    available_letters = new_available_letters

    if len(available_letters) > 0: #if letters are available then we also consider giving a letter hint
        fact_types.append("letter")

    if len(fact_types) > 0: #if its possible for us to give a hint, which is pretty much always the case, we randomly choose a hint type and then generate that kind of hint
        hint_type = random.choice(fact_types)

        if hint_type == "letter": #here we generate a letter hint and save that we did so
            letter = random.choice(available_letters)
            st.session_state["used_letterhints"].append(letter)
            hint = "The country has the letter " + letter

            st.session_state["hint_data"].append({"kind": "letter", "value": letter})

        else:
            st.session_state["used_facthints"].append(hint_type)

            #gdp, population, area and continent hints are generated here and the rules for them are saved in hint_data for later use in statistics.py

            if hint_type == "gdp":
                limit = random.choice([69, 200, 500, 1000, 2000, 5000])
                if data["gdp"] >= limit:
                    hint = "The GDP is larger than $" + str(limit) + " billion."
                else:
                    hint = "The GDP is smaller than $" + str(limit) + " billion."
                st.session_state["hint_data"].append({"kind": "gdp", "limit": limit, "above": data["gdp"] >= limit})

            elif hint_type == "population":
                limit = random.choice([5, 20, 50, 69, 100, 200, 500])
                if data["population"] >= limit * 1000000:
                    hint = "The population is at least " + str(limit) + " million."
                else:
                    hint = "The population is less than " + str(limit) + " million."
                st.session_state["hint_data"].append({"kind": "population", "limit": limit * 1000000, "above": data["population"] >= limit * 1000000})

            elif hint_type == "area":
                limit = random.choice([50000, 100000, 500000, 696969, 1000000, 5000000])
                if data["area"] >= limit:
                    hint = "The area is at least " + str(limit) + " km²."
                else:
                    hint = "The area is less than " + str(limit) + " km²."
                
                st.session_state["hint_data"].append({"kind": "area", "limit": limit, "above": data["area"] >= limit})

            elif hint_type == "continent":
                hint = "The country is in " + data["continent"]
                st.session_state["hint_data"].append({"kind": "continent", "value": data["continent"]})

        st.session_state["hints"].append(hint)

#detects if game has not begun yet and initializes it if so

if "country" not in st.session_state: 
    game_initialize()

with st.form("guess_country", clear_on_submit=True): #make the player enter a guess
    guess = st.text_input("Enter the country you think it is:",value="",)
    submitted = st.form_submit_button("Submit")

if submitted and not st.session_state["game_over"]: #if the game is not over, we check if the guess is correct and then either end the game or give another hint

    guess = guess.strip() #clean up the input 

    if not guess: #make sure you dont enter nothing
        st.warning("Please enter a country.")

    elif guess.casefold() in [c.casefold() for c in countries2]: #make sure you dont enter a country that exists but is not in the game
        st.error("This country exists, but it is not available in the game.")

    elif guess.casefold() not in [c.casefold() for c in countries]: #make it more flexible (doesnt care if its gErMaNy or germany) check if the input is a country
        st.error("Please enter a valid country.")

    else:
        country = st.session_state["country"]

         # find the correct spelling of the guess (for statistics.py) 
        matched = guess
        for c in countries:
            if c.casefold() == guess.casefold():
                matched = c

        # check this guess against the hints shown so far (for statistics.py)
        st.session_state["hint_checks"].append(
            check_hints(st.session_state["hint_data"], matched))

        # Check if the guess is correct
        if guess.casefold() == country.casefold():
            st.session_state["guess_count"] += 1 #basic stuff like increasing guess count and displaying it, then ending the game
            st.session_state["game_over"] = True
            st.session_state["won"] = True

            st.session_state["history"].append(st.session_state["guess_count"]) #save the guess count and record the game for statistics.py   
            record_game(country, 
                len(st.session_state["hints"]), st.session_state["jokers"], True,
                st.session_state["hint_checks"])

        else: #guessed wrong and either you get another hint or the game is over
            st.session_state["guess_count"] += 1

            if st.session_state["guess_count"] < 6: #if its just a wrong guess we just generate another hint
                generate_hint()
            else:
                st.session_state["game_over"] = True #ends the game and save the shit

                st.session_state["history"].append(st.session_state["guess_count"]) #save the guess count and record the game for statistics.py   
                record_game(country, 
                len(st.session_state["hints"]), st.session_state["jokers"], False,
                st.session_state["hint_checks"])

if not st.session_state["game_over"]:
    st.write(f"Guesses: {st.session_state['guess_count']} / 6")
    # Display previous messages
    for message in st.session_state["chat_history"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Get a new question
    if question := st.chat_input("Ask a yes-or-no geography question..."):
        st.session_state["jokers"] += 1
        st.session_state["chat_history"].append({"role": "user", "content": question})

        with st.chat_message("user"):
            st.markdown(question)

        try:
            with st.spinner("The AI is thinking..."):

                answer = ask_ai(
                    api_key,
                    st.session_state["country"],
                    question,
                    st.session_state["chat_history"][:-1]
                )

            st.session_state["chat_history"].append({"role": "assistant", "content": answer})

            with st.chat_message("assistant"):
                st.markdown(answer)

        except AuthenticationError:
            st.error("API key not accepted. Please check your key.")

        except OpenAIError:
            st.error("AI request failed. Please try again.")


for hint in st.session_state["hints"]:
    st.info(hint)

if st.session_state["game_over"]: #game over message and option to play again

    if st.session_state["won"]:
        st.success(
            f"Correct! You found {st.session_state['country']} "
            f"in {st.session_state['guess_count']} guesses!"
        )
    else:
        st.error(f"Game over! The country was {st.session_state['country']}.")
    
    if st.button("Play again"): #play again button to initialize game
        game_initialize()
        st.rerun()


#button styling

st.markdown("""
<style>

div.stButton > button {
    background-color: #214761;
    color: #B7C9E2;
    border: none;
    border-radius: 20px;
    width: 110px;
    height: 60px;
    font-family: 'Manrope', sans-serif;
    font-size: 100px;
    letter-spacing: 2px;
    transition: all 0.25s ease;
}

/* hover effect for the button */

div.stButton > button:hover {
    background-color: #B7C9E2;
    color: #214761;
    border: none;
    transform: scale(1.05);
}

/* focus effect for the button */

div.stButton > button:focus {
    box-shadow: none;
}
</style>
""", unsafe_allow_html=True)

if st.button("GO BACK"): #go back to the welcome page
    st.switch_page("welcome.py")