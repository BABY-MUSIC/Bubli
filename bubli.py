#Meet Bubli: apaki apani dost !
#Jitendra Narayan @ jnarayan81@gmail.com

#import necessary libraries to begin with
import io
import random
import string 
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import warnings
warnings.filterwarnings('ignore')

import nltk
from nltk.stem import WordNetLemmatizer
nltk.download('popular', quiet=True) # for downloading packages

#Few stuff you need to use in first round of run
# uncomment the following only the first time
#nltk.download('punkt') # first-time use only
#nltk.download('wordnet') # first-time use only


#Reading in the corpus -- training themself from here
with open('chatbot.txt','r', encoding='utf8', errors ='ignore') as fin:
    raw = fin.read().lower()

#TOkenisation
sent_tokens = nltk.sent_tokenize(raw)# converts to list of sentences 
word_tokens = nltk.word_tokenize(raw)# converts to list of words

# Preprocessing
lemmer = WordNetLemmatizer()
def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]
remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)
def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))


# Keyword Matching
GREETING_INPUTS = ("ka", "hi", "ka ba", "bol", "bolo","kaha",)
GREETING_RESPONSES = ["ka ho", "kaisan", "sab thik", "nik", "nike ba", "Maja aa gail ho! Baat kar ke"]

def greeting(sentence):
    """If user's input is a greeting, return a greeting response"""
    for word in sentence.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES)


# Generating response by bubli
def response(user_response):
    bubli_response=''
    sent_tokens.append(user_response)
    TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
    tfidf = TfidfVec.fit_transform(sent_tokens)
    vals = cosine_similarity(tfidf[-1], tfidf)
    idx=vals.argsort()[0][-2]
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]
    if(req_tfidf==0):
        bubli_response=robo_response+"Mafi! Kuchu bujhail na"
        return robo_response
    else:
        bubli_response = bubli_response+sent_tokens[idx]
        return bubli_response


flag=True
print("Bubli: Hum bubli bola tani. Rauaa humase baat kari na. ! Na ta likhi 'jo' ya 'tata'")
while(flag==True):
    user_response = input()
    user_response=user_response.lower()
    if(user_response!='tata'):
        if(user_response=='jo' or user_response=='Thik ba' ):
            flag=False
            print("Bubli: ja tani, huh..")
        else:
            if(greeting(user_response)!=None):
                print("Bubli: "+greeting(user_response))
            else:
                print("Bubli: ",end="")
                print(response(user_response))
                sent_tokens.remove(user_response)
    else:
        flag=False
        print("Bubli: Bye! Aapan Khyal Rakhi..")

