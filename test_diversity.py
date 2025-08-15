#!/usr/bin/env python3
"""
Test script to verify SAYRA's improved diversity and reduced repetition
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import find_best_quote

def test_diversity():
    """Test that SAYRA provides diverse responses and doesn't repeat quotes"""
    print("🎬 Testing SAYRA's Response Diversity")
    print("=" * 50)
    
    # Test with similar questions to see if we get different responses
    similar_questions = [
        "How can I be successful?",
        "What should I do to succeed?", 
        "I need advice for success",
        "Help me achieve my goals",
        "What's the secret to success?"
    ]
    
    print("Testing similar questions for diversity:")
    print("-" * 40)
    
    responses = []
    session_id = "test_session"
    
    for i, question in enumerate(similar_questions, 1):
        response, similarity = find_best_quote(question, session_id=session_id)
        responses.append(response)
        print(f"{i}. Q: '{question}'")
        print(f"   A: {response}")
        print(f"   Similarity: {similarity:.3f}")
        print()
    
    # Check for repetition
    unique_responses = set(responses)
    repetition_rate = (len(responses) - len(unique_responses)) / len(responses) * 100
    
    print("=" * 50)
    print(f"📊 Diversity Analysis:")
    print(f"Total responses: {len(responses)}")
    print(f"Unique responses: {len(unique_responses)}")
    print(f"Repetition rate: {repetition_rate:.1f}%")
    
    if repetition_rate < 20:
        print("✅ Good diversity! Low repetition rate.")
    elif repetition_rate < 50:
        print("⚠️  Moderate diversity. Some repetition detected.")
    else:
        print("❌ High repetition rate. Diversity needs improvement.")
    
    print("\n" + "=" * 50)
    print("Testing different question types:")
    print("-" * 40)
    
    # Test different types of questions
    diverse_questions = [
        "I'm feeling sad today",
        "How do I overcome fear?",
        "What's the meaning of life?",
        "I need relationship advice",
        "How do I make money?"
    ]
    
    for i, question in enumerate(diverse_questions, 1):
        response, similarity = find_best_quote(question, session_id=session_id)
        print(f"{i}. Q: '{question}'")
        print(f"   A: {response}")
        print()

if __name__ == "__main__":
    try:
        test_diversity()
        print("✅ Diversity test completed!")
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
