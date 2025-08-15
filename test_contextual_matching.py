#!/usr/bin/env python3
"""
Test script for SAYRA's enhanced contextual matching
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import find_best_quote, categorize_user_intent, create_contextual_response

def test_contextual_questions():
    """Test SAYRA's ability to answer contextual questions"""
    print("🧪 Testing SAYRA's Contextual Question Answering...")
    print("=" * 60)
    
    test_questions = [
        # Advice/Help questions
        "What should I do when I'm feeling lost?",
        "How do I deal with failure?",
        "Can you give me some life advice?",
        
        # Love/Relationship questions
        "How do I know if someone loves me?",
        "What should I do about my relationship?",
        "I'm having trouble with dating",
        
        # Work/Career questions
        "How can I be successful in business?",
        "What's the secret to making money?",
        "I'm having problems at work",
        
        # Life philosophy questions
        "What's the meaning of life?",
        "How should I live my life?",
        "What's important in life?",
        
        # Fear/Courage questions
        "I'm scared to take risks",
        "How do I overcome my fears?",
        "I need courage to face challenges",
        
        # Dreams/Goals questions
        "How do I achieve my dreams?",
        "What if my goals seem impossible?",
        "I want to pursue my passion",
        
        # Emotional questions
        "I'm feeling really sad today",
        "I'm so angry about everything",
        "I'm confused about what to do",
        "I'm really happy right now!"
    ]
    
    for question in test_questions:
        print(f"\n🎭 Question: '{question}'")
        
        # Test intent categorization
        topics, emotions = categorize_user_intent(question)
        print(f"📊 Detected Topics: {topics}")
        print(f"😊 Detected Emotions: {emotions}")
        
        # Test quote matching
        quote_response, similarity = find_best_quote(question)
        print(f"🎬 Response: {quote_response}")
        print(f"📈 Similarity Score: {similarity}")
        
        # Test contextual response creation
        if quote_response and ' — ' in quote_response:
            parts = quote_response.split(' — ')
            if len(parts) == 2:
                quote, movie = parts
                contextual_response = create_contextual_response(question, quote, movie)
                print(f"💬 Contextual Response: {contextual_response}")
        
        print("-" * 60)

def test_specific_scenarios():
    """Test specific conversation scenarios"""
    print("\n🎯 Testing Specific Conversation Scenarios...")
    print("=" * 60)
    
    scenarios = [
        ("I just got fired from my job", "Work/Career Crisis"),
        ("My girlfriend broke up with me", "Relationship Issues"),
        ("I don't know what to do with my life", "Life Direction"),
        ("I'm afraid to start my own business", "Fear of Risk"),
        ("How do I become rich?", "Financial Success"),
        ("I feel like giving up on my dreams", "Motivation/Persistence"),
        ("What makes a good friend?", "Friendship"),
        ("I'm worried about getting older", "Aging/Time"),
        ("How do I deal with bullies?", "Conflict Resolution"),
        ("I want to be famous", "Fame/Recognition")
    ]
    
    for question, scenario_type in scenarios:
        print(f"\n🎭 Scenario: {scenario_type}")
        print(f"❓ Question: '{question}'")
        
        quote_response, similarity = find_best_quote(question)
        print(f"🎬 SAYRA's Response: {quote_response}")
        print(f"📈 Relevance Score: {similarity}")
        print("-" * 60)

if __name__ == "__main__":
    print("🎬 SAYRA Enhanced Contextual Matching Test Suite")
    print("Testing how well SAYRA answers questions with relevant movie dialogues")
    print("=" * 80)
    
    try:
        test_contextual_questions()
        test_specific_scenarios()
        print("\n✅ All contextual matching tests completed!")
        print("🎭 SAYRA should now provide much more relevant movie quote responses!")
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
