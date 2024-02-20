import streamlit as st
import pickle
import requests
from bs4 import BeautifulSoup
import pickle
from sklearn.feature_extraction.text import CountVectorizer


st.header('Dark Pattern Recognition', divider='rainbow')
model = pickle.load(open('model.pkl','rb'))

text_input = st.text_input("Enter the URL 👇 in (https://www.example.com) format")
if text_input:
    st.write("The URL you entered: ", text_input)

# url = 'https://www.amazon.in/'
# url = 'https://naveedqadir0.pythonanywhere.com'
    url = str(text_input)

    response = requests.get(url)
    model = pickle.load(open('model.pkl','rb'))
    count_vect = pickle.load(open('count_vect.pkl','rb'))

    c_dark = 0
    c_not = 0
    total = 0
    per_dark = 0

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        header = soup.find_all('div')
        for h in header:
            result = model.predict(count_vect.transform([h.text]))
            if result[0] == 'Dark':
                c_dark = c_dark + 1
            else:
                c_not = c_not + 1
                
        # print('c_not: ',c_not )
        # print('c_dark: ', c_dark)
        total = c_dark + c_not
        # print(total)
        per_dark = (c_dark / total ) * 100
        # print('per_dark: ', per_dark)
        st.write(f"Percentage of dark pattern in the provided URL:  :blue[**{per_dark}%**]")
    else:
        print(f'Failed to retrieve the page. Status code: {response.status_code}')
        st.write("Failed to retrieve the page. Status code: ", response.status_code)
