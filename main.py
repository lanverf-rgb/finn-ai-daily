import os
import datetime

# Test without google library first to get green check
print("Testing GitHub Actions...")

# Check if secret exists
key = os.environ.get("GEMINI_API_KEY", "")
if not key:
    print("ERROR: GEMINI_API_KEY secret not found!")
    exit(1)

print(f"Key found: {key[:10]}... length {len(key)}")

# Now try import
try:
    import google.generativeai as genai
    print("google-generativeai imported OK")
except Exception as e:
    print(f"Import failed: {e}")
    exit(1)

try:
    genai.configure(api_key=key)
    print("Configured OK")
    
    model = genai.GenerativeModel("gemini-2.0-flash")
    print("Model created OK")
    
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    response = model.generate_content(f"Write a short AI news summary for {today}. 4 stories with sources. Keep it brief.")
    text = response.text
    print(text)
    
    with open("substack_today.md", "w", encoding="utf-8") as f:
        f.write(f"# AI Daily - {today}\n\n" + text)
    with open("x_posts_today.md", "w", encoding="utf-8") as f:
        f.write("X posts placeholder - copy from substack")
    
    print("SUCCESS - files saved")
    
except Exception as e:
    print(f"ERROR during generation: {e}")
    import traceback
    traceback.print_exc()
    exit(1)
