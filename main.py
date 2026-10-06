import os
import datetime
from google import genai

key = os.environ.get("GEMINI_API_KEY", "")
if not key:
    print("ERROR: GEMINI_API_KEY missing")
    exit(1)

client = genai.Client(api_key=key)

# List models first
print("=== AVAILABLE MODELS ===")
try:
    models = client.models.list()
    for m in list(models)[:30]:
        print(f" - {m.name}")
except Exception as e:
    print(f"List failed: {e}")

today = datetime.datetime.now().strftime("%Y-%m-%d")

# Try models in order - newest first as Google recommends
models_to_try = [
    "gemini-3.8-flash",
    "gemini-3-flash-preview",
    "gemini-2.5-flash",
    "gemini-2.5-flash-lite",
    "gemini-flash-latest",
    "gemini-flash-lite-latest",
    "gemini-2.0-flash",
    "gemini-2.0-flash-lite",
]

prompt = f"""Date: {today}. Write AI Daily with 4 short AI news stories (headline + 2 sentences + why matters). Real news."""

success = False
for model_name in models_to_try:
    try:
        print(f"\nTrying: {model_name}...")
        response = client.models.generate_content(
            model=model_name,
            contents=prompt
        )
        text = response.text
        print(f"SUCCESS with {model_name}!")
        print(text[:500])
        
        with open("substack_today.md", "w", encoding="utf-8") as f:
            f.write(f"# AI Daily - {today}\n\nModel: {model_name}\n\n" + text)
        with open("x_posts_today.md", "w", encoding="utf-8") as f:
            f.write(text[:2000])
        
        success = True
        break
    except Exception as e:
        print(f"Failed {model_name}: {e}")
        continue

if not success:
    print("ALL MODELS FAILED")
    exit(1)

print("DONE - green check!")
