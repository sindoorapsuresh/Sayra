#!/usr/bin/env python3
"""
Demo script showing SAYRA's enhanced contextual responses
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import find_best_quote, create_contextual_response

def demo_enhanced_responses():
    """Demonstrate SAYRA's enhanced contextual responses"""
    print("🎬 SAYRA Enhanced Contextual Response Demo")
    print("=" * 60)
    print("See how SAYRA now provides movie quotes that actually relate to your questions!")
    print()
    
    demo_conversations = [
        {
            "category": "💼 Career Advice",
            "questions": [
                "How can I be more successful at work?",
                "I'm thinking about starting my own business",
                "What's the key to making money?"
            ]
        },
        {
            "category": "💕 Love & Relationships", 
            "questions": [
                "How do I know if someone really loves me?",
                "I'm having relationship problems",
                "What makes a good relationship?"
            ]
        },
        {
            "category": "🌟 Life Philosophy",
            "questions": [
                "What's the meaning of life?",
                "How should I live my life?",
                "What's really important in life?"
            ]
        },
        {
            "category": "💪 Motivation & Dreams",
            "questions": [
                "I want to achieve my dreams",
                "How do I stay motivated?",
                "What if my goals seem impossible?"
            ]
        },
        {
            "category": "😰 Dealing with Fear",
            "questions": [
                "I'm scared to take risks",
                "How do I overcome my fears?",
                "I need courage to face challenges"
            ]
        },
        {
            "category": "😢 Emotional Support",
            "questions": [
                "I'm feeling really sad today",
                "I'm so angry about everything", 
                "I'm confused about what to do"
            ]
        }
    ]
    
    for conversation in demo_conversations:
        print(f"\n{conversation['category']}")
        print("-" * 40)
        
        for question in conversation['questions']:
            print(f"\n🗣️  You: \"{question}\"")
            
            # Get SAYRA's response
            quote_response, similarity = find_best_quote(question)
            
            if quote_response and ' — ' in quote_response:
                parts = quote_response.split(' — ')
                if len(parts) == 2:
                    quote, movie = parts
                    contextual_response = create_contextual_response(question, quote, movie)
                    print(f"🎭 SAYRA: {contextual_response}")
                    print(f"📊 Relevance Score: {similarity:.2f}")
                else:
                    print(f"🎭 SAYRA: {quote_response}")
            else:
                print(f"🎭 SAYRA: {quote_response}")
        
        print("\n" + "=" * 60)

if __name__ == "__main__":
    print("🎬 Welcome to the SAYRA Enhanced Demo!")
    print("This shows how SAYRA now provides contextually relevant movie quotes")
    print("that actually relate to your questions and concerns.")
    print()
    
    try:
        demo_enhanced_responses()
        print("\n✨ Demo completed!")
        print("🌐 Try chatting with SAYRA at http://localhost:5000")
        print("🎭 Ask any question and see how she responds with relevant movie wisdom!")
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()
