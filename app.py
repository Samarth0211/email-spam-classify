import streamlit as st
import nltk
from nltk.corpus import stopwords
import string
from nltk.stem.porter import PorterStemmer
import pickle


def transform_text(text):
    text = text.lower()
    text = nltk.word_tokenize(text)
    y = []
    for i in text:
        if i.isalnum():
            y.append(i)
    text = y[:]
    y.clear()
    for i in text:
        if i not in stopwords.words('english') and i not in string.punctuation:
            y.append(i)
    text = y[:]
    y.clear()
    for i in text:
        y.append(ps.stem(i))
    return " ".join(y)

ps = PorterStemmer()
# nltk.download('stopwords')
# stop_words = set(stopwords.words('english'))
# print(stopwords)
stopwords_file_path = "english_stopwords.txt"

# Initialize an empty set to store the stopwords
stop_words = set()

# Read the stopwords from the file and store them in the set
with open(stopwords_file_path, 'r') as file:
    for line in file:
        stop_words.add(line.strip())

tfidf = pickle.load(open('vectorizer.pkl','rb'))
model = pickle.load(open('model.pkl','rb'))

st.title("Email Spam Classifier")

input_email = st.text_input("Enter the E-mail")
if st.button('Predict'):
    transform_email = transform_text(input_email)
    vector_input = tfidf.transform([transform_email])

    result = model.predict(vector_input)[0]
    if result == 1:
        st.header("Spam")
    else:
        st.header("Not Spam")