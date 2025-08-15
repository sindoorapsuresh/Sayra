#!/usr/bin/env python3
"""
Startup script for SAYRA chatbot
"""

import os
import sys
import subprocess

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import flask
        import pandas
        import sklearn
        import textblob
        print("✅ All dependencies are installed!")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("📦 Installing dependencies...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
            print("✅ Dependencies installed successfully!")
            return True
        except subprocess.CalledProcessError:
            print("❌ Failed to install dependencies. Please run: pip install -r requirements.txt")
            return False

def check_data_files():
    """Check if required data files exist"""
    required_files = ["movie_quotes.csv", "index.html"]
    missing_files = []
    
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Missing required files: {missing_files}")
        return False
    
    print("✅ All required files are present!")
    return True

def start_sayra():
    """Start the SAYRA chatbot"""
    print("🎬 Starting SAYRA - Your AI companion who speaks in iconic movie dialogues!")
    print("=" * 70)
    
    if not check_dependencies():
        return False
    
    if not check_data_files():
        return False
    
    # Check if OpenAI API key is set (optional)
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  OpenAI API key not found. SAYRA will work with basic responses.")
        print("   To enable enhanced responses, set OPENAI_API_KEY environment variable.")
    else:
        print("✅ OpenAI API key found - enhanced responses enabled!")
    
    print("\n🚀 Starting SAYRA web server...")
    print("🌐 Open http://localhost:5000 in your browser to chat with SAYRA!")
    print("🛑 Press Ctrl+C to stop the server")
    print("-" * 70)
    
    try:
        from app import app
        app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n👋 SAYRA says: 'I'll be back!' - The Terminator")
    except Exception as e:
        print(f"❌ Error starting SAYRA: {e}")
        return False
    
    return True

if __name__ == "__main__":
    start_sayra()
