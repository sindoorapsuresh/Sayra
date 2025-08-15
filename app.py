from flask import Flask, render_template_string, request, jsonify
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import openai
import os
import random
import re
from textblob import TextBlob

app = Flask(__name__)

# Configure API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Simple conversation memory (in production, use a proper database)
conversation_memory = {}

# Track recently used quotes to prevent repetition
recent_quotes_cache = {}

# Load movie quotes dataset
df = pd.read_csv("movie_quotes.csv")

# Vectorize quotes
vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 2))
quote_vectors = vectorizer.fit_transform(df['quote'])

# Fallback responses when no good match is found
fallback_responses = [
    "Frankly, my dear, I don't give a damn. — Gone with the Wind",
    "I'll be back. — The Terminator",
    "May the Force be with you. — Star Wars",
    "Here's looking at you, kid. — Casablanca",
    "You talking to me? — Taxi Driver",
    "Show me the money! — Jerry Maguire",
    "I see dead people. — The Sixth Sense",
    "Houston, we have a problem. — Apollo 13",
    "Life is like a box of chocolates. You never know what you're gonna get. — Forrest Gump",
    "Keep your friends close, but your enemies closer. — The Godfather",
    "Nobody puts Baby in a corner. — Dirty Dancing",
    "I'm not bad. I'm just drawn that way. — Who Framed Roger Rabbit",
    "After all, tomorrow is another day! — Gone with the Wind",
    "Roads? Where we're going, we don't need roads. — Back to the Future",
    "I'm gonna make him an offer he can't refuse. — The Godfather",
    "Elementary, my dear Watson. — Sherlock Holmes",
    "Toto, I've a feeling we're not in Kansas anymore. — The Wizard of Oz"
]

# Contextual fallback responses for specific situations
contextual_fallbacks = {
    'greeting': [
        "Hello. My name is Inigo Montoya. You killed my father. Prepare to die. — The Princess Bride",
        "Here's looking at you, kid. — Casablanca",
        "Good morning, Vietnam! — Good Morning Vietnam"
    ],
    'farewell': [
        "I'll be back. — The Terminator",
        "Frankly, my dear, I don't give a damn. — Gone with the Wind",
        "May the Force be with you. — Star Wars"
    ],
    'confusion': [
        "I'm confused. — Confused",
        "There is no spoon. — The Matrix",
        "What we've got here is failure to communicate. — Cool Hand Luke"
    ],
    'excitement': [
        "I'm the king of the world! — Titanic",
        "Woohoo! — The Simpsons Movie",
        "To infinity and beyond! — Toy Story"
    ],
    'sadness': [
        "Nobody puts Baby in a corner. — Dirty Dancing",
        "I see dead people. — The Sixth Sense",
        "After all, tomorrow is another day! — Gone with the Wind"
    ]
}

def analyze_sentiment(text):
    """Analyze sentiment of user input"""
    blob = TextBlob(text)
    return blob.sentiment.polarity  # Returns -1 to 1

def extract_keywords(text):
    """Extract important keywords from user input"""
    # Remove common words and extract meaningful terms
    keywords = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
    return [word for word in keywords if word not in ['the', 'and', 'but', 'for', 'are', 'you', 'can', 'have', 'this', 'that', 'with', 'was', 'will']]

def categorize_user_intent(user_input):
    """Analyze user input to determine intent and topic"""
    user_lower = user_input.lower()

    # Question patterns
    question_patterns = {
        'advice': ['what should i', 'how do i', 'what can i', 'advice', 'suggest', 'recommend'],
        'motivation': ['motivate', 'inspire', 'encourage', 'boost', 'confidence', 'believe'],
        'love_relationship': ['love', 'relationship', 'dating', 'romance', 'heart', 'crush', 'partner'],
        'work_career': ['work', 'job', 'career', 'boss', 'office', 'business', 'success'],
        'life_philosophy': ['life', 'meaning', 'purpose', 'philosophy', 'wisdom', 'truth'],
        'friendship': ['friend', 'friendship', 'buddy', 'pal', 'companion'],
        'family': ['family', 'mother', 'father', 'parent', 'child', 'brother', 'sister'],
        'fear_courage': ['afraid', 'scared', 'fear', 'courage', 'brave', 'coward'],
        'dreams_goals': ['dream', 'goal', 'ambition', 'future', 'hope', 'wish'],
        'failure_success': ['fail', 'failure', 'success', 'win', 'lose', 'achievement'],
        'time_age': ['time', 'age', 'old', 'young', 'past', 'future', 'memory'],
        'money_wealth': ['money', 'rich', 'poor', 'wealth', 'expensive', 'cheap', 'cost'],
        'death_loss': ['death', 'die', 'loss', 'grief', 'goodbye', 'end'],
        'power_strength': ['power', 'strong', 'weak', 'strength', 'control', 'authority'],
        'justice_revenge': ['justice', 'revenge', 'fair', 'unfair', 'right', 'wrong']
    }

    # Emotion patterns
    emotion_patterns = {
        'happy': ['happy', 'joy', 'excited', 'great', 'awesome', 'wonderful', 'amazing'],
        'sad': ['sad', 'depressed', 'down', 'upset', 'hurt', 'crying', 'tears'],
        'angry': ['angry', 'mad', 'furious', 'rage', 'hate', 'annoyed'],
        'confused': ['confused', 'lost', 'don\'t understand', 'unclear', 'puzzled'],
        'tired': ['tired', 'exhausted', 'weary', 'sleepy', 'drained'],
        'lonely': ['lonely', 'alone', 'isolated', 'solitude', 'empty']
    }

    detected_topics = []
    detected_emotions = []

    # Check for topics
    for topic, keywords in question_patterns.items():
        if any(keyword in user_lower for keyword in keywords):
            detected_topics.append(topic)

    # Check for emotions
    for emotion, keywords in emotion_patterns.items():
        if any(keyword in user_lower for keyword in keywords):
            detected_emotions.append(emotion)

    return detected_topics, detected_emotions

