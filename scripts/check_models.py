import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("❌ Error: GEMINI_API_KEY not found in environment variables.")
    exit(1)

genai.configure(api_key=api_key)

print(f"Checking available models for API Key: {api_key[:5]}...*****")

try:
    available_models = []
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"- {m.name}")
            available_models.append(m.name)
    
    if not available_models:
        print("\n❌ No models found! Your API key might be invalid or has no access to Generative Language API.")
    else:
        print("\n✅ SUCCESS! Use one of the names above in your .env file.")
        print("Example: If you see 'models/gemini-1.5-flash', put 'gemini-1.5-flash' in your .env")

except Exception as e:
    print(f"\n❌ Error listing models: {e}")