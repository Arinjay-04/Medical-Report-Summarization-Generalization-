# Medical Report Text Extraction and Summarization Project

## Overview

This project aims to extract text from PDF documents and summarize the content based on user-defined keywords. It leverages several libraries, including `pdfplumber`, `pandas`, and `spaCy`, to handle text extraction and natural language processing tasks. Additionally, the project integrates with the OpenAI API to provide a generalized explanation of the summarized content.

## Features

- Extracts text from PDF files.
- Summarizes the text based on a focus keyword provided by the user.
- Uses NLP techniques to identify and rank sentences related to the focus keyword.
- Integrates with OpenAI's language model to provide generalized explanations of the summarized text.

## Requirements

- Python 3.x
- Libraries:
  - `pdfplumber`
  - `pandas`
  - `spacy`
  - `requests`
  - `tabulate`

You can install the required libraries using pip:

```bash
pip install pdfplumber pandas spacy requests tabulate
