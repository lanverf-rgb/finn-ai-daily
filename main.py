import os
import datetime
from google import genai

print("Testing new google-genai library...")

key = os.environ.get("GEMINI_API_KEY", "")
if not key:
    print("ERROR: GEMINI_API_KEY secret not found!")
    exit(1)

print(f"Key found: {key[:10]}... len {len(key)}")

try:
    client = genai.Client(api_key=key)
    print("Client created OK")

    # List available models to debug
    print("Listing models...")
    models = client.models.list()
    for m in models:
        if "flash" in m.name.lower() or "pro" in m.name.lower():
            print(f" - {m.name}")

    today = datetime.datetime.now().strftime("%Y-%m-%d")
    
    # Use gemini-2.5-flash - latest stable free model
    model_name = "gemini-2.5-flash"
    print(f"Trying model: {model_name}")
    
    prompt = f"""You are AI Daily newsletter writer. Date: {today}.

Write AI Daily newsletter with 4 AI news stories from last 24h. Format:

# AI Daily - {today}

1. **Headline**
What happened: 2 sentences
Why it matters: 1 sentence
Source: real source name

2. etc...

Keep it short, real, English."""

    response = client.models.generate_content(
        model=model_name,
        contents=prompt
    )
    
    text = response.text
    print("=== GENERATED ===")
    print(text)
    
    with open("substack_today.md", "w", encoding="utf-8") as f:
        f.write(text)
    with open("x_posts_today.md", "w", encoding="utf-8") as f:
        f.write(text[:2000])
    
    print("SUCCESS - files saved")

except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
    exit(1)
