import streamlit as st
import pandas as pd
import base64
from stats_logic import init_state

# Load background image 

with open("background_statistics.png", "rb") as image:
    encoded_image = base64.b64encode(image.read()).decode()

# Background styling

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

# font styling

st.markdown("""
    <div style="text-align: center; padding: 30px 0 20px 0;">
        <h1 style="
            text-align: center;
            color: #2B4136;
            font-size: 60px;
            font-family: Fraunces;
            font-weight: bold;
            margin-bottom: -25px;
            margin-top: -10px;
        ">
            Game Statistics
        </h1>
    </div>
""", unsafe_allow_html=True)

st.markdown(
    """
    <div style="
        text-align: center;
        font-family: 'Manrope', sans-serif;
        color: #30483C;
        font-size: 15px;
        font-style: italic;
        ">
            Some interesting statistics about your game history.
        </ul>
    </div>
    """,
    unsafe_allow_html=True
)

init_state()
games = st.session_state["games"]

# If no game is saved yet, show a message and stop
if len(games) == 0:
    st.info("No games finished yet. Play a round on the Play page first!")

else:
    # we initialize some variables to calculate the statistics with
    number_of_games = len(games)
    total_guesses = 0
    total_hints = 0
    total_jokers = 0
    total_information = 0
    won_games = 0

    for game in games: #loops through recorded games and adds up the numbers we get
        total_guesses = total_guesses + game["guesses"]
        total_hints = total_hints + game["hints"]
        total_jokers = total_jokers + game["jokers"]

        if game["won"]:
            won_games = won_games + 1

    #we calculate the averages and percentages 
    average_guesses = total_guesses / number_of_games
    total_information = total_hints + total_jokers
    average_information = total_information / number_of_games
    win_percentage = won_games / number_of_games * 100

    # displaying the basic statistics in containers
    part1, part2, part3, part4 = st.columns(4)
    with part1.container(border=True):
        st.metric("Games played", number_of_games)
    with part2.container(border=True):
        st.metric("Total Guesses", total_guesses)
    with part3.container(border=True):
        st.metric("Win Percentage", f"{win_percentage:.1f}%")
    with part4.container(border=True):
        st.metric("Guesses/Game", round(average_guesses, 1))

    # the bar chart showing the amount of information used per game
    st.subheader("Hints + Questions per game")

    #this is the bar chart showing you how many hints and questions you used in each game, to see if you are getting better at guessing the country with less information
    chart_labels = []
    won_counts = []
    lost_counts = []

    for number, game in enumerate(games, start=1): #in this for loop we go through the games and assign a color and count the information needed
        chart_labels.append("Round " + str(number))
        count = game["hints"] + game["jokers"]

        if game["won"]:
            won_counts.append(count)
            lost_counts.append(None)
        else:
            won_counts.append(None)
            lost_counts.append(count)

    information_chart = pd.DataFrame({
        "Won": won_counts,
        "Lost": lost_counts
    }, index=chart_labels)

    st.bar_chart(information_chart, color=["#439243", "#863030"], stack=True)

    # here we estimate the quality of the guesses 

    st.subheader("Quality of guesses")
    st.caption("Each guess is judged based on whether all or some hints were properly considered")

    #initialize counters and then count based on the nested for-loop after what we calculate the percentages
    good_count = 0
    okay_count = 0
    bad_count = 0

    for game in games:
        for label in game["labels"]:
            if label == "Good":
                good_count = good_count + 1
            elif label == "Okay":
                okay_count = okay_count + 1
            elif label == "Bad":
                bad_count = bad_count + 1

    good_share = round(100 * good_count / (good_count + okay_count + bad_count))
    okay_share = round(100 * okay_count / (good_count + okay_count + bad_count))
    bad_share = round(100 * bad_count / (good_count + okay_count + bad_count))

    # count how many hints were considered and how many there were potentially to consider 
    checks_total = 0
    checks_fit = 0
    for game in games:
        for guess_row in game["hint_checks"]:
            for result in guess_row:
                checks_total = checks_total + 1
                if result:
                    checks_fit = checks_fit + 1

    hints_share = 0
    if checks_total > 0:
        hints_share = round(100 * checks_fit / checks_total)

    # displaying the quality of guesses in containers
    q1, q2, q3, q4 = st.columns(4)
    with q1.container(border=True):
        st.metric("Good", str(good_share) + "%")
    with q2.container(border=True):
        st.metric("Okay", str(okay_share) + "%")
    with q3.container(border=True):
        st.metric("Bad", str(bad_share) + "%")
    with q4.container(border=True):
        st.metric("Hints considered", str(hints_share) + "%")

    #table showing different stats for each individual game, including the country, result, number of guesses, hints and AI questions used
    st.subheader("Games in detail")

    table_rows = []
    
    for game in games: 
        if game["won"]:
            result_text = "Won"
        else:
            result_text = "Lost"

        table_rows.append({
            "Country": game["country"],
            "Result": result_text,
            "Guesses": game["guesses"],
            "Hints": game["hints"],
            "AI questions": game["jokers"],
        })

    st.dataframe(pd.DataFrame(table_rows), hide_index=True) #this displays the table with the data we just collected

st.divider()

#button styling

st.markdown("""
<style>

div.stButton > button {
    background-color: #30483C;
    color: #A5B58B;
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
    background-color: #98A780;
    color: #30483C;
    border: none;
    transform: scale(1.05);
}

/* focus effect for the button */

div.stButton > button:focus {
    box-shadow: none;
}
</style>
""", unsafe_allow_html=True)

if st.button("GO BACK"):
    st.switch_page("welcome.py")