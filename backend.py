import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import openai
import os

# -----------------
# CONFIGURE API KEY
# -----------------
# Replace with your own key or set in terminal as: setx OPENAI_API_KEY "your_key_here"
openai.api_key = os.getenv("OPENAI_API_KEY")

# Load movie quotes dataset
df = pd.read_csv("movie_quotes.csv")

# Vectorize quotes
vectorizer = TfidfVectorizer()
quote_vectors = vectorizer.fit_transform(df['quote'])

def find_best_quote(user_input):
    # Match user input to closest movie quote
    user_vec = vectorizer.transform([user_input])
    similarity = cosine_similarity(user_vec, quote_vectors)
    index = similarity.argmax()
    return df.iloc[index]['quote'], df.iloc[index]['movie']

def chatbot():
    print("🎬 Welcome to SAYRA! I speak in iconic movie dialogues. Type 'exit' to quit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ['exit', 'quit']:
            print("SAYRA: That's all folks! 🍿")
            break

        # Get best fitting quote
        quote, movie = find_best_quote(user_input)

        # Optionally, enhance humor/fun with API
        try:
            prompt = f"User said: '{user_input}'. Respond only with a witty version of this movie quote: '{quote}' from {movie}."
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}]
            )
            bot_reply = response.choices[0].message.content.strip()
        except Exception as e:
            bot_reply = f"{quote} — {movie}"

        print(f"SAYRA: {bot_reply}")

if __name__ == "__main__":
    chatbot()
