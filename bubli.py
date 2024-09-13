import io
import random
import string
import numpy as np
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import warnings
import re
import tkinter as tk
from tkinter import scrolledtext
from datetime import datetime

# Suppress warnings
warnings.filterwarnings('ignore')

# Download NLTK packages if not already downloaded
nltk.download('popular', quiet=True)

from nltk.stem import WordNetLemmatizer

# Read in the corpus
with open('chatbot.txt', 'r', encoding='utf8', errors='ignore') as fin:
    raw = fin.read().lower()

# Tokenization
sent_tokens = nltk.sent_tokenize(raw)
word_tokens = nltk.word_tokenize(raw)

# Preprocessing
lemmer = WordNetLemmatizer()

def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]

remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)

def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))

# Keyword Matching
GREETING_INPUTS = ("hi", "hello", "ka", "ka ba", "bol", "bolo", "kaha", "kahan")
GREETING_RESPONSES = [
    "Ka ho! Kaise madad kari? 😊",
    "Hi! Ka kari? 😃",
    "Hello! Ka haal ba? 👋",
    "Hey! Kaise ba? 🤗"
]

# Extended Small Talk
SMALL_TALK_INPUTS = ("ka haal ba", "tohar naam ka ba", "ek joke suna", "ka kari sakat ba", "kaise ba", "kuch fun bata", "weather kaisa hai", "aaj kya din hai")
SMALL_TALK_RESPONSES = [
    "Hum bot bani, lekin theek ba! Dhanyawaad poochhe khatir. 😄",
    "Hum Bubli bani, aapan chatbot. Kaise madad kari? 🖐",
    "Gyaan rakh ke na, ki scientist log atom par bharosa nahi karte, kyunki woh sab kuch banawat ba! 🤔",
    "Hum kai tarah ke kaam me madad kar sakat bani. Batawa ka chahiye! 🙌",
    "Hum theek ba! Baatein kari ke ready bani. 😎",
    "Ego fun fact: Bhojpuri bhaasha bharatiya upmahadweep ke ek rochak bhaasha hai! 🌍",
    "Aaj kal mausam badal raha hai, par hum to hamesha yahin hain! ☀️🌧️",
    "Aaj {day}. Kaise raha aapka din? 📅"
]

# Extended FAQ Handling
FAQ_INPUTS = ("tohar naam ka ba", "tohar umar kitna ba", "kahan se aail ba", "aapka favorite color ka ba", "kaha rehta hai")
FAQ_RESPONSES = [
    "Humra naam Bubli ba. 🤖",
    "Hum timeless bani! Umar nahi hota. ⏳",
    "Hum digital duniya se aail bani. 🌐",
    "Humara favorite color to digital blue hai! 💙",
    "Hum virtual duniya mein rehta bani, aap ke sath! 🌟"
]

# Jokes and Fun Facts
JOKE_RESPONSES = [
    "Ek joke sunawe? Kahe computer apna homework nahi kar sakta? Kyunki woh always binary hota! 😆",
    "Aapko ek joke aur sunawe? Ek baar ek computer ne bola, 'Mujhe virus ho gaya!' Aur computer ke doctor ne bola, 'Tumhe zyada RAM ki zarurat hai!' 😂"
]

# User Name Management
user_name = None

# Help Command
HELP_RESPONSES = [
    "Humra se aap greeting, small talk, aur FAQ puch sakat bani. 🆘",
    "Hum basic math operations aur fun facts bhi de sakat bani. 🔢",
    "Agar aapko kuch aur chahiye, bas batawa. 🤗"
]

def greeting(sentence):
    """Return a greeting response if the user's input is a greeting."""
    for word in sentence.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES)

def small_talk(sentence):
    """Return a response for small talk."""
    for word in sentence.split():
        if word.lower() in SMALL_TALK_INPUTS:
            response = random.choice(SMALL_TALK_RESPONSES)
            if "aaj kya din hai" in sentence:
                day = datetime.now().strftime("%A")
                response = response.format(day=day)
            return response

def faq_response(sentence):
    """Return a response for frequently asked questions."""
    for word in sentence.split():
        if word.lower() in FAQ_INPUTS:
            return random.choice(FAQ_RESPONSES)

def help_response():
    """Return a help response."""
    return random.choice(HELP_RESPONSES)

def joke_response():
    """Return a random joke."""
    return random.choice(JOKE_RESPONSES)

