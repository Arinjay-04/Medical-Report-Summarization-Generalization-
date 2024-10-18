import pdfplumber
import pandas as pd
from pdfplumber.utils import extract_text, get_bbox_overlap, obj_to_bbox
import tabulate

import pdfplumber


###  EXTRACTING TEXT FROM THE PDF file


def extract_text_from_pdf(pdf_path):
    """
    Extracts all text from a PDF file and returns it as a single string.

    Args:
        pdf_path (str): The file path to the PDF document.

    Returns:
        str: The extracted text from the PDF.
    """
    all_text = []


    with pdfplumber.open(pdf_path) as pdf:

        for page_number, page in enumerate(pdf.pages, start=1):

            page_text = page.extract_text()

            if page_text:
                all_text.append(page_text)
            else:
                print(f"Warning: No text found on page {page_number}.")


    return "\n".join(all_text)


pdf_path = r"your_file_path"
extracted_text = extract_text_from_pdf(pdf_path)
print(extracted_text)



## Summarizing the text using T2 model + ony retriving the text related to given key word

import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from collections import Counter
from heapq import nlargest

nlp = spacy.load('en_core_web_sm')




focus_word = input("Enter ").lower()


stopwords = list(STOP_WORDS)
allowed_pos = ['ADJ', 'PROPN', 'VERB', 'NOUN']


doc = nlp(extracted_text)


tokens = [
    token.lemma_.lower()
    for token in doc
    if not token.is_punct and token.lemma_.lower() not in stopwords and token.pos_ in allowed_pos
]


freq = Counter(tokens)
max_freq = max(freq.values()) if freq else 1


for word in freq:
    freq[word] /= max_freq


lines = extracted_text.split('\n')
lines = [line.strip() for line in lines if line.strip()]

sentence_scores = {}


focus_word_related_sentences = [
    line for line in lines if focus_word in line.lower()
]


if not focus_word_related_sentences:
    print(f"No sentences found related to '{focus_word}'.")
else:

    for line in focus_word_related_sentences:
        line_doc = nlp(line)
        for token in line_doc:
            lemma = token.lemma_.lower()
            if lemma in freq:
                sentence_scores[line] = sentence_scores.get(line, 0) + freq[lemma]


    num_sentences = 5
    summary_sentences = nlargest(num_sentences, sentence_scores, key=sentence_scores.get)


    word_related_summary = ' '.join([sent for sent in summary_sentences])


    print(f"\nSummary related to '{focus_word}':\n")
    print(word_related_summary)


## Integrating LLP (openAi) to generalize the text

import requests
import json

def fetch_ai_explanation(prompt, api_key):
    url = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent'
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        'contents': [
            {
                'parts': [
                    {
                        'text': prompt
                    }
                ]
            }
        ]
    }


    response = requests.post(url, headers=headers, params={'key': api_key}, json=data)


    if response.status_code == 200:
        return response.json()
    else:
        return {'error': response.status_code, 'message': response.text}


api_key = 'AIzaSyDeZ71gRCQmFB-FzNrwrrhdEBvkbZ940VM'
prompt =  word_related_summary
result = fetch_ai_explanation(prompt, api_key)
text_content = result["candidates"][0]["content"]["parts"][0]["text"]
print(text_content)