def find_contextual_quotes(topics, emotions):
    """Find quotes that match specific topics and emotions"""
    # Topic-based quote mapping
    topic_quotes = {
        'advice': [
            "With great power comes great responsibility",
            "Do or do not, there is no try",
            "Life is like a box of chocolates",
            "The Force will be with you"
        ],
        'motivation': [
            "You're gonna need a bigger boat",
            "I'll be back",
            "May the Force be with you",
            "To infinity and beyond"
        ],
        'love_relationship': [
            "Here's looking at you, kid",
            "You had me at hello",
            "Nobody puts Baby in a corner",
            "I'm also just a girl, standing in front of a boy, asking him to love her"
        ],
        'work_career': [
            "Show me the money",
            "I'm gonna make him an offer he can't refuse",
            "Greed is good",
            "You're fired"
        ],
        'life_philosophy': [
            "Life is like a box of chocolates",
            "Hakuna Matata",
            "After all, tomorrow is another day",
            "There is no spoon"
        ],
        'fear_courage': [
            "I see dead people",
            "You're gonna need a bigger boat",
            "Do or do not, there is no try",
            "Fear leads to anger"
        ],
        'dreams_goals': [
            "To infinity and beyond",
            "I'm the king of the world",
            "Adventure is out there",
            "Just keep swimming"
        ],
        'failure_success': [
            "Life finds a way",
            "Houston, we have a problem",
            "After all, tomorrow is another day",
            "Get busy living, or get busy dying"
        ]
    }

    # Emotion-based quote mapping
    emotion_quotes = {
        'happy': [
            "Hakuna Matata",
            "I'm the king of the world",
            "To infinity and beyond",
            "Adventure is out there"
        ],
        'sad': [
            "After all, tomorrow is another day",
            "Nobody puts Baby in a corner",
            "Life is like a box of chocolates",
            "Just keep swimming"
        ],
        'angry': [
            "You talking to me",
            "Say hello to my little friend",
            "I'm mad as hell and I'm not gonna take this anymore",
            "Frankly, my dear, I don't give a damn"
        ],
        'confused': [
            "There is no spoon",
            "What we've got here is failure to communicate",
            "I'm not a smart man, but I know what love is",
            "Houston, we have a problem"
        ]
    }

    candidate_quotes = []

    # Add topic-based quotes
    for topic in topics:
        if topic in topic_quotes:
            candidate_quotes.extend(topic_quotes[topic])

    # Add emotion-based quotes
    for emotion in emotions:
        if emotion in emotion_quotes:
            candidate_quotes.extend(emotion_quotes[emotion])

    return list(set(candidate_quotes))  # Remove duplicates

def get_session_id_for_quotes(request):
    """Get session ID for quote tracking"""
    return request.remote_addr or 'default'

def add_to_recent_quotes(session_id, quote_movie_pair):
    """Add a quote to recent quotes cache to prevent repetition"""
    if session_id not in recent_quotes_cache:
        recent_quotes_cache[session_id] = []

    recent_quotes_cache[session_id].append(quote_movie_pair)

    # Keep only last 5 quotes to prevent repetition
    if len(recent_quotes_cache[session_id]) > 5:
        recent_quotes_cache[session_id] = recent_quotes_cache[session_id][-5:]

def is_recently_used(session_id, quote_movie_pair):
    """Check if a quote was recently used"""
    if session_id not in recent_quotes_cache:
        return False
    return quote_movie_pair in recent_quotes_cache[session_id]

