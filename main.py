# Libraries
import urllib3
import requests
from bs4 import BeautifulSoup
import streamlit as st
from sumy.summarizers.lex_rank import LexRankSummarizer
from sumy.summarizers.text_rank import TextRankSummarizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.nlp.tokenizers import Tokenizer
from sumy.parsers.plaintext import PlaintextParser
#from gensim.summarization.summarizer import summarize
import nltk
nltk.download('punkt')
# text tu\o audio
#import pyttsx3

# summarization

# UI

# web scaping

# OCR
# import pytesseract
# import cv2
# import easyocr


LANGUAGE = "english"

# functions


def textFromYoutube(link):
    id = link.split('watch?v=')
    srt = YouTubeTranscriptApi.get_transcript(
        id[1])
    print(srt)
    text_list = []
    for i in srt:
        text_list.append(i['text'])
    text = ' '.join(text_list)
    return text


def textFromLink(link):
    if 'watch?v=' in link:
        return textFromYoutube(link)
    else:
        res = requests.get(link)
        res = BeautifulSoup(res.text, 'lxml')
        txt = res.select('p')
        a = ''
        for i in txt:
            a += str(i.text)
            a += ' '
        return a


def imgFromLink(link):
    http = urllib3.PoolManager()
    url = link
    response = http.request('GET', url)
    soup = BeautifulSoup(response.data, "html.parser")
    images = soup.findAll('img')
    img = []
    for image in images:
        img.append(image['src'])
    return img


def LSA(txt, num):
    parser = PlaintextParser.from_string(txt, Tokenizer(LANGUAGE))
    summarizer_1 = LsaSummarizer()
    summary_1 = summarizer_1(parser.document, num)
    ans = ''
    for sentence in summary_1:
        ans += str(sentence)
        ans += ' '

    st.write(len(txt))
    st.write(len(ans))
    return ans


def textRank(txt, num):
    parser = PlaintextParser.from_string(txt, Tokenizer(LANGUAGE))
    summarizer_1 = TextRankSummarizer()
    summary_1 = summarizer_1(parser.document, num)
    ans = ''
    for sentence in summary_1:
        ans += str(sentence)
        ans += ' '

    st.write(len(txt))
    st.write(len(ans))
    return ans


def luhnSummarizer(txt, num):
    parser = PlaintextParser.from_string(txt, Tokenizer(LANGUAGE))
    from sumy.summarizers.luhn import LuhnSummarizer
    summarizer_1 = LuhnSummarizer()
    summary_1 = summarizer_1(parser.document, num)
    ans = ''
    for sentence in summary_1:
        ans += str(sentence)
        ans += ' '

    st.write(len(txt))
    st.write(len(ans))
    return ans


# def mysummarizer(txt):
#     txt = summarize(txt)
#     return txt


def LexSummarizer(txt, num):
    parser = PlaintextParser.from_string(txt, Tokenizer(LANGUAGE))
    summarizer_1 = LexRankSummarizer()
    summary_1 = summarizer_1(parser.document, num)
    ans = ''
    for sentence in summary_1:
        ans += str(sentence)
        ans += ' '

    st.write(len(txt))
    st.write(len(ans))
    return ans


if __name__ == '__main__':
    #speaker = pyttsx3.init()

    st.title("Tinygram")
    link = st.text_input('Enter the link of the website : ')
    link_txt = ''
    txt = ''

    st.subheader("or")

    txt_box = st.text_area(label='Enter Your Text', value="", height=200, max_chars=None,
                           key=None, help=None, on_change=None, args=None, kwargs=None, placeholder=None)
    txt2 = ''
    title = ''
    # st.subheader('or')
    #img = st.file_uploader("Choose a Image")
    number = st.number_input('Enter Number of Sentences', value=5)

    # if img is not None:
    #     img = cv2.imread('img1.png')
    #     text = pytesseract.image_to_string(img)
    #     st.write(txt)

    # result = cloudinary.uploader.upload(uploaded_image)
    # url = result.get('url')
    # st.write(url)
    # reader = easyocr.Reader(['en'], gpu= False)
    # result = reader.readtext('img1.png')
    # st.write(result)

    algo = st.radio(
        "Select Algorithm: ",
        ('Lex', 'Luhn', 'LSA', 'Text Ranking'))

    images = []

    if st.button('Summarize'):
        try:
            link_txt = textFromLink(link)
            images = imgFromLink(link)
        except:
            pass
        title = 'Summarized text:'
        txt = link_txt + txt_box

        # if algo == 'Gensim':
        #     txt2 = mysummarizer(txt)

        if algo == 'Lex':
            txt2 = LexSummarizer(txt, number)

        elif algo == 'Luhn':
            txt2 = luhnSummarizer(txt, number)

        elif algo == 'LSA':
            txt2 = LSA(txt, number)

        elif algo == 'Text Ranking':
            txt2 = textRank(txt, number)

    st.title(title)
    st.write(txt2)
    for i in images:
        try:
            st.image(i)
        except:
            pass

    st.write("Made with ❤️ by Keshav Tanwar")

    # col1, col2, col3, col4, col5 = st.columns(5)
    # with col1:
    #     if st.button('Genism'):
    #         if len(txt) < 10:
    #
    #             st.write('sentence is too short')
    #         else:
    #             title = 'Summarized text:'
    #             txt2 = mysummarizer(txt)
    # with col2:
    #     if st.button('Lex'):
    #         if len(txt) < 10:
    #             st.write('sentence is too short')
    #         else:
    #             title = 'Summarized text:'
    #             txt2 = LexSummarizer(txt, number)
    #
    # with col3:
    #     if st.button('Luhn'):
    #         if len(txt) < 10:
    #             st.write('sentence is too short')
    #         else:
    #             title = 'Summarized text:'
    #             txt2 = luhnSummarizer(txt, number)
    #
    # with col4:
    #     if st.button('LSA'):
    #         if len(txt) < 10:
    #             st.write('sentence is too short')
    #         else:
    #             title = 'Summarized text:'
    #             txt2 = LSA(txt, number)
    #
    # with col5:
    #     if st.button('Text Ranking'):
    #         if len(txt) < 10:
    #             st.write('sentence is too short')
    #         else:
    #             title = 'Summarized text:'
    #             txt2 = textRank(txt, number)
