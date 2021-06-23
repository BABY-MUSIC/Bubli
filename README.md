# Building a Simple Bhojpuri Chatbot: Bubli v0.1.

Bubli a pretty basic bot with few cognitive abilities, but it's still an excellent way to chat. 


# Outline
* [Motivation](#motivation)
* [Pre-requisites](#pre-requisites)
* [How to run](#how-to-run)


## Motivation

I am a native Bhojpuri speaker, a beautiful north Indian language. For fun, I wanted to converse with a chatbot.
Bubli is my very first chatbot projects, created with natural language processing.

## Pre-requisites
**NLTK(Natural Language Toolkit)**

[Natural Language Processing with Python](http://www.nltk.org/book/) provides a practical introduction to programming for language processing.

For platform-specific instructions, read [here](https://www.nltk.org/install.html)

### Installation of NLTK
```
pip install nltk
```
### Installing required packages
After NLTK has been downloaded, install required packages
```
import nltk
from nltk.stem import WordNetLemmatizer
nltk.download('popular', quiet=True)
nltk.download('punkt') 
nltk.download('wordnet') 
```

## How to run

* Run through terminal
```
python bubli.py
```
