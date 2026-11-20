import streamlit as st

page1 = st.Page("welcome.py", title="Start")
page2 = st.Page("play.py", title="Play")
page3 = st.Page("statistics.py", title="Statistics")


pg = st.navigation(pages=[page1, page2, page3])
pg.run()