def find_best_quote(user_input, threshold=0.08, session_id='default'):
    """Find the best matching movie quote for user input with enhanced contextual matching and diversity"""
    # Analyze user intent and emotions
    topics, emotions = categorize_user_intent(user_input)

    # Get contextually relevant quotes
    contextual_candidates = find_contextual_quotes(topics, emotions)

    # Basic TF-IDF similarity
    user_vec = vectorizer.transform([user_input])
    similarity = cosine_similarity(user_vec, quote_vectors)

    # Create boosted similarity matrix
    boosted_similarity = similarity.copy()

    # Heavily boost contextually relevant quotes
    if contextual_candidates:
        for i, (_, row) in enumerate(df.iterrows()):
            quote_text = row['quote'].lower()
            for candidate in contextual_candidates:
                if candidate.lower() in quote_text:
                    boosted_similarity[0][i] += 0.5  # Strong boost for contextual relevance

    # Extract keywords for additional matching
    keywords = extract_keywords(user_input)

    # Boost scores for quotes containing keywords
    for i, (_, row) in enumerate(df.iterrows()):
        quote_text = row['quote'].lower()
        keyword_boost = 0
        for keyword in keywords:
            if keyword in quote_text:
                keyword_boost += 0.15
        boosted_similarity[0][i] += keyword_boost

    # Sentiment-based boosting
    user_sentiment = analyze_sentiment(user_input)
    for i, (_, row) in enumerate(df.iterrows()):
        quote_sentiment = analyze_sentiment(row['quote'])
        # Boost quotes with similar sentiment
        if abs(user_sentiment - quote_sentiment) < 0.3:
            boosted_similarity[0][i] += 0.1

    # DIVERSITY ENHANCEMENT: Penalize recently used quotes
    for i, (_, row) in enumerate(df.iterrows()):
        quote_movie_pair = f"{row['quote']} — {row['movie']}"
        if is_recently_used(session_id, quote_movie_pair):
            boosted_similarity[0][i] *= 0.3  # Heavily penalize recently used quotes

    # Get top 3 candidates instead of just the best one for more variety
    top_indices = boosted_similarity[0].argsort()[-3:][::-1]  # Top 3 in descending order

    # Select from top candidates, avoiding recently used ones
    selected_index = None
    selected_similarity = 0

    for idx in top_indices:
        quote = df.iloc[idx]['quote']
        movie = df.iloc[idx]['movie']
        quote_movie_pair = f"{quote} — {movie}"
        similarity_score = boosted_similarity[0][idx]

        if not is_recently_used(session_id, quote_movie_pair) and similarity_score >= threshold:
            selected_index = idx
            selected_similarity = similarity_score
            break

    # If no non-recent quote found, use the best one anyway but with lower threshold
    if selected_index is None:
        max_similarity = boosted_similarity.max()
        if max_similarity >= threshold * 0.5:  # Lower threshold for fallback
            selected_index = boosted_similarity.argmax()
            selected_similarity = max_similarity

    # If still no good match, return contextual fallback
    if selected_index is None:
        user_lower = user_input.lower()
        if any(word in user_lower for word in ['hello', 'hi', 'hey', 'greetings']):
            return random.choice(contextual_fallbacks['greeting']), None
        elif any(word in user_lower for word in ['bye', 'goodbye', 'farewell', 'see you']):
            return random.choice(contextual_fallbacks['farewell']), None
        elif any(word in user_lower for word in ['confused', 'don\'t understand', 'what', 'huh']):
            return random.choice(contextual_fallbacks['confusion']), None
        elif any(word in user_lower for word in ['excited', 'awesome', 'great', 'amazing', 'wow']):
            return random.choice(contextual_fallbacks['excitement']), None
        elif any(word in user_lower for word in ['sad', 'depressed', 'down', 'upset']):
            return random.choice(contextual_fallbacks['sadness']), None
        else:
            return random.choice(fallback_responses), None

    quote = df.iloc[selected_index]['quote']
    movie = df.iloc[selected_index]['movie']
    quote_movie_pair = f"{quote} — {movie}"

    # Add to recent quotes cache
    add_to_recent_quotes(session_id, quote_movie_pair)

    return quote_movie_pair, selected_similarity

