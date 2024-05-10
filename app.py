import streamlit_authenticator as stauth 
import pickle
from pathlib import Path
import streamlit as st
from streamlit_option_menu import option_menu
import google.generativeai as genai

st.set_page_config(page_title="Practice Page", page_icon=":tada:", layout="wide")
remove_default_lauout = '''
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
'''
st.markdown(remove_default_lauout,unsafe_allow_html=True)
genai.configure(api_key="AIzaSyDamDyhxxAKQXhfsFbImw65-L_rehmbcQg")
model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat(history=[])

name = ['Peter Parker', 'Bruce Wane']
user_name = ['spider', 'bat']

file_path = Path(__file__).parent / "hashed_password.pkl"
with file_path.open("rb") as file:
    hashed_password = pickle.load(file)

authenticator = stauth.Authenticate(name, user_name, hashed_password, "cookies", "", cookie_expiry_days=30)

name, authentication_status, user_name = authenticator.login("Login", "main")

if authentication_status == None:
    st.warning("Fill your username and password !")
if authentication_status == False:
    st.error("Invalid username or password !")
if authentication_status:
    st.balloons()

    with st.sidebar:
        st.markdown(f"# WELCOME {user_name}")
        st.markdown("---")
        selected = option_menu(
            menu_title="Main Menu",
            options=["Jarvis"],
            icons=["robot"],
            menu_icon="cast"
        )
        st.markdown('---')
        authenticator.logout("LOG OUT", "sidebar")


    if "messages" not in st.session_state:
        st.session_state.messages= []
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    prompt = st.chat_input('Ask me ......')
    if not prompt:
        st.markdown('''
        <div style="text-align:center;">
        <h1>Jarvis The ChatBot</h1>
        <h2> <i>How Can I Help You ?</i> </h2>
        </div>              
        ''', unsafe_allow_html=True)


    else:
        with st.chat_message('user'):
            st.markdown(prompt)
            st.session_state.messages.append({"role":"user", "content": prompt})


    try:
        chat.send_message(prompt)
        response = chat.last.text
    except:
        response = f"Faild Connecting With API'S  LOL"

    with st.chat_message('assistant'):
        st.markdown(response)
        st.session_state.messages.append({"role":"assistant", "content": response})
