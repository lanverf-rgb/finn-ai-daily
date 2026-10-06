import os
import datetime

print("Testing GitHub Actions...")

key = os.environ.get("GEMINI_API_KEY", "")
if not key:
    print("ERROR: GEMINI_API_KEY secret not found!")
    exit(1)

print(f"Key found: {key[:10]}... length {len(key)}")

try:
    import google.generativeai as genai
    print("google-generativeai imported OK")
except Exception as e:
    print(f"Import failed: {e}")
    exit(1)

try:
    genai.configure(api_key=key)
    print("Configured OK")
    
    # UPDATED MODEL NAME - gemini-2.0-flash is deprecated, use 1.5-flash or 2.5-flash
    model_name = "gemini-1.5-flash"
    print(f"Trying model: {model_name}")
    
    model = genai.GenerativeModel(model_name)
    print("Model created OK")
    
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    prompt = f"""You are AI Daily newsletter writer. Date: {today}.

Write AI Daily with 4 AI news stories from last 24h. For each:
- Headline
- What happened (2 sentences)
- Why it matters (1 sentence)

Keep it short and real. Search your knowledge for recent AI news."""

    response = model.generate_content(prompt)
    text = response.text
    print("=== GENERATED ===")
    print(text)
    
    with open("substack_today.md", "w", encoding="utf-8") as f:
        f.write(f"# AI Daily - {today}\n\n" + text)
    with open("x_posts_today.md", "w", encoding="utf-8") as f:
        f.write(f"# X Posts - {today}\n\n" + text[:1000])
    
    print("SUCCESS - files saved")
    
except Exception as e:
    print(f"ERROR during generation: {e}")
    import traceback
    traceback.print_exc()
    # Try fallback model
    try:
        print("\nTrying fallback model gemini-1.5-flash-8b...")
        model = genai.GenerativeModel("gemini-1.5-flash-8b")
        response = model.generate_content("Write 4 short AI news headlines for today")
        print(response.text)
        with open("substack_today.md", "w", encoding="utf-8") as f:
            f.write(response.text)
        with open("x_posts_today.md", "w", encoding="utf-8") as f:
            f.write("Fallback success")
        print("Fallback SUCCESS")
    except Exception as e2:
        print(f"Fallback also failed: {e2}")
        exit(1)