def basic_sentiment_analysis(sentence):
    """Basic sentiment analysis based on keyword matching."""
    positive_keywords = ["khush", "acha", "theek", "badiya", "sundar", "shresth"]
    negative_keywords = ["udaas", "bura", "kharab", "ganda"]

    positive_count = sum(word in sentence.split() for word in positive_keywords)
    negative_count = sum(word in sentence.split() for word in negative_keywords)

    if positive_count > negative_count:
        return "Lagta hai aap khush hain! 😊"
    elif negative_count > positive_count:
        return "Aap udaas lag rahe hain. Hum madad kar sakat bani. 😔"
    else:
        return "Lagta hai aap neutral hain. 😐"

def basic_math(sentence):
    """Perform basic math operations."""
    try:
        numbers = re.findall(r'\d+', sentence)
        operator = re.search(r'[+\-*/]', sentence)
        if operator and len(numbers) == 2:
            num1, num2 = map(float, numbers)
            op = operator.group()
            if op == '+':
                return f"Jawab: {num1 + num2} 😊"
            elif op == '-':
                return f"Jawab: {num1 - num2} 😊"
            elif op == '*':
                return f"Jawab: {num1 * num2} 😊"
            elif op == '/':
                if num2 != 0:
                    return f"Jawab: {num1 / num2} 😊"
                else:
                    return "Division by zero ke liye khed hai. 😞"
    except:
        return "Math ke sawal ke liye sahi format dein. 😕"

def response(user_response):
    """Generate a response based on user input."""
    if user_response.startswith("hamar naam ba"):
        global user_name
        user_name = user_response.split("hamar naam ba")[-1].strip()
        return f"Achha, {user_name}! Aap se milke accha lagal. 😊"

    if "help" in user_response or "madad" in user_response:
        return help_response()
    
    if re.search(r'\d+[\+\-\*/]\d+', user_response):
        return basic_math(user_response)

    if "joke" in user_response or "fun" in user_response:
        return joke_response()

    bubli_response = ''
    sent_tokens.append(user_response)
    TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
    tfidf = TfidfVec.fit_transform(sent_tokens)
    vals = cosine_similarity(tfidf[-1], tfidf)
    idx = vals.argsort()[0][-2]
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]
    if req_tfidf == 0:
        bubli_response = "Maaf kari, hum samajh nahi paaye. 😕"
    else:
        bubli_response = sent_tokens[idx]
    sent_tokens.remove(user_response)
    return bubli_response

def on_send(event=None):
    """Handle the send button click or Enter key press."""
    user_response = user_input.get()
    if user_response.strip() == "":
        return
    
    chat_window.config(state=tk.NORMAL)  # Enable the chat window for editing
    chat_window.insert(tk.END, f"You: {user_response}\n", 'user')
    
    response_text = response(user_response)
    chat_window.insert(tk.END, f"Bubli: {response_text}\n", 'bot')
    
    chat_window.config(state=tk.DISABLED)  # Disable the chat window for editing
    chat_window.yview(tk.END)  # Scroll to the end

    user_input.delete(0, tk.END)  # Clear the input field

# ASCII art for Bubli
bubli_ascii_art = r"""
  _              
 |_)     |_  | o 
 |_) |_| |_) | | 
                 
"""

welcome_message = f"""
{bubli_ascii_art}
Welcome to Bubli, your Bhojpuri chatbot! 🌟
Aap kaise hain? Hum yahaan aapki madad ke liye hain. 😊
"""

# Create GUI
root = tk.Tk()
root.title("Bubli: Your Bhojpuri Chatbot")

# Chat window
chat_window = scrolledtext.ScrolledText(root, state='disabled', wrap=tk.WORD)
chat_window.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Display welcome message
chat_window.config(state=tk.NORMAL)  # Enable the chat window for editing
chat_window.insert(tk.END, f"Bubli: {welcome_message}\n", 'welcome')
chat_window.config(state=tk.DISABLED)  # Disable the chat window for editing

# User input
user_input = tk.Entry(root, width=80)
user_input.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.X, expand=True)
user_input.bind("<Return>", on_send)  # Bind the Enter key to the on_send function

# Send button
send_button = tk.Button(root, text="Send", command=on_send)
send_button.pack(side=tk.RIGHT, padx=10, pady=10)

# Configure tag colors
chat_window.tag_config('user', foreground='blue')   # User text color
chat_window.tag_config('bot', foreground='green')   # Bot text color
chat_window.tag_config('welcome', foreground='red', font=('Helvetica', 10, 'bold'))  # Welcome message color

root.mainloop()
