#!/usr/bin/env python3
"""
Test script for SAYRA chatbot
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import find_best_quote, analyze_sentiment, extract_keywords
import pandas as pd

def test_quote_matching():
    """Test the quote matching functionality"""
    print("🧪 Testing SAYRA Quote Matching...")
    
    test_cases = [
        "Hello there!",
        "I need help",
        "I'm feeling sad",
        "Show me the money",
        "I'll be back",
        "May the force be with you",
        "Life is like a box of chocolates",
        "I'm confused about something",
        "This is awesome!",
        "Goodbye for now"
    ]
    
    for test_input in test_cases:
        quote, similarity = find_best_quote(test_input)
        print(f"Input: '{test_input}'")
        print(f"Response: {quote}")
        print(f"Similarity: {similarity}")
        print("-" * 50)

def test_sentiment_analysis():
    """Test sentiment analysis"""
    print("\n🧪 Testing Sentiment Analysis...")
    
    test_texts = [
        "I'm so happy today!",
        "This is terrible",
        "I feel okay",
        "Amazing work!",
        "I'm really sad"
    ]
    
    for text in test_texts:
        sentiment = analyze_sentiment(text)
        print(f"Text: '{text}' -> Sentiment: {sentiment:.2f}")

def test_keyword_extraction():
    """Test keyword extraction"""
    print("\n🧪 Testing Keyword Extraction...")
    
    test_texts = [
        "I need help with my computer",
        "Show me the money please",
        "I love watching movies",
        "This is a great day for adventure"
    ]
    
    for text in test_texts:
        keywords = extract_keywords(text)
        print(f"Text: '{text}' -> Keywords: {keywords}")

if __name__ == "__main__":
    print("🎬 SAYRA Test Suite")
    print("=" * 50)
    
    try:
        test_quote_matching()
        test_sentiment_analysis()
        test_keyword_extraction()
        print("\n✅ All tests completed!")
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
