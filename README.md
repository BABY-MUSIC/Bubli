![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Made with love in India](https://madewithlove.now.sh/in?heart=true&colorA=%23f65931&colorB=%23358a24&template=for-the-badge)

# Building a Simple Bhojpuri Chatbot: Bubli v0.1.

![Hum Bubli](https://github.com/jnarayan81/Bubli/blob/main/bubli.jpg)
[@source](https://best-sci-fi-books.com/wp-content/uploads/2020/06/female_protagonist.jpg)

Bubli a pretty basic bot with few cognitive abilities, but it's still an excellent way to chat. 

```diff
- Bhojpuri, oh yes bhojpuri
+ Sarcastically beautiful
! Essence of local
# A language full of double meanings
@@ ka ho (ka hal ba)@@

Inherit beauty of the bhojpuri language is -- you can easily twist it
kal hal ba
hal ka ba
ba ka hal

! All of the meanings remain the same ;) but proceed with caution —- there might be a hidden double meaning :P
```

# Outline
* [Motivation](#motivation)
* [Pre-requisites](#pre-requisites)
* [How to run](#how-to-run)


## Motivation

I am a native speaker of Bhojpuri, a lovely north Indian language. I wanted to talk to a chatbot just for fun. Bubli is one of my first chatbot projects, built using natural language processing. I am working on v0.2 with new cool features, stay tuned ...

### Why named 'Bubli'

Names are crucial to our personal identities. They are linked by strong personal, cultural, familial, and historical ties. They also help us understand who we are, where we fit in the world, and what communities we are a part of. I was inspired to name it 'Bubli' after a popular funny bhojpuri song called "hum bulbi bola tani"

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
