# 🎬 SAYRA - Your AI Companion Who Speaks in Iconic Movie Dialogues

SAYRA is an intelligent chatbot that responds to your messages using iconic movie quotes and dialogues. Whether you're feeling happy, sad, confused, or excited, SAYRA will find the perfect movie quote to match your mood!

## ✨ Features

- **🎯 Contextual Intelligence**: SAYRA analyzes your questions to understand what you're really asking about (love, career, life advice, etc.)
- **🧠 Smart Quote Matching**: Uses advanced TF-IDF vectorization with topic and emotion detection to find truly relevant movie quotes
- **💭 Question-Aware Responses**: Provides movie quotes that actually answer your questions, not just random quotes
- **😊 Sentiment Awareness**: Analyzes your mood and responds with appropriate movie dialogues
- **🔄 Conversation Memory**: Remembers recent exchanges for better context understanding
- **✨ Enhanced Responses**: Optional OpenAI integration for more creative and contextual responses
- **🎪 Smart Fallback System**: Contextual fallback responses when no perfect match is found
- **🔊 Text-to-Speech**: SAYRA speaks her responses with a female voice for immersive experience
- **🎭 Voice Controls**: Toggle voice on/off and stop speech with easy-to-use controls
- **🌐 Web Interface**: Beautiful, responsive chat interface with voice capabilities
- **📚 Extensive Database**: Over 150 iconic movie quotes from various genres and eras

## 🚀 Quick Start

### Option 1: Easy Start (Recommended)
```bash
python start_sayra.py
```

### Option 2: Manual Start
1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the Flask app:
```bash
python app.py
```

3. Open your browser and go to: `http://localhost:5000`

## 🔧 Setup

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Optional: OpenAI API Key
For enhanced, more creative responses, set your OpenAI API key:

**Windows:**
```cmd
setx OPENAI_API_KEY "your_api_key_here"
```

**Mac/Linux:**
```bash
export OPENAI_API_KEY="your_api_key_here"
```

## 🎭 How It Works

1. **🔍 Intent Analysis**: SAYRA categorizes your question by topic (love, career, life advice, etc.) and emotion
2. **🎯 Contextual Matching**: Finds movie quotes that actually relate to your specific question or concern
3. **🧠 Smart Scoring**: Uses machine learning with topic boosting to prioritize relevant quotes
4. **💬 Response Crafting**: Creates contextual responses that connect the quote to your question
5. **🔄 Memory Integration**: Considers conversation history for better follow-up responses
6. **🔊 Voice Synthesis**: Speaks responses with a female voice using Web Speech API
7. **✨ AI Enhancement**: Optionally uses OpenAI for even more natural, conversational responses

## 🎪 Example Conversations

**User**: "How can I be successful in business?"
**SAYRA**: "When it comes to work and success, Jerry Maguire had it right: 'Show me the money!'"

**User**: "I'm having relationship problems"
**SAYRA**: "Ah, matters of the heart! As they wisely said in Casablanca: 'Here's looking at you, kid.'"

**User**: "What's the meaning of life?"
**SAYRA**: "Life's big questions, eh? Forrest Gump put it perfectly: 'Life is like a box of chocolates. You never know what you're gonna get.'"

**User**: "I'm scared to take risks"
**SAYRA**: "Fear is natural, but remember what Star Wars taught us: 'Do or do not, there is no try.'"

**User**: "How do I achieve my dreams?"
**SAYRA**: "Well, as they say in The Pursuit of Happyness: 'You got a dream, you gotta protect it.' - that's my advice to you!"

## 📁 Project Structure

```
sayra3/
├── app.py              # Main Flask application
├── backend.py          # Original console-based version
├── index.html          # Web interface
├── movie_quotes.csv    # Movie quotes database
├── start_sayra.py      # Easy startup script
├── test_sayra.py       # Test suite
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## 🧪 Testing

Run the test suite to verify functionality:
```bash
python test_sayra.py
```

## 🎬 Movie Database

SAYRA includes quotes from:
- Classic Hollywood films (Casablanca, Gone with the Wind)
- Modern blockbusters (Star Wars, Marvel movies)
- Animated favorites (Toy Story, Finding Nemo, Shrek)
- Comedy classics (Anchorman, Zoolander, The Big Lebowski)
- Bollywood hits (3 Idiots, Dangal, KGF)
- And many more!

## 🔮 Future Enhancements

- User preference learning
- Custom quote collections
- Voice interaction
- Multi-language support
- Movie recommendation integration

## 🤝 Contributing

Feel free to add more movie quotes to `movie_quotes.csv` or suggest improvements!

## 📝 License

This project is for educational and entertainment purposes. Movie quotes are property of their respective studios and creators.

---

**"May the Force be with you!" — Star Wars** 🌟
"# Sayra" 
"# Sayra" 
