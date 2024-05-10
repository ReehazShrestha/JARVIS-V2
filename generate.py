import streamlit_authenticator as stauth 
import pickle
from pathlib import Path
import streamlit as st

name = ['Peter Parker', 'Bruce Wane']
user_name = ['spider', 'bat']
password = ['XXXXX', 'XXXXXX']

hashed_psw = stauth.Hasher(password).generate()

file_path = Path(__file__).parent / "hashed_password.pkl"

with file_path.open("wb") as file:
    pickle.dump(hashed_psw, file)