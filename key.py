import os.path
from dotenv import load_dotenv
import streamlit as st


# dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv()

CK = st.secrets("API_KEY")
CS = st.secrets("API_SECRET")
AK = st.secrets("ACCESS_TOKEN")
AS = st.secrets("ACCESS_TOKEN_SECRET")

NW = st.secrets("NEWS_KEY")

# CK = 'IM6rY9ffWSKfl36MhVsgRc6vI'
# CS= 'Hz6PKwWRUvhUNNXJ7X4K2rmvRYGesSRt4OGyn0HOJCyyRANZeB'
# AK = '1329983514536669205-7PoMb4fKwkhS3H6mNubCY81kLfZ0MD'
# AS = 'Xcq9t5acK99Y08pFvhUVIYO3QGaJeJY8Sy8pJ6F19HV6f'
#
# NW ="c3d8cb4b8e834bf1850416917d71dd4d"