def create_contextual_response(user_input, quote, movie):
    """Create a contextual response that relates the quote to the user's question"""
    user_lower = user_input.lower()

    # Question-specific response templates
    if any(word in user_lower for word in ['what should i', 'how do i', 'advice', 'help me']):
        return f"Well, as they say in {movie}: '{quote}' - that's my advice to you!"

    elif any(word in user_lower for word in ['why', 'how come', 'explain']):
        return f"Let me put it this way, like in {movie}: '{quote}'"

    elif any(word in user_lower for word in ['feel', 'feeling', 'emotion']):
        return f"I understand how you feel. Remember what they said in {movie}: '{quote}'"

    elif any(word in user_lower for word in ['love', 'relationship', 'dating']):
        return f"Ah, matters of the heart! As they wisely said in {movie}: '{quote}'"

    elif any(word in user_lower for word in ['work', 'job', 'career', 'business']):
        return f"When it comes to work and success, {movie} had it right: '{quote}'"

    elif any(word in user_lower for word in ['life', 'meaning', 'purpose']):
        return f"Life's big questions, eh? {movie} put it perfectly: '{quote}'"

    elif any(word in user_lower for word in ['afraid', 'scared', 'fear']):
        return f"Fear is natural, but remember what {movie} taught us: '{quote}'"

    elif any(word in user_lower for word in ['dream', 'goal', 'future']):
        return f"Dreams are important! As {movie} reminds us: '{quote}'"

    elif any(word in user_lower for word in ['fail', 'failure', 'mistake']):
        return f"Everyone faces setbacks. {movie} had the right perspective: '{quote}'"

    else:
        return f"'{quote}' — {movie}"

def enhance_response(user_input, quote, movie):
    """Enhance the response using OpenAI API if available, with fallback to contextual responses"""
    try:
        if movie and openai.api_key:  # Only enhance if we have a real movie quote and API key
            prompt = f"""User asked: '{user_input}'.

            Respond as SAYRA, a movie-loving chatbot, using this relevant movie quote: '{quote}' from {movie}.

            Make your response:
            1. Directly address their question/concern
            2. Naturally incorporate the movie quote
            3. Be conversational and helpful
            4. Keep it under 100 words

            Example format: "That's a great question! As they say in [movie]: '[quote]' - and I think that applies perfectly to your situation because..."
            """

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=150,
                temperature=0.7
            )
            return response.choices[0].message.content.strip()
        else:
            # Fallback to contextual response if no API key
            return create_contextual_response(user_input, quote, movie)
    except Exception as e:
        print(f"OpenAI API error: {e}")
        # Fallback to contextual response
        return create_contextual_response(user_input, quote, movie)

@app.route('/')
def home():
    """Serve the main chat interface"""
    with open('index.html', 'r', encoding='utf-8') as f:
        return f.read()

def get_session_id(request):
    """Get or create a session ID for conversation tracking"""
    # In a real app, you'd use proper session management
    # For now, we'll use IP address as a simple identifier
    return request.remote_addr or 'default'

def update_conversation_memory(session_id, user_message, bot_response):
    """Update conversation memory for context"""
    if session_id not in conversation_memory:
        conversation_memory[session_id] = []

    conversation_memory[session_id].append({
        'user': user_message,
        'bot': bot_response,
        'timestamp': pd.Timestamp.now()
    })

    # Keep only last 5 exchanges to prevent memory bloat
    if len(conversation_memory[session_id]) > 5:
        conversation_memory[session_id] = conversation_memory[session_id][-5:]

def get_conversation_context(session_id):
    """Get recent conversation context"""
    if session_id in conversation_memory:
        return conversation_memory[session_id][-3:]  # Last 3 exchanges
    return []

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat messages"""
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        session_id = get_session_id(request)

        if not user_message:
            return jsonify({'reply': 'I need something to work with here! — SAYRA'})

        # Get conversation context
        context = get_conversation_context(session_id)

        # Check for follow-up questions or references to previous conversation
        if context and any(word in user_message.lower() for word in ['what', 'that', 'it', 'this', 'again', 'more']):
            # Add context to the user message for better matching
            context_text = ' '.join([exchange['user'] for exchange in context])
            enhanced_user_message = f"{context_text} {user_message}"
        else:
            enhanced_user_message = user_message

        # Find best matching quote with session-based diversity
        quote_response, similarity = find_best_quote(enhanced_user_message, session_id=session_id)

        # Extract quote and movie if it's a real match
        if similarity and similarity > 0.1:
            parts = quote_response.split(' — ')
            if len(parts) == 2:
                quote, movie = parts
                enhanced_response = enhance_response(user_message, quote, movie)
            else:
                enhanced_response = quote_response
        else:
            enhanced_response = enhance_response(user_message, quote_response, None)

        # Update conversation memory
        update_conversation_memory(session_id, user_message, enhanced_response)

        return jsonify({'reply': enhanced_response})

    except Exception as e:
        print(f"Error in chat endpoint: {e}")
        return jsonify({'reply': 'Something went wrong. But as they say, "Tomorrow is another day!" — Gone with the Wind'})

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'SAYRA is ready to chat!', 'quotes_loaded': len(df)})

if __name__ == '__main__':
    print("🎬 Starting SAYRA - Your AI companion who speaks in iconic movie dialogues!")
    print(f"📚 Loaded {len(df)} movie quotes")
    print("🌐 Open http://localhost:5000 in your browser")
    app.run(debug=True, host='0.0.0.0', port=5000)
