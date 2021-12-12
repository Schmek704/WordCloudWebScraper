# This program will return a word cloud from a web page based on user input
# User will input a web page address and quantity parameters of words for the word cloud

# Import Libraries

# streamlit is the web app designer
import streamlit as st

# Beautiful Soup module helps in web scrapping
from bs4 import BeautifulSoup
# Requests module sends http requests to a web page
import requests
# WordCloud library
from wordcloud import WordCloud, STOPWORDS
# MatPlotLib library
import matplotlib.pyplot as plt
# Python Image Library (Pillow)
from PIL import Image


# create a function to scrape a web page and create a variable word cloud based on the 'p' sections text
def cloud_scrape(url, qty_words):
    # using the url, use the requests library to extract the webpage,
    # receiving that data as the html code from the page
    if len(url) < 10:
        return st.write("Please make sure the address is the complete web URL from your browser's address bar!")
    page = requests.get(url)
    # create a beautiful soup object using the request response above, find all sections tagged with 'p'
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find_all('p')
    # check to see if results from web page may not have enough values to return for the word cloud
    if len(results) == 0:
        return print("This webpage may not allow web scraping, or there is not enough text to scrape on this page")

    # Create a Function to remove html tags from the soup object
    def remove_tags(html):
        for data in html(['style', 'script']):
            # Remove tags
            data.decompose()
            # return data by retrieving the tag content
            return ' '.join(html.stripped_strings)

    # Execute the function on the beautiful soup object, create a list of words from the object
    soup_clean = remove_tags(soup)
    final = soup_clean.split()
    # remove any whitespace that may have been missed, using list comprehension
    final = [x.strip(' ') for x in final]
    # remove any single letters that are in the list, using list comprehension
    final = [x for x in final if len(x) > 1]
    # set variables for the word cloud function, add any additional words to the default set of words to ignore
    comment_words = ''
    stopwords = set(STOPWORDS)
    stopwords.update(['articles', 'site', 'home', 'columns'])
    ignore_word = " "
    stopwords.update(ignore_word)
    # iterate through the object and return the list of words
    for val in final:
        # typecast each val to string
        val = str(val)
        # split the list into tokens
        tokens = val.split()
        # Convert each token into lowercase
        for i in range(len(tokens)):
            tokens[i] = tokens[i].lower()
        comment_words += " ".join(tokens) + " "

    # create the word cloud object
    cloud = WordCloud(
        width=800,
        height=800,
        background_color='white',
        normalize_plurals=True,
        stopwords=stopwords,
        max_words=qty_words,
        min_font_size=10).generate(comment_words)
    # plot the WordCloud image
    plt.figure(figsize=(5, 5), facecolor=None)
    plt.imshow(cloud)
    plt.axis("off")
    plt.tight_layout(pad=0)
    # Save and display the word cloud in a new window
    plt.savefig("words.jpg")
    image = Image.open('words.jpg')
    image.show()
    return "words.jpg"


# TEST THE FUNCTION
# create a variable that will be the target of the web scrape request
# user will be asked to input the web page address and any one word to specifically ignore
st.title("Web Scraping Word Cloud Generator")
url_input = st.text_input("Please copy and paste the complete web URL form your address bar", value="https://")
# set word cloud word quantity
qty_words_input = st.number_input("How many words would you like to see in your word cloud?  ", min_value=10)
if url_input:
    cloud_scrape(url_input, qty_words_input)
