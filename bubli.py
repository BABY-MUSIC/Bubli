import logging
import random
import string
import re
from datetime import datetime
import nltk
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
from sklearn.feature_extraction.text import TfidfVectorizer  # Add this import

# NLTK Setup
nltk.download('popular', quiet=True)
from nltk.stem import WordNetLemmatizer

lemmer = WordNetLemmatizer()
remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)

def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]

def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))

# Corpus
with open('chatbot.txt', 'r', encoding='utf8', errors='ignore') as fin:
    raw = fin.read().lower()

sent_tokens = nltk.sent_tokenize(raw)

# Greeting Inputs and Responses
GREETING_INPUTS = ("hi", "hello", "ka", "ka ba", "bol", "bolo", "kaha", "kahan")
GREETING_RESPONSES = [
    "Ka ho! Kaise madad kari? 😊",
    "Hi! Ka kari? 😃",
    "Hello! Ka haal ba? 👋",
    "Hey! Kaise ba? 🤗"
]

# Small Talk Inputs and Responses
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

# FAQ Inputs and Responses
FAQ_INPUTS = ("tohar naam ka ba", "tohar umar kitna ba", "kahan se aail ba", "aapka favorite color ka ba", "kaha rehta hai")
FAQ_RESPONSES = [
    "Humra naam Bubli ba. 🤖",
    "Hum timeless bani! Umar nahi hota. ⏳",
    "Hum digital duniya se aail bani. 🌐",
    "Humara favorite color to digital blue hai! 💙",
    "Hum virtual duniya mein rehta bani, aap ke sath! 🌟"
]

# Jokes
JOKE_RESPONSES = [
    "Kahe computer apna homework nahi kar sakta? Kyunki woh always binary hota! 😆",
    "Ek baar ek computer ne bola, 'Mujhe virus ho gaya!' Aur computer ke doctor ne bola, 'Tumhe zyada RAM ki zarurat hai!' 😂"
]

def greeting(sentence):
    """Check if user input is a greeting and respond accordingly."""
    for word in sentence.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES)

def small_talk(sentence):
    """Respond to small talk inputs."""
    for word in sentence.split():
        if word.lower() in SMALL_TALK_INPUTS:
            response = random.choice(SMALL_TALK_RESPONSES)
            if "aaj kya din hai" in sentence:
                day = datetime.now().strftime("%A")
                response = response.format(day=day)
            return response

def faq_response(sentence):
    """Respond to FAQ-style inputs."""
    for word in sentence.split():
        if word.lower() in FAQ_INPUTS:
            return random.choice(FAQ_RESPONSES)

def joke_response():
    """Provide a random joke."""
    return random.choice(JOKE_RESPONSES)

def response(user_response):
    """Generate a response for user input."""
    if greeting(user_response):
        return greeting(user_response)
    if small_talk(user_response):
        return small_talk(user_response)
    if faq_response(user_response):
        return faq_response(user_response)
    if "joke" in user_response or "fun" in user_response:
        return joke_response()
    
    # Fallback to corpus-based response
    sent_tokens.append(user_response)
    TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
    tfidf = TfidfVec.fit_transform(sent_tokens)
    vals = cosine_similarity(tfidf[-1], tfidf)
    idx = vals.argsort()[0][-2]
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]
    sent_tokens.remove(user_response)
    if req_tfidf == 0:
        return "Maaf kari, hum samajh nahi paaye. 😕"
    else:
        return sent_tokens[idx]

# Telegram Bot Handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a welcome message."""
    await update.message.reply_text("Namaste! Humra naam Bubli hai. Kaise madad kari? 😊")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle user messages."""
    user_message = update.message.text
    bot_response = response(user_message)
    await update.message.reply_text(bot_response)

# Main function to start the bot
def main():
    # Telegram bot token
    TOKEN = "7561329328:AAELQQNBhe3UJRsAzVqspnHxuysbAQB4NHg"

    # Create the application
    app = ApplicationBuilder().token(TOKEN).build()

    # Adding handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Start the bot
    print("Bot is running...")
    app.run_polling()

if __name__ == '__main__':
    main()
