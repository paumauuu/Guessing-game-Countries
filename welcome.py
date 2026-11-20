import streamlit as st
import json
import base64
from streamlit_lottie import st_lottie

# Load background image
with open("background_welcome.png", "rb") as image:
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


# Loading custom fonts and define title style

st.markdown(
    """<style>
    @import url('https://fonts.googleapis.com/css2?family=Manrope:wght@300;400;500;600;700&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Fraunces:wght@400;700&display=swap');
    </style>""",
    unsafe_allow_html=True,
)

st.markdown(
    '''<div style="
        font-weight: bold;
        font-family: Fraunces;
        color: #30483C;
        font-size: 90px;
        margin-bottom: 0px;
    ">
        Discover the
    </div>''',
    unsafe_allow_html=True
)


st.markdown(
    '''<div style="
        text-align: left;
        padding-left: 55%;
        font-weight: bold;
        font-family: Fraunces;
        color: #A5B58B;
        font-size: 90px;
        margin-top: -15px;
    ">
        World
    </div>''', 
    unsafe_allow_html=True
)


st.markdown(
    """
    <div style=" 
        text-align: center; 
        font-family: 'Manrope', sans-serif; 
        color: #000000; 
        background-color: #FDF9F0; 
        display: block; 
        border-radius: 30px;
        width: fit-content;
        margin: 0 auto;
        padding: 4px 10px;
        font-style: italic;
        font-size: 20px;
        position: relative;
        z-index: 2;
    ">
        Your next destination is just a guess away
    </div>
    """,
    unsafe_allow_html=True
)

#button styling

st.markdown("""
<style>

div.stButton > button {
    background-color: #A5B58B;
    color: #30483C;
    border: none;
    border-radius: 20px;
    width: 150px;
    height: 80px;
    font-family: 'Manrope', sans-serif;
    font-size: 100px;
    letter-spacing: 2px;
    transition: all 0.25s ease;
}

/* hover effect for the button */

div.stButton > button:hover {
    background-color: #30483C;
    color: #FAF8F1;
    border: none;
    transform: scale(1.05);
}

/* focus effect for the button */

div.stButton > button:focus {
    box-shadow: none;
}

</style>
""", unsafe_allow_html=True)

if st.button("PLAY"):
        st.switch_page("play.py")

st.markdown("""
<style>
[data-testid="stImage"] {
    position: fixed;
    bottom: 90px;
    right: 90px;
    z-index: 1;
    transform: translate(50%, 50%);
}
</style>
""", unsafe_allow_html=True)

st.image("weltkugel.png", width=750)